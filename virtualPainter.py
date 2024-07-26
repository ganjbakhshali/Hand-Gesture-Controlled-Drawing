import cv2
import numpy as np
import os
import time
import HandTrakingModule as hmt

imgPaths="images"
imglist=os.listdir(imgPaths)

imgLayer=[]
for imPath in imglist:
    image= cv2.imread(f"{imgPaths}/{imPath}")
    imgLayer.append(image)
    
# print(len(imgLayer))

header= imgLayer[0]
color=(0,0,255)#BGR
cap=cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)
brushThickness=15
eraserThickness=50

detector= hmt.handDetector(detectionCon=0.85)
xp,yp=0,0


imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    
    #1-import image
    success, img=cap.read()
    img = cv2.flip(img,1)
    
    #2-find landmarks
    img= detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    
    if len(lmlist)!=0:
        

        #index of index and middle finger:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        
        
        
    
        #3- check which finger is up
        fingers=detector.fingersUp()
        # print(fingers)
        #4- if selection mode -2 fingers up:
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print("Selection mode")
            if y1<125:
                if 250<x1<450:
                    header= imgLayer[0]
                    color=(0,0,255)
                elif 550<x1<750:
                    header= imgLayer[1]
                    color=(255,0,0)
                elif 800<x1<950:
                    header= imgLayer[2]
                    color=(0,255,0)
                elif 1050<x1<1200:
                    header= imgLayer[3]
                    color=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),color,cv2.FILLED)
        
        #5-- if drwaing mode - index is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,color,cv2.FILLED)
            print("Drawing mode")
            
            if xp==0 and yp==0:
                xp,yp=x1,y1
            
            if color==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),color,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),color,eraserThickness)
            else:   
                cv2.line(img,(xp,yp),(x1,y1),color,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),color,brushThickness)
            xp,yp=x1,y1
            
            
    #create Mask        
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)
    
    
    img[0:125,0:1280]=header
    # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("image",img)
    cv2.imshow("imgCanvas",imgCanvas)
    cv2.waitKey(1)

