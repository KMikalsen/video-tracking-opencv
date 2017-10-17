############## VERSION 20141118-PC
import cv2
import numpy as np

import serial
import time
font = cv2.FONT_HERSHEY_SIMPLEX
ser = serial.Serial("COM6",115200)
mask2 = np.zeros((480,640), np.uint8)
meanVal = [2,128,208]

kernel = np.ones((5,5),np.uint8)

cap = cv2.VideoCapture(1)
cap.read()
cv2.namedWindow('bars')
cv2.namedWindow('box',flags = cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('h','box',0,255,nothing)
cv2.createTrackbar('s','box',55,255,nothing)
cv2.createTrackbar('v','box',223,255,nothing)

cv2.createTrackbar('lx','box',74,640,nothing)
cv2.createTrackbar('ly','box',0,480,nothing)
cv2.createTrackbar('rx','box',511,640,nothing)
cv2.createTrackbar('ry','box',480,480,nothing)
oldCx = 0
oldCy = 0
while(1):
    h = cv2.getTrackbarPos('h','box')
    s = cv2.getTrackbarPos('s','box')
    v = cv2.getTrackbarPos('v','box')
    lx = cv2.getTrackbarPos('lx','box')
    ly = cv2.getTrackbarPos('ly','box')
    rx =cv2.getTrackbarPos('rx','box')
    ry =cv2.getTrackbarPos('ry','box')
    mask2 = np.zeros((480,640), np.uint8)
    cv2.rectangle(mask2,(lx,ly),(rx,ry),(255,255,255),-1)
    # Take each frame
    _, frame = cap.read()
    frame = cv2.flip(frame,0)
    img = cv2.medianBlur(frame,5)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h+20,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    dilation = cv2.dilate(mask,kernel,iterations = 1)
    dilation = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    dilation = dilation & mask2
    cv2.imshow('mask',dilation)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= dilation)
    
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.bitwise_and(frame,frame,mask=mask2)
    if len(contours) > 0:
        max_area = 0
        largest_contour = None
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        cnt = largest_contour #contours[0]
        if cnt != None:
            M = cv2.moments(cnt)
        if M["m00"] > 1000:
            if M['m00'] > 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            #print "Cx: "+str(cx) + "\t Cy: "+str(cy)
            cv2.circle(frame,(cx,cy), 25, (0,0,255), 3)
            cv2.putText(frame,'Tracking',(10,50), font, 1.5,(0,255,0),2,cv2.CV_AA)
            cv2.putText(frame,'X:'+str(cy)+' Y:'+str(cx),(cx+25,cy+25), font, 0.5,(255,0,0),1,cv2.CV_AA)
            vx = cx - oldCx
            vy = cy - oldCy
            cv2.line(frame,(cx,cy),(cx+vx*10,cy+vy*10),(255,0,0),2)
            oldCx = cx
            oldCy = cy
            print str(cy) + " "+str(cx)
            ser.write(str(cy) + " "+str(cx)+"o")
    else:
        cv2.putText(frame,'Not tracking',(10,50), font, 1.5,(0,0,255),2,cv2.CV_AA)
    frame = cv2.resize(frame, (640, 480))
    if(frame != None):
        cv2.imshow('frame',frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
