import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math

'''
functions in this file:
* angle_calculate(pt1,pt2, trigger = 0) - function to return angle between two points
* detect_Aruco(img) - returns the detected aruco list dictionary with id: corners
* mark_Aruco(img, aruco_list) - function to mark the centre and display the id
* calculate_Robot_State(img,aruco_list) - gives the state of the bot (centre(x), centre(y), angle)
'''

def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
    angle_list_1 = list(range(359,0,-1))
    
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]
    angle = int(math.degrees(math.atan2(y,x)))
    angle_float = round(math.degrees(math.atan2(y,x)),2) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    
    angle = "%.2f" % angle
    return angle

def detect_Aruco(img):  #returns the detected aruco list dictionary with id: corners
    aruco_list = {}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)   #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
    parameters = aruco.DetectorParameters_create()  #refer opencv page for clarification
    #lists of ids and the corners beloning to each id
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    #corners is the list of corners(numpy array) of the detected markers. For each marker, its four corners are returned in their original order (which is clockwise starting with top left). So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
    # print corners[0]
    #gray = aruco.drawDetectedMarkers(gray, corners,ids)
    #cv2.imshow('frame',gray)
    #print (type(corners[0]))
    if len(corners):    #returns no of arucos
        #print (len(corners))
        #print (len(ids))
        #print (type(corners))
        #print (corners[0][0])
        for k in range(len(corners)):
            temp_1 = corners[k]
            temp_1 = temp_1[0]
            temp_2 = ids[k]
            temp_2 = temp_2[0]
            aruco_list[temp_2] = temp_1
        return aruco_list


def mark_Aruco(img, aruco_list,origin,ratio_ppc):    #function to mark the centre and display the id
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry is a numpy array with shape (4,2)
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#so being numpy array, addition is not list addition
        centre[:] = [int(x / 4) for x in centre]    #finding the centre
        orient_centre = centre + [0.0,5.0]
        centre = tuple(centre)  
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        centre_calibrate = (round((centre[0]-origin[0])/ratio_ppc,2),round((origin[1]-centre[1])/ratio_ppc,2))
        if key == 0:
            cv2.putText(img,'('+str(centre_calibrate[0])+','+str(centre_calibrate[1])+')', (int(centre[0]+30), int(centre[1])), font, 1, (255,128,0), 2, cv2.LINE_AA)# displaying the idno
            cv2.putText(img,'Messi',(int(centre[0]+30), int(centre[1])-40),font, 1, (255,128,0), 2, cv2.LINE_AA)
            cv2.line(img,(int(centre[0]),int(centre[1])),(int(orient_centre[0]),int(orient_centre[1])),(255,128,0),4)
            cv2.putText(img, 'id'+str(key)+':Messi', (10,450), font, 1, (255,128,0), 2, cv2.LINE_AA)
            cv2.circle(img,(int(centre[0]),int(centre[1])),1,(255,128,0),8)
        elif key ==1:
            cv2.putText(img,'('+str(centre_calibrate[0])+','+str(centre_calibrate[1])+')', (int(centre[0]+30), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)# displaying the idno
            cv2.putText(img,'Enemy',(int(centre[0]+30), int(centre[1])-40),font, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(img, 'id'+str(key)+':Enemy', (10,500), font, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.circle(img,(int(centre[0]),int(centre[1])),1,(0,0,255),8)
    return img


def mark_Aruco_parameter(img, aruco_list,origin,ratio_ppc):    #function to mark the centre and display the id
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry is a numpy array with shape (4,2)
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#so being numpy array, addition is not list addition
        centre[:] = [int(x / 4) for x in centre]    #finding the centre
        #print centre
        orient_centre = centre + [0.0,5.0]
        #print orient_centre
        centre = tuple(centre)  
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        #print centre
        #print orient_centre
        cv2.circle(img,(int(centre[0]),int(centre[1])),1,(0,0,255),8)
        #cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
        #cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
        #cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
        #cv2.circle(img,orient_centre,1,(0,0,255),8)
        cv2.line(img,(int(centre[0]),int(centre[1])),(int(orient_centre[0]),int(orient_centre[1])),(255,0,0),4) #marking the centre of aruco
        #cv2.line(img,centre,orient_centre,(255,0,0),4)
        cv2.putText(img, 'id:'+str(key), (10,450), font, 1, (255,128,0), 2, cv2.LINE_AA)
        centre_calibrate = (round((centre[0]-origin[0])/ratio_ppc,2),round((origin[1]-centre[1])/ratio_ppc,2))
        #cv2.putText(img,'('+str(centre_calibrate[0])+','+str(centre_calibrate[1])+')', (int(centre[0]+30), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)# displaying the idno
    return centre_calibrate

def calculate_Robot_State(img,aruco_list,origin,ratio_ppc):  #gives the state of the bot (centre(x), centre(y), angle)
    robot_state = {}
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for key in key_list:
        dict_entry = aruco_list[key]
        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
        centre[:] = [int(x / 4) for x in centre]
        centre = tuple(centre)
        #print centre
        angle = angle_calculate(pt1, pt2)
        angle_show = int(float(angle))
        if key == 0:
            cv2.putText(img, str(angle_show), (int(centre[0] - 80), int(centre[1])), font, 1, (255,128,0), 2, cv2.LINE_AA)
        x_robot = (centre[0]-origin[0])/ratio_ppc
        y_robot = (origin[1]-centre[1])/ratio_ppc
        x_robot = "%.2f" % x_robot
        y_robot = "%.2f" % y_robot

        robot_state[key]=(x_robot,y_robot,angle)
    #HOWEVER IF YOU ARE SCALING IMAGE AND ALL...THEN BETTER INVERT X AND Y...COZ THEN ONLY THE RATIO BECOMES SAME
    return robot_state
 

def calculate_Robot_State_angle(img,aruco_list):  #gives the state of the bot (centre(x), centre(y), angle)
    robot_state = {}
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for key in key_list:
        dict_entry = aruco_list[key]
        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
        centre[:] = [int(x / 4) for x in centre]
        centre = tuple(centre)
        #print centre
        angle = round(angle_calculate(pt1, pt2),2)
        cv2.putText(img, str(angle), (int(centre[0] - 80), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
        robot_state[key] = (round(centre[0],2), round(centre[1],2), angle)#HOWEVER IF YOU ARE SCALING IMAGE AND ALL...THEN BETTER INVERT X AND Y...COZ THEN ONLY THE RATIO BECOMES SAME
        robot_state_parameter = (round(centre[0],2), round(centre[1],2), angle)

    return robot_state_parameter[2]