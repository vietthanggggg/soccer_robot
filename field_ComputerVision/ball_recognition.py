import cv2
import numpy as np

cap = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def ball_coordinate(frame,origin,ratio_ppc):
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([20,83,110])
    upper_orange= np.array([52,221,245])
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
        ball_coordinate = (round((chosen[0]-origin[0])/ratio_ppc,2),round((chosen[1]-origin[1])/ratio_ppc,2))
        return ball_coordinate

while True:
    ret, n_frame = cap.read()
    frame=cv2.flip(n_frame,1)
    #gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([25,26,153])
    upper_orange= np.array([34,96,255])
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
        text='('+str(int((chosen[0]-300)/37.8))+', '+str( int((chosen[1]-200)/37.8))+')'
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