import pyautogui
import time
import json
import requests

baseURL = 'https://camera-db.firebaseio.com'

def fetch_data(collection):
    current_limit, i = 500, 0
    firebase = requests.get('%s/%s.json?limit' % (baseURL, collection))
        # time.sleep(0.5)
    return firebase.json()

def calc_delta_gyro(collection, delta_time):
	gyro_data = fetch_data('gyro')
	print(gyro_data)
	x, y = gyro_data['x'], gyro_data['y']
	time.sleep(delta_time)
	new_gyro_data = fetch_data('gyro')
	x_new, y_new = new_gyro_data['x'], new_gyro_data['y']
	print(x,y)
	return float(x_new)-float(x), float(y_new)-float(y)

def move_cursor(x_threshold,y_threshold):
	gyro_data = fetch_data('gyro')
	x,y = gyro_data['x'],gyro_data['y']
	x,y = float(x), float(y)
	x = 0 if abs(x) < x_threshold else x
	y = 0 if abs(y) < y_threshold else y
	x_sign = -1 if x >0 else 1
	y_sign = 1 if y > 0 else -1
	x_scale = (600*x)**2 
	y_scale = (80*y)**2
	print(x_scale, y_scale)
	pyautogui.moveRel(abs(x)*x_scale*x_sign,abs(y)*y_scale*y_sign) # make sure gyro coord is same as pyautogui

def main():
	while(True):
		x_cur, y_cur = pyautogui.position()
		#d_x, d_y = calc_delta_gyro('gyro', 0)


		gyro_data = fetch_data('gyro')
		x,y = gyro_data['x'], gyro_data['y']

		wink_data = fetch_data('wink')
		click_left, click_right = wink_data['left'], wink_data['right'] 
		if click_left and not click_right:
			pyautogui.click(button='left')
		if not click_left and click_right:
			pyautogui.click(button='right')
		move_cursor(0.005,0.02)

		# x_scale, y_scale = 15,  # adjust here
		# pyautogui.moveRel(x_scale*float(x), y_scale*float(y),0.3,pyautogui.easeOutQuad) # make sure gyro coord is same as pyautogui
		

if __name__ == "__main__":
    main()