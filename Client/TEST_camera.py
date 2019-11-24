import cv2
import random
import time
from time import gmtime, strftime, localtime
import datetime
import requests
import base64
import picamera
import RPi.GPIO as GPIO

from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
signal(SIGPIPE, SIG_IGN)
import os
class Camera():
    def __init__(self, width, height, storepath):
        
        self.cap = picamera.PiCamera()
        self.cap.resolution = (width, height)
        self.curImg = None
       
        self.cap.framerate = 60
        self.cap.meter_mode = 'average'
        self.cap.shutter_speed = 15000
        self.cap.sharpness = 50
        self.cap.exposure_mode = 'off'
        self.cap.iso = 60
        
        
        if not os.path.exists(storepath):
            os.mkdir(storepath)
        self.storePath = storepath
        
    def Shot(self):
        
        
        filename = strftime("%Y-%m-%d-%T", localtime())+'.jpg'
        self.cap.start_preview()
        time.sleep(1)

        self.cap.capture(self.storePath + filename)
        self.curImg = cv2.imread(self.storePath + filename)
        '''
        r = requests.get('http://140.137.132.172:2004/cur_shot')
        data = r.json() # Check the JSON Response Content documentation below
        img_name = self.storePath + strftime("%Y-%m-%d-%T", localtime())+'.jpg'
        with open(img_name, 'wb') as output:
            output.write(base64.b64decode(data['image']))
        self.curImg = cv2.imread(img_name)
        '''
        return self.curImg

    def ShowCurImage(self):
        cv2.imshow('showCurFrame',self.curImg)
        cv2.waitKey(0)

    

if __name__ == "__main__":
    
    c = Camera(608,608,'./imageLog/mixing/')
    c.Shot()