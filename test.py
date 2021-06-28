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
import argparse

from rectification import *
from Speed_estimate import SpeedEstimation


def calibration_image_median(data):
    # real data (m)
    real_width_car= 2
    real_length_car= 4

    real_width_motor= 0.5
    real_length_motor=2

    real_width_person=0.5
    real_height_person=0.5

    width_pixel_car=[]
    length_pixel_car=[]

    width_pixel_motor=[]
    length_pixel_motor=[]

    width_pixel_person=[]
    height_pixel_person=[]

    for obj in data:
        try:
            if data[obj]['label'] == 'car':
                for box in data[obj]['boxes']:
                    width_pixel_car.append(min(box[2]-box[0],box[3]-box[1]))
                    length_pixel_car.append(max(box[2]-box[0],box[3]-box[1]))

            if data[obj]['label'] == 'motor':
                for box in data[obj]['boxes']:
                    width_pixel_motor.append(min(box[2]-box[0],box[3]-box[1]))
                    length_pixel_motor.append(max(box[2]-box[0],box[3]-box[1]))

            if data[obj]['label'] == 'pedestrian':
                for box in data[obj]['boxes']:
                    width_pixel_person.append(min(box[2]-box[0],box[3]-box[1]))
                    height_pixel_person.append(max(box[2]-box[0],box[3]-box[1]))
        except:
            continue

    if len(width_pixel_car) !=0:
        median_x = statistics.mean(width_pixel_car)
        median_y = statistics.mean(length_pixel_car)
        return real_width_car/median_x, real_length_car/median_y

    elif len(width_pixel_motor) !=0:
        median_x = statistics.mean(width_pixel_motor)
        median_y = statistics.mean(length_pixel_motor)
        return real_width_motor/median_x, real_length_motor/median_y
    else:
        median_x = statistics.mean(width_pixel_person)
        median_y = statistics.mean(height_pixel_person)
        return real_width_person/median_x, real_height_person/median_y

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--videopath", help=" path of video mp4 ", default="car_hightway.mp4")
    parse.add_argument("--resultpath", help=" path of result video mp4 ", default="car_hightway_speed.mp4")
    parse.add_argument("--pklpath", help=" path of pkl file", default="car_hightway.pkl" )
    parse.add_argument("--widthreal", help= "real width",default=150)
    parse.add_argument("--heightreal", help="real height",default=70)

    agrs= parse.parse_args()

    with open(agrs.pklpath,"rb") as f:
        data= pickle.load(f)

    cap= cv2.VideoCapture(agrs.videopath)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    result = cv2.VideoWriter(agrs.resultpath,cv2.VideoWriter_fourcc(*'MJPG'),30,size)
                            

    fps = cap.get(cv2.CAP_PROP_FPS)
    _,img_frame = cap.read()
    H, max_x,max_y = matrix_homorgenous(img_frame)

    # estimate x,y in real 
    x= agrs.widthreal
    y= agrs.heightreal

    # coeffient width, height for image plane
    coef_x=x/max_x
    coef_y=y/max_y



    # "12.mkv"
    # coef_x,coef_y = 50/3000,50/1064
    # "video_cut"
    # coef_x,coef_y = 70/1022,50/1202 
    # "car_highway"
    # coef_x,coef_y = 150/1076,70/1324
    # "town"
    # coef_x,coef_y = 30/7680,70/7680 

    while True:
        ret,frame= cap.read()
        if not ret:
            break
        if ret:
            for obj in data:
                try:
                    for ind,fr in enumerate(data[obj]['frames']):
                        if fr == cap.get(cv2.CAP_PROP_POS_FRAMES) :
                            x_min_i,y_min_i,x_max_i,y_max_i = data[obj]['boxes'][ind]
                            loc_after = data[obj]['boxes'][ind]
                            loc_before = data[obj]['boxes'][ind-1]
                            speed= SpeedEstimation(loc_before, loc_after, 2 , 4, H, fps, coef_x,coef_y).compute_speed()
                            cv2.rectangle(frame, (x_min_i,y_min_i), (x_max_i,y_max_i), (0,0,255))
                            cv2.putText(frame,"{}km/h".format(int(speed)),(x_min_i-2,y_min_i-2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                except:
                    traceback.print_exc()
            # result.write(frame)
            cv2.imshow("Image",cv2.resize(frame,(1500,1000)))
            if cv2.waitKey(20) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()
        
if __name__=="__main__":
    main()
