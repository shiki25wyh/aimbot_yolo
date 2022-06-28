import cv2
import numpy as np
from mss import mss
import pyautogui
# PyTorch Hub
import torch
import random
import keyboard
import pygetwindow

import pydirectinput
pyautogui.FAILSAFE = False
import time
# Model
model = torch.hub.load('.', 'custom', path='exp17/best.pt', source='local')
game = pygetwindow.getWindowsWithTitle('Counter-Strike: Global Offensive - Direct3D 9')[0]
y1,x1 = game.topleft
scwidth = game.width
scheight = game.height
# x1=0
# y1=0
# width = 1000
# height = 640

bounding_box = {'top': x1, 'left': y1, 'width': scwidth, 'height': scheight}

with mss() as sct:
    while True:
            sct_img = sct.grab(bounding_box)
            scr_img = np.array(sct_img)

            # cv2.imshow('screen', scr_img) # display screen in box
            results = model(scr_img)
            # print(results.xyxy)
            cv2.imshow('Testing', np.squeeze(results.render()))
            coor = results.xyxy[0].tolist()
            # print(coor)
            if len(coor)>0:
                if coor[0][4]>0.3:
                    if coor[0][5] == 0:
                        x = int(coor[0][2])
                        y = int(coor[0][3])
                        width = int(coor[0][2]-coor[0][0])
                        height = int(coor[0][3]-coor[0][1])
                        xpos = int(((x-(width/2))-pydirectinput.position()[0]))
                        ypos = int(((y-(width/2))-pydirectinput.position()[1]))
                        # print(xpos,ypos)
                        # autopy.mouse.move(x,y) 
                        pydirectinput.moveRel(xpos,ypos)
                        pydirectinput.click()
                        # time.sleep(0.25)
                        # pydirectinput.moveRel(-xpos,-ypos)


            if (cv2.waitKey(20) & 0xFF) == ord('q'):
                
                cv2.destroyAllWindows()
                break

            if keyboard.is_pressed('e'):
                cv2.destroyAllWindows()
                break