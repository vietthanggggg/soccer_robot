import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse
from tkinter import *
import cv2
import numpy as np
 
class App:
    def __init__(self, window, window_title,window_icon,video_source=0):
        self.window = window
        self.window.title(window_title)
        #self.window.geometry=geometry
        self.ok=False
        self.window.iconbitmap(window_icon)
        self.video_source = video_source
        #self.window_icon=Image(self)
        #self.color = ChangeColor(self.window)
        #self.calibration = Calibration(self.window)
 
        #timer
        self.timer=ElapsedTimeClock(self.window)
 
        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)
 
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height,background = 'white')
        self.canvas.pack(side = tk.RIGHT)
 
        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", command=self.snapshot,bg = "yellow",fg="black",width=30)
        self.btn_snapshot.pack(side=tk.TOP)
 
        #video control buttons
 
        self.btn_start=tk.Button(window, text='START', command=self.open_camera,bg = "yellow",fg="black",width=30)
        self.btn_start.pack(side=tk.TOP)
 
        self.btn_stop=tk.Button(window, text='STOP', command=self.close_camera,bg = "yellow",fg="black",width=30)
        self.btn_stop.pack(side=tk.TOP)
 
        #change color button
        self.btn_calibration=tk.Button(window, text="Calibration", command=self.calibration_camera,bg = "yellow",fg="black",width=30)
        self.btn_calibration.pack(side=tk.TOP)

        # quit button
        self.btn_quit=tk.Button(window, text='QUIT', command=quit,bg = "yellow",fg="black",width=30)
        self.btn_quit.pack(side=tk.TOP)
 
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=10
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()
 
        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
 
    def open_camera(self):
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")
 
    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")

    
    def calibration_camera(self):
        cv2.namedWindow('Track')
        cv2.resizeWindow('Track', 500,350)
        self.vid.calibration()
    
      
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
 
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)
 
 
class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Command Line Parser
        args=CommandLineParser().args
 
        
        #create videowriter
 
        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
 
        self.fourcc=VIDEO_TYPE[args.type[0]]
 
        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)
 
        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])
 
        # Get video source width and height
        self.width,self.height=res
 

    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()
    
    def calibration(self):
        #self.title('Calibration')
        #self.resizeWindow('Calibration', 500,350)
        def track(self):
         pass
        cv2.namedWindow('Track')
        cv2.resizeWindow('Track', 500,350)
        cv2.createTrackbar('hue min','Track',0,179, track)
        cv2.createTrackbar('hue max','Track',179,179, track)
        cv2.createTrackbar('sat min','Track',0,255, track)
        cv2.createTrackbar('sat max','Track',255,255, track)
        cv2.createTrackbar('val min','Track',0,255, track)
        cv2.createTrackbar('val max','Track',255,255, track)
        while True:
            #webcam
            _,frame =self.vid.read()
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
            mask=(cv2.inRange(hsv_frame, lower, uper))
    
            cv2.imshow('mask',mask)
            #cv2.imshow('frame',frame)
    
            if cv2.waitKey(1) & 0xFF ==ord('q'):
                break


class ElapsedTimeClock:
    def __init__(self,window):
        self.T=tk.Label(window,text='00:00:00',font=('times', 20, 'bold'), bg='black',fg='green')
        #self.T.pack(fill=tk.BOTH, expand=1)
        self.elapsedTime=dt.datetime(1,1,1)
        self.running=0
        self.lastTime=''
        t = time.localtime()
        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
        # self.tick()

    # def features(self):
    #     self.stopwatch_label = tk.label(self,text='00:00:00')

    def tick(self):
        # get the current local time from the PC
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.updwin=self.T.after(100, self.tick)


    def start(self):
            if not self.running:
                self.zeroTime=dt.datetime(1, 1, 1).now()-self.elapsedTime
                self.tick()
                self.running=1

    def stop(self):
            if self.running:
                self.T.after_cancel(self.updwin)
                self.elapsedTime=dt.datetime(1, 1, 1).now()-self.zeroTime
                self.time2=self.elapsedTime
                self.running=0

class CommandLineParser:
    
    def __init__(self):

        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['mp4'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()




def main():
    # Create a window and pass it to the Application object
    App(tk.Tk(),'Soccer robot',r'C:\Users\AD\Pictures\favicon.ico')

main()