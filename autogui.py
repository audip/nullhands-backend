import pyautogui
import time

from firebase import firebase



def connect_db():
    return firebase.FirebaseApplication('https://camera-db.firebaseio.com', None)

def fetch_wink(collection):
    firebase = connect_db()
    blink_left = firebase.get('wink', 'left')
    blink_right = firebase.get('wink', 'right')
    return [blink_left, blink_right]

def fetch_gyro(collection):
    firebase = connect_db()
    response_x = firebase.get('gyro', 'x')
    response_y = firebase.get('gyro', 'y')
    return [response_x, response_y]

screenWidth, screenHeight = pyautogui.size()

#def move_cursor(time):
#	direction = fetch_gyro('gyro')
#	pyautogui.moveTo(float(direction[0]), float(direction[1]), time)

print(fetch_wink('wink'))
print(fetch_gyro('gyro'))

#move_cursor(1)




