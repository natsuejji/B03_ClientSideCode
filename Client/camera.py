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
    def __init__(self, storepath):
        if not os.path.exists(storepath):
            os.mkdir(storepath)
        self.storePath = storepath
    def Shot(self):

        r = requests.get('http://140.137.132.172:2004/cur_shot')
        data = r.json() # Check the JSON Response Content documentation below
        img_name = self.storePath + strftime("%Y-%m-%d-%T", localtime())+'.jpg'
        with open(img_name, 'wb') as output:
            output.write(base64.b64decode(data['image']))
        self.curImg = cv2.imread(img_name)
        
        return self.curImg


if __name__ == "__main__":
    
    c = Camera(608,608,'./imageLog/')
    c.Shot()