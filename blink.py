import cv2
import itertools
import numpy as numpy
import threading
import time
import requests, json
import os

def save_data(wink_data):
    url = 'https://camera-db.firebaseio.com/wink.json'
    result = requests.put(url, data=json.dumps(wink_data))
    return result

# given more than two candidates for eyes, selects the best pair using y coord as a ranking
# draws the pair on the frame
def findBestEyes(eyes, frame):
    if len(eyes) > 2:
        min_dif = 9999
        best_eyes = None
        for eye1, eye2 in itertools.combinations(eyes,2):
            dif = abs(eye1[1]-eye2[1])
            if dif < min_dif:
                min_dif = dif
                best_eyes = [eye1,eye2]
    else:
        best_eyes = eyes
    # for x,y,w,h in best_eyes:
    #     cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 1)
    return best_eyes

def findEyeStatus(eyes, eye_status, frame):
    h_frame, w_frame = frame.shape[:2] # if x_pupil is less than w_frame/2, its on LHS
    pupils = []
    for x,y,w,h in eyes:
        pupils.append(x+w/2) # only append x coord of each pupil
    for pupil in pupils:
        if pupil < w_frame/2:
            eye_status['right'] = True
        if pupil > w_frame/2:
            eye_status['left'] = True
    return eye_status

def printEyeStatus(eye_status):
    out = ''
    out += "left open     " if eye_status['left'] else "left closed     "
    out += "right open" if eye_status['right'] else "right closed"
    print out

def main():
    eye_status = {'left': False, 'right': False}
    prev_eye_status = None
    cam = cv2.VideoCapture(0)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
    eye_cascade_path = os.path.join(os.path.realpath(__file__).strip(__file__),"haarcascade_eye.xml")
    file_path_path = os.path.join(os.path.realpath(__file__).strip(__file__),"haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    face_cascade = cv2.CascadeClassifier(file_path_path)
    while(True):
        printEyeStatus(eye_status)
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(face)==1:
            x,y,w,h = face[0]
            cropped_frame = frame[y:y+h*0.66,x:x+w]
            time.sleep(0.1)
            eyes = eye_cascade.detectMultiScale(
                cv2.cvtColor(cropped_frame,cv2.COLOR_BGR2GRAY),
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            eyes = findBestEyes(eyes,cropped_frame)
            eye_status = {'left': False, 'right': False}
            eye_status = findEyeStatus(eyes, eye_status, cropped_frame)
            if eye_status != prev_eye_status:
                save_data(eye_status)
            prev_eye_status = eye_status
            
            cv2.imshow("ayy lmao", cropped_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()