import cv2
import numpy as np
import cv2.aruco as aruco
from aruco_lib import *
from transform import four_point_transform
from transform import order_points
from skimage.filters import threshold_local
import argparse
import imutils
import time
import socket
import threading
from time import sleep

clientlst =[]
SeverIP = "10.128.49.126"                     #Computer IP
SeverPort = 20001                         #Sever port or this computer port
bufferSize = 1024                         #Maximum buffer size
msgFromSever = "Hello UDP client"
bytesToSend1 = str.encode(msgFromSever)

#Create a datagram socket (UDP)
UDPSeverSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

#Bind to address and ip
UDPSeverSocket.bind((SeverIP, SeverPort))
print("UDP sever up and listening")

bytesAddressPair = UDPSeverSocket.recvfrom(bufferSize)  #waiting here until receiving
message = bytesAddressPair[0].decode('utf-8')
address = bytesAddressPair[1]

print(address)
print(message)

#send to that client
# UDPSeverSocket.sendto(bytesToSend1, address)

def ReceiveThread():
    while True:
        bytesAddressPair = UDPSeverSocket.recvfrom(bufferSize)  #waiting here until receiving
        message = bytesAddressPair[0].decode('utf-8')
        msg = 'robot coordinates : ('+str(robot_state_parameter[0])+','+str(robot_state_parameter[1])+','+str(robot_state_parameter[2])+')\nBall coordinates: ('+str(ball_coordinate[0])+', '+str(ball_coordinate[1])+')'
        address = bytesAddressPair[1]
        bytesToSend = str.encode(msg)
        UDPSeverSocket.sendto(bytesToSend,address)
        
        print(address)
        print(message)

        #send to that client
        #UDPSeverSocket.sendto(bytesToSend, address)

# #Listen for incoming datagrams
# thread = threading.Thread(target = ReceiveThread, args = ())
# thread.start()

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
#cv2.imshow("Image", image)
cv2.imshow("Edged", edged)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
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
tl = rect[0]
print(tl)
bl = rect[3]
origin = (tl+bl)/2
print(origin)
print(origin[0])
dis = ((rect[1][1]-rect[0][1])**2+(rect[1][0]-rect[0][0])**2)**0.5
ratio_ppc = dis/91
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
# cap.set(cv2.CAP_PROP_FPS, 100)
# cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

det_aruco_list = {}
print("STEP 3: Apply perspective transform")

while True:
    ret,n_frame = cap.read()

    frame=cv2.flip(n_frame,1)

    det_aruco_list = detect_Aruco(frame)
    if(det_aruco_list):
        origin = (tl+bl)/2
        ratio_ppc = dis/91
        img1 = mark_Aruco(frame,det_aruco_list,origin,ratio_ppc)
        robot_state = calculate_Robot_State(img1,det_aruco_list)
        robot_state_coordinate = mark_Aruco_parameter(frame,det_aruco_list,origin,ratio_ppc)
        robot_state_angle = calculate_Robot_State_angle(img1,det_aruco_list)
        robot_state_parameter = (robot_state_coordinate[0],-robot_state_coordinate[1],robot_state_angle)
        print('robot state parameter:')
        print('x : ',robot_state_parameter[0])
        print('y : ',-robot_state_parameter[1])
        print('angle : ',robot_state_parameter[2])

    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_orange= np.array([23,85,80])
    upper_orange= np.array([33,255,255])
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
        ball_coordinate = (round((chosen[0]-origin[0])/ratio_ppc,2),round((origin[1]-chosen[1])/ratio_ppc,2))
        text='('+str(ball_coordinate[0])+', '+str(ball_coordinate[1])+')'
        frame = cv2.putText(frame, 
                            text, 
                            (chosen[0]-70,chosen[1]-70),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1,
                            color = (255, 0, 0), 
                            thickness = 2, 
                            lineType=cv2.LINE_4)
        prevCircle=chosen
        print('ball coordinate:')
        print('x:',ball_coordinate[0])
        print('y:',ball_coordinate[1])

    cv2.imshow('circle',frame)
    cv2.imshow('blur',blur_frame)
    #cv2.imshow("Original", imutils.resize(orig, height = 650))
    #cv2.imshow("Scanned", imutils.resize(warped, height = 650))
    #cv2.imshow("Scanned", warped)
    
    thread = threading.Thread(target = ReceiveThread, args = ())
    thread.start()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()