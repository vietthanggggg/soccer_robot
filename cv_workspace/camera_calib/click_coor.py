# importing the module
import cv2
import numpy as np

CM_TO_PIXEL = 80 / 610
CM_TO_PIXEL_2 =100/ 793

CM_2_PIXEL=(CM_TO_PIXEL+CM_TO_PIXEL_2)/2
print(CM_TO_PIXEL)
print(CM_TO_PIXEL_2)

# function to display the coordinates of
# of the points clicked on the image

#resized
scale_percent = 60 # percent of original size

def click_event(event, x, y, flags, params):

   # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
         x_cm = round(x * CM_2_PIXEL,2)
         y_cm = round(y * CM_2_PIXEL-40,2)
         # displaying the coordinates
         # on the Shellq
         print(x_cm, ' ', y_cm)
   
         # displaying the coordinates
         # on the image window
         font = cv2.FONT_HERSHEY_SIMPLEX
         cv2.circle(img,(x,y), 5, (0, 0, 255), -1)
         cv2.putText(img, str(x_cm) + ',' +str(y_cm), (x,y), font,1, (255, 0, 0), 2)
         cv2.imshow('image', img)
         
# driver function
if __name__=="__main__":

# reading the image
  img = cv2.imread('D:\BK-DOCS\Luan Van\lv_workspace\empty_field\crop_field.jpg', 1)
  width = int(img.shape[1] * scale_percent / 100)
  height = int(img.shape[0] * scale_percent / 100)
  dim = (width, height)
  
# resize image
  img=cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# setting mouse handler for the image
# and calling the click_event() function
  cv2.setMouseCallback('image', click_event)

# wait for a key to be pressed to exit
  cv2.waitKey(0)

 # close the window
  cv2.destroyAllWindows()
print('Original Dimensions : ',img.shape)