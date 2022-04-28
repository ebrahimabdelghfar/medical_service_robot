#!/usr/bin/env python3
from library import *
rospy.init_node("vision")

def connect_port(port):
  sim.simxFinish(-1)
  clientID=sim.simxStart("127.0.0.1",port,True,True,2000,5) #get the client ID
  if clientID==0:
    print("connected")
  else:
    print ("disc")
  return clientID

ID=connect_port(19999)
returncode,camera_handle=sim.simxGetObjectHandle(ID,"camera",sim.simx_opmode_oneshot_wait)
returncode,display_handle=sim.simxGetObjectHandle(ID,"display",sim.simx_opmode_oneshot_wait)
returncode,res,img=sim.simxGetVisionSensorImage(ID,camera_handle,0,sim.simx_opmode_streaming)
while (sim.simxGetConnectionId(ID) != -1):
  returncode,res,img=sim.simxGetVisionSensorImage(ID,camera_handle,0,sim.simx_opmode_buffer)
  if returncode == sim.simx_return_ok:
    img2 = np.array(img,dtype=np.uint8)
    img2.resize([res[0],res[1],3])
    for barcode in decode(img2):
      text = barcode.data.decode('utf-8')
      print(text)
      polygon_Points = np.array([barcode.polygon], np.int32)
      polygon_Points=polygon_Points.reshape(-1,1,2)
      rect_Points= barcode.rect
      cv2.polylines(img2,[polygon_Points],True,(255,255, 0), 5)
      cv2.putText(img2, text, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255, 0), 2)
      #adjust the image
      img2=cv2.flip(img2,0)
      #end
      img2 = np.ravel(img2)
      sim.simxSetVisionSensorImage(ID, display_handle,img2, 0, sim.simx_opmode_streaming)
    
