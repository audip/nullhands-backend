import pyautogui
import time
from firebase import firebase



def connect_db():
    return firebase.FirebaseApplication('https://camera-db.firebaseio.com', None)

def fetch_wink(collection):
    firebase = connect_db()
    blink_left = firebase.get('wink', 'left')
    blink_right = firebase.get('wink', 'right')
    return blink_left, blink_right

def fetch_gyro(collection):
    firebase = connect_db()
    x = firebase.get('gyro', 'x')
    y = firebase.get('gyro', 'y')
    return x, y

def calc_delta_gyro(collection, delta_time):
	x, y = fetch_gyro('gyro')
	time.sleep(delta_time)
	x_new, y_new = fetch_gyro('gyro')
	print(x,y)
	return float(x_new)-float(x), float(y_new)-float(y)

def main():
	while(True):
		x_cur, y_cur = pyautogui.position()
		d_x, d_y = calc_delta_gyro('gyro', 0.1)
		click_left, click_right = fetch_wink('wink')
		x_scale, y_scale = 1000, 1000 # adjust here
		pyautogui.moveRel(x_scale*d_x, y_scale*d_y) # make sure gyro coord is same as pyautogui
		if click_left and not click_right:
			pyautogui.click(button='left')
		if not click_left and click_right:
			pyautogui.click(button='right')

if __name__ == "__main__":
    main()