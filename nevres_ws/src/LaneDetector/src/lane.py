import cv2
from tensorflow import keras
from keras.models import load_model
import time
import pandas as pd
import numpy as np
import serial
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan


data=[0,1,2,0,0]
arduino = serial.Serial('/dev/ttyUSB1',baudrate=115200,timeout=.5)
time.sleep(5)

steeringMaxAngle = 255

def stop():
    data[2] = 1
    time.sleep(0.2)
    arduino.write(data)


def goStraight(value):
    data[0] = 70
    data[2] = 2
    data[3] = int(value)
    print(data)
    time.sleep(0.5)
    arduino.write(data)
    


def steeringAverage(value):
    data[0] = 70
    data[1] = 1
    data[2] = 2
    data[3] = int(value)
    print(data)
    time.sleep(0.15)
    arduino.write(data)
middlePosition = steeringMaxAngle / 2 
steeringAverage(middlePosition)
time.sleep(8)


model = load_model("/home/oguzhan/nevres_ws/src/LaneDetector/src/nevres-best.hdf5", compile=False)


cap=cv2.VideoCapture(0)

while True:
    
    frames=[]
    ret,frame =cap.read()

    frame = frame[0:376,0:672]
    
    framef = cv2.resize(frame, (256, 256))
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.resize(gray_image, (256, 256))
    frames.append(gray_image)
    image_dataset = np.array(frames)
    image_dataset = np.expand_dims(image_dataset, axis=3)
    image_dataset = image_dataset / 255.


    pred = (model.predict(image_dataset)[0,:,:,0] > 0.5).astype(np.uint8)

    pred = pred.reshape(256, 256, 1)
    pred = pred.astype(np.uint8)

    h, w, d = pred.shape
    image = framef.copy()

    mask0 = pred.copy()
    mask6 = pred.copy()

    sagserit = pred.copy()
    solserit = pred.copy()

    search_top0 = h // 2
    search_bot0 = h // 2 + 100
    mask0[0:search_top0, 0:w] = 0
    mask0[search_bot0:h, 0:w] = 0
    mask_sol_karsi = mask0.copy()
    mask_sag_karsi = mask0.copy()

    sol_roi_x = 7 * w // 13
    sol_roi_y = 2 * h // 7 

    sag_roi_x = 4 * w // 6 
    sag_roi_y = 2 * h // 7 

    mask_sol_karsi[:, sol_roi_x:] = 0
    mask_sag_karsi[:, :sag_roi_x] = 0

    search = h // 2 + 150
    mask6[0:search, 0:w] = 0

    sagserit[:sag_roi_y, :] = 0
    sagserit[sag_roi_y:, :sag_roi_x] = 0

    solserit[:sol_roi_y, :] = 0
    solserit[sol_roi_y:, sol_roi_x:] = 0

    M = cv2.moments(solserit)
    N = cv2.moments(sagserit)

    SagM = cv2.moments(mask_sag_karsi)
    SolM = cv2.moments(mask_sol_karsi)

    S = cv2.moments(mask0)

    pred *= 255
    pred = pred.astype(np.uint8)
    white_pixel_count = np.sum(pred)
    red = np.zeros((image.shape[0], image.shape[1], image.shape[2]), np.uint8)
    cv2.rectangle(red, (0, 0), (red.shape[1], red.shape[0]), (255, 0, 0), -1)
    maskbgr = cv2.cvtColor(pred, cv2.COLOR_GRAY2BGR)
    try:
        redmask = cv2.bitwise_and(maskbgr, red)
        bitnot = cv2.bitwise_not(pred)
        bitnot3 = cv2.cvtColor(bitnot, cv2.COLOR_GRAY2BGR)
        bitw = cv2.bitwise_and(image, bitnot3)
        image = cv2.add(bitw, redmask)
    except:
        print("Frame Hatası")

    solRef=0
    sagRef=0

    try:
        cx1 = int(M['m10'] / M['m00'])
        cy1 = int(M['m01'] / M['m00'])
        cv2.circle(image, (cx1, cy1), 5, (0, 0, 0), -1)
        cv2.putText(image, "Sol", (cx1 - 10, cy1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_4)
        solRef=cx1
        print(cx1)
    except:
        print("Sol Serit ALgılanamadı")


    try:
        cx2 = int(N['m10'] / N['m00'])
        cy2 = int(N['m01'] / N['m00'])
        cv2.circle(image, (cx2, cy2), 5, (0, 0, 0), -1)
        cv2.putText(image, "Sag", (cx2 - 10, cy2 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_4)
        sagRef=cx2
    except:
        print("Sag Serit Algılanamadı")

    image = cv2.resize(image, (850, 400))
    orta_nokta = ( sagRef+ solRef )
    orta_nokta = orta_nokta / 2

    if orta_nokta < 116 :
        
        goStraight(135)
        print("Sola Dönülüyor")

    elif orta_nokta > 130:
        goStraight(105)
        print("Saga Dönülüyor")
    else :
        goStraight(190)
        print("Düz Devam Ediliyor")




    print(orta_nokta)

    cv2.imshow('lane segmentation', image)

    if cv2.waitKey(1) == ord('q'):
        break