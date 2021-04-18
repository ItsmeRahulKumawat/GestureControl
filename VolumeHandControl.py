import cv2
import numpy
import time
import HandTrackingModule as htm

#####################
wCam, hCam = 640, 480
#####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # bcos its returning 3 list values and we want only '1' one
        x2, y2 = lmList[8][1], lmList[8][2] # 8 is x part and 1,2 is y part

        cv2.circle(img, (x1,y1), 5, (255,0,255),cv2.FILLED) #create 2 circles at the given point
        cv2.circle(img, (x2,y2), 5, (255,0,255),cv2.FILLED) #to know whether we took right hand points


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)