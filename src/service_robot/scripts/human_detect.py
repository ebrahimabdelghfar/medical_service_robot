import cv2
import imutils
import numpy as np
import argparse
from library import *
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def connect_port(port):
  sim.simxFinish(-1)
  clientID=sim.simxStart("127.0.0.1",port,True,True,2000,5) #get the client ID
  if clientID==0:
    print("connected")
  else:
    print ("disc")
  return clientID


def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", default=None, help="path to Video File ")
    arg_parse.add_argument("-i", "--image", default=None, help="path to Image File ")
    arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")
    arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
    args = vars(arg_parse.parse_args())
    return args

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    return frame


HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
args = argsParser()

ID=connect_port(19999)
returncode,camera_handle=sim.simxGetObjectHandle(ID,"camera",sim.simx_opmode_oneshot_wait)
returncode,display_handle=sim.simxGetObjectHandle(ID,"display",sim.simx_opmode_oneshot_wait)
returncode,res,img=sim.simxGetVisionSensorImage(ID,camera_handle,0,sim.simx_opmode_streaming)
while (sim.simxGetConnectionId(ID) != -1):
    returncode,res,img=sim.simxGetVisionSensorImage(ID,camera_handle,0,sim.simx_opmode_buffer)
    if returncode == sim.simx_return_ok:
        img2 = np.array(img,dtype=np.uint8)
        img2.resize([res[0],res[1],3])
        #detecting human
        img2 = detect(img2)
        #end 
        #adjust the image
        img2=cv2.flip(img2,0)
        #end
        frame = np.ravel(img2)
        sim.simxSetVisionSensorImage(ID, display_handle,frame, 0, sim.simx_opmode_streaming)
