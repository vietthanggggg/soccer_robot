import math

class speedEstimator():

    def __init__(self, radius, R, L):
        '''
            Initialize speed estimator
            
            el - left wheel encoder
            er - right wheel encoder
            R - radious of the wheels in meters
            L - distance  between the wheels in meters
        '''
        self.radius = radius
        self.R = R
        self.L = L
        

def uni_to_diff(v,w,radius_r,radius_l, L):

    vel_r = (2 * v - w * L)/(2 * radius_r);
    vel_l = (2 * v + w * L)/(2 * radius_l);
    
    return vel_l, vel_r
