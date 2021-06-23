import glob
import cv2
import pickle 
import math
import random
import datetime
import numpy as np
import statistics
from skimage import transform
import traceback

from rectification import *




def compute_time(frame1,frame2):
    date1 = datetime.datetime.strptime(frame1, "%H:%M:%S")
    date2 = datetime.datetime.strptime(frame2, "%H:%M:%S")
    return datetime.datetime.timestamp(date2)-datetime.datetime.timestamp(date1)

def img2ground(point,H):
    return transform.matrix_transform(point, H)[0]

def calibration_image_median(data):
    real_width_car= 0.002
    real_width_motor= 0.001
    real_width_person=0.0005

    width_pixel_car=[]
    width_pixel_motor=[]
    width_pixel_person=[]

    for obj in data:
        try:
            if data[obj]['label'] == 'car':
                for box in data[obj]['boxes']:
                    width_pixel_car.append(box[2]-box[0])
                    
            if data[obj]['label'] == 'motor':
                for box in data[obj]['boxes']:
                    width_pixel_motor.append(box[2]-box[0])
            
            if data[obj]['label'] == 'pedestrian':
                for box in data[obj]['boxes']:
                    width_pixel_person.append(box[2]-box[0])
        except:
            continue
    if len(width_pixel_motor) !=0:
        median = statistics.median(width_pixel_motor)
        return real_width_motor/median
    elif len(width_pixel_car) !=0:
        median = statistics.median(width_pixel_car)
        return real_width_car/median
    else:
        median = statistics.median(width_pixel_person)
        return real_width_person/median


def estimate_speed(x_before,x_after,Sx,Sy,fps,H):
    i_x= x_after[0]-x_before[0]
    i_y= x_after[1]-x_before[1]
    t_x,t_y = img2ground((i_x,i_y),H)
    speed = math.sqrt((i_x*Sx)**2+(i_y*Sx)**2)
    return speed * 3600*fps/2

if __name__== "__main__":
    with open("12.pkl","rb") as f:
        data= pickle.load(f)

    cap= cv2.VideoCapture("12.mkv")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    result = cv2.VideoWriter('filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),30,size)
                            
    cal_coef= calibration_image_median(data)
    fps = cap.get(cv2.CAP_PROP_FPS)
    _,img_frame = cap.read()
    H = matrix_homorgenous(img_frame)

    Sx=cal_coef
    Sy=Sx*frame_height/frame_width

    vel=[0]
    while True:
        ret,frame= cap.read()
        if not ret:
            break
        if ret:
            for obj in data:
                try:
                    for ind,fr in enumerate(data[obj]['frames']):
                        if fr == cap.get(cv2.CAP_PROP_POS_FRAMES) :
                            x_min_i,y_min_i,x_max_i,y_max_i=data[obj]['boxes'][ind]
                            x_min_old_i,y_min_old_i,x_max_old_i,y_max_old_i=data[obj]['boxes'][ind-1]

                            # (x_min,y_min) = img2ground((x_min_i,y_min_i))
                            # (x_max,y_max) = img2ground((x_max_i,y_max_i))
                            # (x_min_old,y_min_old) = img2ground((x_min_old_i,y_min_old_i))
                            # (x_max_old,y_max_old)= img2ground((x_max_old_i,y_max_old_i))
                            
                            x_before=((x_max_i+x_min_i)/2,(y_max_i+y_min_i)/2)
                            x_before= img2ground(x_before,H) 
                            # print(x_before)
                            x_after=((x_max_old_i+x_min_i)/2,(y_max_old_i+y_min_old_i)/2)
                            x_after= img2ground(x_after,H)
                            # print(x_after)
                            # w_tb= int((x_max_i-x_min_i)/2 + (x_max_old_i-x_min_old_i)/2)
                            # cal_coef= calibration_image_2(w_tb)
                            # time= abs(compute_time( data[obj]['times'][ind-fr//2], data[obj]['times'][ind]))
                            # time_line.append(data[obj]['times'][ind])
                            # speed = convPtoR_2(x_before[0],x_before[1],x_after[0],x_after[1]) *3.6*fps/2
                            speed = estimate_speed(x_before,x_after,Sx,Sy,fps,H)
                            if abs(vel[-1]-speed) >3:
                                vel.append(speed)
                            else:
                                speed=vel[-1] 
                            # speed_es= (vel[-1] * len(vel) + speed)/(len(vel)+1)
                            cv2.rectangle(frame, (x_min_i,y_min_i), (x_max_i,y_max_i), (0,0,255))
                            cv2.putText(frame,"{}km/h".format(int(speed)),(x_min_i-2,y_min_i-2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                except:
                    traceback.print_exc()
            # result.write(frame)
            cv2.imshow("Image",cv2.resize(frame,(2000,1500)))
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()
        

