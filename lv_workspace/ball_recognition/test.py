from unittest import result
import cv2
import numpy as np

np.seterr(over='ignore')

cap = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2
#create a window
cv2.namedWindow('Track')
cv2.resizeWindow('Track', 500,320)
#trackbar
def track(x):
    pass

cv2.createTrackbar('hue min','Track',0,179, track)
cv2.createTrackbar('hue max','Track',179,179, track)
cv2.createTrackbar('sat min','Track',0,255, track)
cv2.createTrackbar('sat max','Track',255,255, track)
cv2.createTrackbar('val min','Track',0,255, track)
cv2.createTrackbar('val max','Track',255,255, track)

while True:
    h_min =cv2.getTrackbarPos('hue min','Track')
    h_max =cv2.getTrackbarPos('hue max','Track')
    s_min =cv2.getTrackbarPos('sat min','Track')
    s_max =cv2.getTrackbarPos('sat max','Track')
    val_min =cv2.getTrackbarPos('val min','Track')
    val_max =cv2.getTrackbarPos('val max','Track')
    
    lower =np.array([h_min, s_min, val_min])
    uper =np.array([h_max, s_max, val_max])
    
    
    ret, n_frame = cap.read()
    frame=cv2.flip(n_frame,1)
    #gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([h_min, s_min, val_min])
    upper_orange= np.array([h_max, s_max, val_max])
    mask=cv2.inRange(hsv,lower_orange,upper_orange)
    result=cv2.bitwise_and(frame,frame,mask=mask)
    gray_frame = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)
    mask_check =cv2.inRange(hsv, lower, uper)
    
    circles =cv2.HoughCircles(blur_frame, cv2.HOUGH_GRADIENT, 1,100,
                             param1=100, param2=50,minRadius=0, maxRadius=0)
    
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
        text='('+str(chosen[0])+', '+str( chosen[1])+')'
        frame = cv2.putText(frame, 
                            text, 
                            (chosen[0]-20,chosen[1]-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1,
                            color = (255, 0, 0), 
                            thickness = 2, 
                            lineType=cv2.LINE_4)
        prevCircle=chosen
        
    cv2.imshow('circle',frame)
    #cv2.imshow('frame',result)
    cv2.imshow('Mask',mask_check)
    #cv2.imshow('a',blur_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()