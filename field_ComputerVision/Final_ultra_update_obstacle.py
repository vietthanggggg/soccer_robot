import cv2
import numpy as np
import cv2.aruco as aruco
from aruco_lib import *
from transform import four_point_transform
from transform import order_points
from skimage.filters import threshold_local
import argparse
import imutils
import json
#import math

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image1 = cv2.imread(args["image"])
image = cv2.flip(image1,1)
# image = cv2.imread('path')
ratio = image.shape[0]/500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)


# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]   #Sort the contours by area and keep only the largest ones
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
rect = order_points(screenCnt.reshape(4, 2) * ratio)

#Calibrate coordinate
tl = rect[0]
print(tl)
bl = rect[3]
tr = rect[1]
br = rect[2]
origin = (tl+bl)/2
print(origin)
dis_1 = ((rect[1][1]-rect[0][1])**2+(rect[1][0]-rect[0][0])**2)**0.5
dis_2 = ((rect[3][1]-rect[2][1])**2+(rect[3][0]-rect[2][0])**2)**0.5
dis = (dis_1+dis_2)/2
ratio_ppc = dis/90

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255
# show the original and scanned images

cap = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

det_aruco_list = {}
print("STEP 3: Apply perspective transform")

while True:
    ret,n_frame = cap.read()

    frame=cv2.flip(n_frame,1)

    
    det_aruco_list = detect_Aruco(frame)
    if(det_aruco_list[0]):
        origin = (tl+bl)/2
        ratio_ppc = dis/90
        img1 = mark_Aruco(frame,det_aruco_list[0],origin,ratio_ppc)
        robot_state = calculate_Robot_State(img1,det_aruco_list[0])
        robot_state_coordinate = mark_Aruco_parameter(frame,det_aruco_list[0],origin,ratio_ppc)
        robot_state_angle = calculate_Robot_State_angle(img1,det_aruco_list[0])
        robot_state_parameter = (robot_state_coordinate[0],robot_state_coordinate[1],robot_state_angle)    #Robot coordinates (x,y,angle)
    
    if(det_aruco_list[1]):
        origin = (tl+bl)/2
        ratio_ppc = dis/90
        img1 = mark_Aruco(frame,det_aruco_list[1],origin,ratio_ppc)
        obstacle_state = calculate_Robot_State(img1,det_aruco_list[1])
        obstacle_state_coordinate = mark_Aruco_parameter(frame,det_aruco_list[1],origin,ratio_ppc)
        obstacle_state_angle = calculate_Robot_State_angle(img1,det_aruco_list[1])
        obstacle_state_parameter = (obstacle_state_coordinate[0],obstacle_state_coordinate[1],obstacle_state_angle)    #Robot coordinates (x,y,angle)
    
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([21,100,139])                 #BK
    upper_orange= np.array([31,171,241])                 #BK
    # lower_orange= np.array([20,36,103])                 #KTX
    # upper_orange= np.array([35,255,255])                 #KTX
    mask=cv2.inRange(hsv,lower_orange,upper_orange)
    result=cv2.bitwise_and(frame,frame,mask=mask)
    gray_frame = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame,(17,17),0)

    cv2.circle(frame,(int(origin[0]),int(origin[1])),1,(255,0,0),-3)                                      #Origin
    cv2.circle(frame,(int(origin[0]+90*ratio_ppc),int(origin[1])),1,(255,0,0),-3)                        #Center of goal
    
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
        ball_coordinate = (round((chosen[0]-origin[0])/ratio_ppc,2),round((origin[1]-chosen[1])/ratio_ppc,2))  
        text='('+str(ball_coordinate[0])+', '+str(ball_coordinate[1])+')'
        frame = cv2.putText(frame, 
                            text, 
                            (chosen[0]+70,chosen[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1,
                            color = (255, 0, 0), 
                            thickness = 2, 
                            lineType=cv2.LINE_4)
        prevCircle=chosen
        #lineFromCenterGoalToBall = cv2.line(frame,(int(origin[0]+90*ratio_ppc),int(origin[1])),(chosen[0],chosen[1]),(50,156,100),2)   #Line from center of goal to ball
        #len = math.sqrt(math.pow(origin[0]+90*ratio_ppc-chosen[0],2.0)+math.pow(chosen[1],2.0))
        #takeDistance = (int(origin[0]+90*ratio_ppc+(origin[0]+90*ratio_ppc-chosen[0])/len*200),int(origin[1]+(origin[1]+chosen[1])/len*200))
        #cv2.line(frame,(chosen[0],chosen[1]),(takeDistance[0],takeDistance[1]),(200,50,100),2)
        #cv2.circle(frame,(takeDistance[0],takeDistance[1]),1,[100,25,30],3)
        #cv2.line(frame,(int(origin[0]+90*ratio_ppc),int(origin[1])),(chosen[0],chosen[1]),(50,156,100),2)
    
    #obstacle
    #ball
    ox, oy = [], []
    for i in range(int(ball_coordinate[0]-7*ratio_ppc), int(ball_coordinate[0]+7*ratio_ppc)):
        ox.append(i)
        oy.append(int(ball_coordinate[1]-7*ratio_ppc))
    for i in range(int(ball_coordinate[1]-7*ratio_ppc),int(ball_coordinate[1]+7*ratio_ppc)):
        ox.append(int(ball_coordinate[0]+7*ratio_ppc))
        oy.append(i)
    for i in range(int(ball_coordinate[0]-7*ratio_ppc),int(ball_coordinate[0]+7*ratio_ppc)):
        ox.append(i)
        oy.append(int(ball_coordinate[0]+7*ratio_ppc))
    for i in range(int(ball_coordinate[1]-7*ratio_ppc),int(ball_coordinate[1]+7*ratio_ppc)):
        ox.append(int(ball_coordinate[0]-7*ratio_ppc))
        oy.append(i)
    
    #enemies
    for i in range(int(obstacle_state_coordinate[0]-10*ratio_ppc), int(obstacle_state_coordinate[0]+10*ratio_ppc)):
        ox.append(i)
        oy.append(int(obstacle_state_coordinate[1]-10*ratio_ppc))
    for i in range(int(obstacle_state_coordinate[1]-10*ratio_ppc), int(obstacle_state_coordinate[1]+10*ratio_ppc)):
        ox.append(int(obstacle_state_coordinate[0]+10*ratio_ppc))
        oy.append(i)
    for i in range(int(obstacle_state_coordinate[0]-10*ratio_ppc), int(obstacle_state_coordinate[0]+10*ratio_ppc)):
        ox.append(i)
        oy.append(int(obstacle_state_coordinate[0]+10*ratio_ppc))
    for i in range(int(obstacle_state_coordinate[1]-10*ratio_ppc),int(obstacle_state_coordinate[1]+10*ratio_ppc)):
        ox.append(int(obstacle_state_coordinate[0]-10*ratio_ppc))
        oy.append(i)
    
    #field
    for i in range(int(tl[0]), int(tr[0])):
        ox.append(i)
        oy.append(int(tl[1]))
    for i in range(int(bl[1]), int(tl[1])):
        ox.append(int(bl[0]))
        oy.append(i)
    for i in range(int(br[1]), int(tr[1])):
        ox.append(int(br[0]))
        oy.append(i)
    for i in range(int(bl[0]),int(br[0])):
        ox.append(i)
        oy.append(int(bl[1]))

    cv2.imshow('circle',frame)
    cv2.imshow('blur',blur_frame)
    cv2.imshow("Scanned", warped)

    if cv2.waitKey(1) & 0xFF == ord('s'):

        # Data to be written
        dictionary = {
            "name": "sathiyajith",
            "rollno": 56,
            "cgpa": 8.6,
            "phonenumber": "9976770500"
        }
 
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
 
        # Writing to sample.json
        with open("data.json", "w") as outfile:
            outfile.write(json_object)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()