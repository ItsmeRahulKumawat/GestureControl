import cv2
import numpy
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####################
wCam, hCam = 640, 480
#####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(detectionCon=0.8)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0] # set the min val for sound
maxVol = volRange[1] # set max
vol = 0
volBar = 400 # bcos its 400 at lowest postion in bar
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # bcos its returning 3 list values and we want only '1' one
        x2, y2 = lmList[8][1], lmList[8][2] # 8 is x part and 1,2 is y part
        cx, cy = (x1+x2)//2, (y1+y2)//2 # one '/' gives the float value and '//' give int val

        cv2.circle(img, (x1,y1), 5, (255,0,255),cv2.FILLED) #create 2 circles at the given point
        cv2.circle(img, (x2,y2), 5, (255,0,255),cv2.FILLED) #to know whether we took right hand points
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3) #draws the line between two points
        cv2.circle(img, (cx, cy), 5, (255,0,0),cv2.FILLED) #circle to know the middle of line

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # our handrange was 15 - 200
        # Volume Range from -65 - 0

        # specifying that vol will be in between and 20-180 is our pc limit by hand gesture
        vol = numpy.interp(length, [20, 150], [minVol, maxVol])
        volBar = numpy.interp(length, [20, 150], [400, 150])
        volPer = numpy.interp(length, [20, 150], [0, 100])


        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)  # this will change the system volume

        if length < 20:
            cv2.circle(img, (cx, cy), 5, (100, 110, 220), cv2.FILLED)  # circle to know the middle of line

    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
    cv2.putText(img,f' {int(volPer)} %', (40,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)