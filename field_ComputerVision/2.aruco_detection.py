import numpy as np
import cv2
import cv2.aruco as aruco
from aruco_lib import *
import time

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

det_aruco_list = {}
def aruco_paramter(frame):
	det_aruco_list = detect_Aruco(frame)
	if(det_aruco_list):
		img = mark_Aruco(frame,det_aruco_list)
		robot_state = calculate_Robot_State(img,det_aruco_list)
	robot_state_parameter = calculate_Robot_State_parameter(frame,det_aruco_list)
	return robot_state_parameter

while (True):
	ret,frame = cap.read()
	det_aruco_list = detect_Aruco(frame)
	if(det_aruco_list):
		img = mark_Aruco(frame,det_aruco_list)
		robot_state = calculate_Robot_State(img,det_aruco_list)
	robot_state_parameter = calculate_Robot_State_parameter(frame,det_aruco_list)
	print('x : ',robot_state_parameter[0])
	print('y : ',robot_state_parameter[1])
	print('angle : ',robot_state_parameter[2])
		
	cv2.imshow('image',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
