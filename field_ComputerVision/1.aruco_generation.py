import numpy as np
import cv2
import cv2.aruco as aruco
 
 
'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
 
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100) #creating aruco dictionary...250 markers and a marker size of 6x6 bits
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
img = aruco.drawMarker(aruco_dict, 0, 500) # 2-- marker id, as the chose dictionary is upto 250...so the id no ranges from 0 to 249....and 700x700 is the pixel 
img = cv2.flip(img,1)
print(img.shape)
cv2.imwrite("C://Users//AD//Documents//Thesis//computer_vision//ArUco_marker_detection//Aruco_id//test_marker11_big.jpg", img)
print(img.shape)
cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()