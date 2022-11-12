import cv2
import numpy as np

#create a window
cv2.namedWindow('Track')
cv2.resizeWindow('Track', 500,350)


cap= cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#cv2.imshow('original',img)

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
    #webcam
    _,frame =cap.read()
    hsv_frame =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    h_min =cv2.getTrackbarPos('hue min','Track')
    h_max =cv2.getTrackbarPos('hue max','Track')
    s_min =cv2.getTrackbarPos('sat min','Track')
    s_max =cv2.getTrackbarPos('sat max','Track')
    val_min =cv2.getTrackbarPos('val min','Track')
    val_max =cv2.getTrackbarPos('val max','Track')
    #print(f'HUE MIN: {h_min} HUE MAX: {h_max} SAT MIN: {s_min} SAT MAX: {s_max} VAL MIN: {val_min} VAL MAX: {val_max} ')
    
    #mask
    lower =np.array([h_min, s_min, val_min])
    uper =np.array([h_max, s_max, val_max])
    mask =cv2.inRange(hsv_frame, lower, uper)
    
    cv2.imshow('Mask',mask)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break