import cv2
import numpy as np
import cv2.aruco as aruco
from aruco_lib import *
#from scan import *
from transform import four_point_transform
import time

cap = cv2.VideoCapture(1)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

det_aruco_list = {}

while True:
    ret,n_frame = cap.read()

    # det_aruco_list = detect_Aruco(n_frame)
    # if(det_aruco_list):
    #     img1 = mark_Aruco(n_frame,det_aruco_list)
    #     robot_state = calculate_Robot_State(img1,det_aruco_list)

    frame=cv2.flip(n_frame,1)
    #gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)

    
    det_aruco_list = detect_Aruco(frame)
    if(det_aruco_list):
        img1 = mark_Aruco(frame,det_aruco_list)
        robot_state = calculate_Robot_State(img1,det_aruco_list)

    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([28,89,102])
    upper_orange= np.array([63,210,161])
    mask=cv2.inRange(hsv,lower_orange,upper_orange)
    result=cv2.bitwise_and(frame,frame,mask=mask)
    gray_frame = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)
    #mask_check =cv2.inRange(hsv, lower, uper)
    
    circles =cv2.HoughCircles(blur_frame, cv2.HOUGH_GRADIENT, 1,100,
                             param1=100, param2=25,minRadius=0, maxRadius=0)
    
    if circles is not None:
        circles= np.uint32(np.around(circles))
        chosen= None
        for i in circles[0,:]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                   chosen=i
        cv2.circle(frame,(chosen[0],chosen[1]),1,(0,100,100),3) 
        cv2.circle(frame,(chosen[0],chosen[1]),chosen[2],(0,255,0),3)
        #print(chosen)
        text='('+str(chosen[0])+', '+str(chosen[1])+')'
        frame = cv2.putText(frame, 
                            text, 
                            (chosen[0]-70,chosen[1]-70),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1,
                            color = (255, 0, 0), 
                            thickness = 2, 
                            lineType=cv2.LINE_4)
        prevCircle=chosen
    cv2.imshow('circle',frame)
    cv2.imshow('blur',blur_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()