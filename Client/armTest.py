import socket
import cv2
import traceback
import camera
import random
import time
import base64
import numpy as np
import sys
import time
from time import sleep
sys.path.insert(0,'/home/pi/uArm-Python-SDK-2.0')
from uarm.wrapper import SwiftAPI  # 取得uarm函數庫
import RPi.GPIO as GPIO # 設定繼電器的開關
import json
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
signal(SIGPIPE, SIG_IGN)
from camera import *
class set_arm_control():
    def __init__(self,RELAY_PIN=12):
        self.arm = SwiftAPI()
        self.arm.get_power_status()
        self.RELAY_PIN = RELAY_PIN
        self.arm.reset()
    #機械手臂進行初始化動作
    def set_arm_origin(self):
        self.arm.waiting_ready()
        self.arm.set_position(200, 0, 170, speed=100000)
    # 機械手臂設定(x, y, z)座標移動
    def set_arm_move(self, x, y, z):
        self.arm.set_position(x, y, z, speed=100000)
    # 機械手臂切斷連線
    def arm_disconnect(self):
        self.arm.disconnect() 
    def get_position(self):
        print(self.arm.get_position())
    #初始設定繼電器
    def origin_pump(self):
        GPIO.setmode(GPIO.BOARD)  # 指定模式BOARD 啟用RPi板子相對應之腳位編號
        GPIO.setwarnings(False)  # 避免出現警告
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)  # 設定pin腳為輸出
    #打開幫浦=開啟繼電器(使電流流通)
    def start_pump(self):
        GPIO.output(self.RELAY_PIN, 0)
    #關閉幫浦=關閉繼電器(使電流不能流通)
    def close_pump(self):
        GPIO.output(self.RELAY_PIN, 1)

arm = set_arm_control()
arm.set_arm_origin()  # 機械手臂移動到初始位置

data_dic =  {'0': [530,430], '1': [250,145], '2':[300,600], '3':[455,200]}
#

if len(data_dic)==0:
    print("don't have defect bean")
else:
    for i in range(0,len(data_dic)):

        #轉換真實空間位置
        Bean_information_image_width = 608
        Bean_information_image_hight = 608
        inch_to_mm = 25.4
        x_dpi =155
        y_dpi =155

        pixel_arm_y=Bean_information_image_width/2
        pixel_arm_x=Bean_information_image_hight/2
        print(i)
                
        x_str = data_dic[str(i)][0]
        #print(x_str)
        y_str = data_dic[str(i)][1]
        print("yolo_center")
        print(x_str,y_str)
                #print(y_str)
#                DistancePixel_arm_bean_x=abs(pixel_arm_x-float(x_str))
#                DistancePixel_arm_bean_y=abs(pixel_arm_y-float(y_str))
#                DistancePixel_arm_bean_x=pixel_arm_x-float(x_str)
#                DistancePixel_arm_bean_y=pixel_arm_y-float(y_str)
        DistancePixel_arm_bean_x=float(x_str)-pixel_arm_x
        DistancePixel_arm_bean_y=float(y_str)-pixel_arm_y
        print("arm_bean_pixel")
        print(DistancePixel_arm_bean_x,DistancePixel_arm_bean_y)
                
        real_distance_x_cm =  DistancePixel_arm_bean_x*inch_to_mm/x_dpi
        real_distance_y_cm =  DistancePixel_arm_bean_y*inch_to_mm/y_dpi
        print("real_distance")
        print(real_distance_x_cm,real_distance_y_cm)
#                if(real_distance_x_cm*real_distance_y_cm>0):
#                    real_distance_x_cm*=-1
#                    real_distance_y_cm*=-1
                    
        x=200-real_distance_y_cm
        y=0-real_distance_x_cm
        print(x)
        print(y)
                
        move_x=round(x,2)
        move_y=round(y,2)
                # 機械手臂移動至瑕疵豆的上方位置
                
        arm.set_arm_move(move_x, move_y, 170)
        sleep(3)
        arm.get_position()
                
        print("move:",move_x,move_y)

        # 補償吸嘴與相機的差距(x+50,y-2.5)
        x_s = float(move_x) + 50
        y_s = float(move_y) - 7.5
                 
        x_s=round(x_s,2)
        y_s=round(y_s,2)
        y_overset = float(y_s) + 5
            
        arm.set_arm_move(x_s, y_s, 30)
        sleep(3)
        arm.set_arm_move(x_s, y_overset, 30)
        sleep(3)
        print("move:",x_s, y_overset)
                
        arm.get_position()
 
        # 啟動幫浦
        arm.origin_pump()
        arm.start_pump()
        sleep(2)
        # 吸取瑕疵豆
        arm.set_arm_move(x_s, y_overset, 0)
        sleep(9)
        # 移動機械手臂移除瑕疵豆
        arm.set_arm_move(x_s, y_overset, 150)
        sleep(2)
        arm.set_arm_move(150, 180, 150)
        sleep(2)

        #CLOSE幫浦
        arm.close_pump()
        sleep(3)

        arm.set_arm_origin()  # 機械手臂移動到初始位置
#
        sleep(2)

        #data = site.pop(i)
        print("finish catch defect bean")  