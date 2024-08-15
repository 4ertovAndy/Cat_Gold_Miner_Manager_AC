

#I will be glad of any help
#to improve the work of this project
#and other projects.


#DONAT

#in Telegram-stars @o4ertov_andy
#TON NOT USDT valet - UQDQD8AAtR0ksFG9QONgOK72qzeVf2AM1xUcc3GDu8dVOXXr



import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import random


AC_START_STOP = keyboard.Key.ctrl_r
CLOSE_AC = keyboard.Key.shift_r 
region = (30, 30, 370, 630)


clicking_enabled = False
program_running = True
executor = ThreadPoolExecutor(max_workers=1)

def on_press(key):
    global clicking_enabled, program_running
    try:
        if key == AC_START_STOP:
            clicking_enabled = not clicking_enabled
            print(f"AC JOB  {clicking_enabled}")
        elif key == CLOSE_AC:
            program_running = False
            print("Exit AC...")
            return False  
    except AttributeError:
        pass

def click_on_position(screen_x, screen_y):
    global clicking_enabled
    if clicking_enabled:
        pyautogui.click(screen_x, screen_y)

def print_areas(frame):
    cv2.rectangle(frame,(287,1),(300,25),(0,255,255),2)
    cv2.rectangle(frame,(5,330),(80,350),(0,255,255),2)
    cv2.rectangle(frame,(120,495),(195,515),(0,255,255),2)
    cv2.rectangle(frame,(190,300),(210,320),(255,255,0),2)

def find_timer(area):
    hsv = cv2.cvtColor(area, cv2.COLOR_BGR2HSV)
    #cv2.imwrite("result_1.jpg", hsv)
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([10, 10, 10]))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(area, contours, -1, (0, 0, 255), 2)
    #cv2.imwrite("result_2.jpg", area)
    #print(len(contours))
    if len(contours) > 2:
        return (False, len(contours))
    else:
        return (True, len(contours))

def find_dance_cat(area):
    hsv = cv2.cvtColor(area, cv2.COLOR_BGR2HSV)
    #cv2.imwrite("result_cat_1.jpg", hsv)
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([10, 10, 10]))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(area, contours, -1, (0, 0, 255), 2)
    #cv2.imwrite("result_2.jpg", area)
    #print(len(contours))
    if len(contours) > 0:
        return (True, len(contours))
    else:
        return (False, len(contours))

def activ_manager():
    executor.submit(click_on_position, 285, 630)
    time.sleep(1)
    executor.submit(click_on_position, 100, 560)
    time.sleep(1)
    executor.submit(click_on_position, 100, 100)
    time.sleep(1)
    executor.submit(click_on_position, 350, 155)
    time.sleep(1)

def activ_dance_cat():
    executor.submit(click_on_position, 210, 320)
    time.sleep(1)
    executor.submit(click_on_position, 150, 500)
    time.sleep(1)


def capture_and_process():
    global program_running
    while program_running:
        time.sleep(1) 
        screenshot = pyautogui.screenshot(region=region)
        mframe = np.array(screenshot)
        frame = cv2.cvtColor(mframe, cv2.COLOR_RGB2BGR)
        #370*630
        print_areas(frame)
        #hsv = cv2.cvtColor(mframe, cv2.COLOR_BGR2HSV)
        #cv2.imwrite("result_cat.jpg", mframe)     
        cv2.imshow("Captured area", frame)
        cv2.waitKey(1)  
        
        crop_1_timer = mframe[330:350, 5:80].copy()
        con = find_timer(crop_1_timer)
        if not con[0]:
            print(f'not 1 timer {con[1]}')
        else:
            print(f'yes 1 timer {con[1]}')
            if clicking_enabled:
                activ_manager()
        crop_2_timer = mframe[495:515, 120:195].copy()
        con = find_timer(crop_2_timer)
        if not con[0]:
            print(f'not 2 timer {con[1]}')
        else:
            print(f'yes 2 timer {con[1]}')
            if clicking_enabled:
                activ_manager()
        crop_dance_cat = mframe[300:320,190:210].copy()
        con = find_dance_cat(crop_dance_cat)
        if not con[0]:
            print(f'not Dance Cat {con[1]}')
        else:
            print(f'yes Dance Cat {con[1]}')
            if clicking_enabled:
                activ_dance_cat()
            
    cv2.destroyAllWindows()
    print("Capture and processing thread terminated")

listener = keyboard.Listener(on_press=on_press)
listener.start()

capture_thread = threading.Thread(target=capture_and_process)
capture_thread.start()

try:
    listener.join()
    capture_thread.join()
except KeyboardInterrupt:
    cv2.destroyAllWindows()
    print("Program terminated")
