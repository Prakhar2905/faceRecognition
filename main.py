import threading

import cv2
from deepface import DeepFace

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
faceMatched = False
checkImage = cv2.imread("reference.jpg")

def authorization(frame):
    global faceMatched
    try:
        if DeepFace.verify(frame, checkImage):
            faceMatched = True
        else:
            faceMatched = False
    except ValueError:
        faceMatched = False


while True:
    ret, frame = cam.read()
    if ret:
        if counter %30 == 0:
            try:
                threading.Thread(target=authorization, args=(frame.copy(),)).start
            except ValueError:
                pass
        counter = counter + 1

        if faceMatched:
            cv2.putText(frame, "Authorized", (20,450), cv2.FONT.HERSHEY_SIMPLEX, 2, (0,255,0), 5 )
        else:
            cv2.putText(frame, "Not Authorized", (20,450), cv2.FONT.HERSHEY_SIMPLEX, 2, (0,0,255), 5 )

    pressed = cv2.waitKey(1)
    if pressed == ord("e"):
        break

cv2.destroyAllWindows

