from skimage import transform
import math

class SpeedEstimation:
    def __init__(self, loc_before , loc_after, idfr_before , idfr_after , H , fps , coef_x ,coef_y):

        self.loc_before = loc_before
        self.loc_after = loc_after
        self.idfr_before = idfr_before
        self.idfr_after = idfr_after
        self.H = H
        self.fps = fps
        self.coef_x= coef_x
        self.coef_y= coef_y

    def matrix_transform(self,loc):
        return transform.matrix_transform(loc, self.H)[0]

    def compute_speed (self):
        loc1 = ( (self.loc_before[0]+self.loc_before[2])//2 , (self.loc_before[1]+ self.loc_before[3])//2 )
        loc2 = ( (self.loc_after[0]+self.loc_after[2])//2 , (self.loc_after[1]+ self.loc_after[3])//2 )
        
        loc1_to_real = self.matrix_transform(loc1)
        loc2_to_real = self.matrix_transform(loc2)


        Rx= abs(loc2_to_real[0] - loc1_to_real[0])
        Ry= abs(loc2_to_real[1] - loc1_to_real[1])
        R = math.sqrt( (Rx*self.coef_x)**2 + (Ry*self.coef_y)**2)

        speed = R * self.fps * 3.6 / (self.idfr_after - self.idfr_before) 
        return  speed


