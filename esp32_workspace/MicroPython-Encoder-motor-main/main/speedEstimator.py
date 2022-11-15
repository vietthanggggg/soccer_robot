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
        

def uni_to_diff(v,w, radius, L):

    vel_r = (2 * v + w * L)/(2 * radius);
    vel_l = (2 * v - w * L)/(2 * radius);
    
    return vel_l, vel_r
