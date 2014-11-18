#########VERSION 20141118-PI
import cv2
import numpy as np
import client

def nothing(x):
    pass

kernel = np.ones((5,5),np.uint8)
mask2 = np.zeros((240,320),np.uint8)

cap = cv2.VideoCapture(0)
cap.read()
cap.set(3,320)
cap.set(4,240)

cv2.namedWindow('box',flags = cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('h','box',0,255,nothing)
cv2.createTrackbar('s','box',55,255,nothing)
cv2.createTrackbar('v','box',223,255,nothing)
cv2.createTrackbar('left','box',0,240,nothing)
cv2.createTrackbar('right','box',240,240,nothing)

#oldCx = 0
#oldCy = 0
h = 0
s = 55
v = 223
while(1):
    mask2 = np.zeros((240,320), np.uint8)
    h = cv2.getTrackbarPos('h','box')
    s = cv2.getTrackbarPos('s','box')
    v = cv2.getTrackbarPos('v','box')
    left= cv2.getTrackbarPos('left','box')
    right= cv2.getTrackbarPos('right','box')
    cv2.rectangle(mask2,(left,0),(right,240),(255,255,255),-1)

    # Take each frame
    _, frame = cap.read()

    # # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of ball color
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h+20,255,255])

    # Threshold the HSV image to get only balls
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    dilation = cv2.dilate(mask,kernel,iterations = 1) & mask2
    #dilation = dilation & mask2

    #Find contours
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    frame = cv2.bitwise_and(frame,frame, mask=mask2)
    #Find largest contour (ball)
    if len(contours) > 0:
        max_area = 0
        largest_contour = None
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        cnt = largest_contour
        if cnt != None:
            M = cv2.moments(cnt)
        
        if M["m00"] > 300:
            if M['m00'] > 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame,(cx,cy), 15, (0,255,0), 2)
   #             vx = cx - oldCx
   #             vy = cy - oldCy
   #             cv2.line(frame,(cx,cy),(cx+vx*10,cy+vy*10),(255,0,0),2)
   #             oldCx = cx
   #             oldCy = cy
   #             #cv2.line(path,(oldCx,oldCy),(cx,cy),(255,255,255),2)
                client.sendMessage(str(cx) + " "+str(cy)+"o") # NETTWORK
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
client.s.close()
cv2.destroyAllWindows()
