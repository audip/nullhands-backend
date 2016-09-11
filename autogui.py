import pyautogui
import time
import json
import requests

baseURL = 'https://camera-db.firebaseio.com'

def fetch_data():
    firebase = requests.get('%s/%s.json' % (baseURL, 'values'))
    return firebase.json()

# def calc_delta_gyro(collection, delta_time):
# 	gyro_data = fetch_data('gyro')
# 	print(gyro_data)
# 	x, y = gyro_data['x'], gyro_data['y']
# 	time.sleep(delta_time)
# 	new_gyro_data = fetch_data('gyro')
# 	x_new, y_new = new_gyro_data['x'], new_gyro_data['y']
# 	print(x,y)
# 	return float(x_new)-float(x), float(y_new)-float(y)

def move_cursor(gyro_data, x_threshold,y_threshold):
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

def click_cursor(wink_data):
	click_left, click_right = wink_data['left'], wink_data['right'] 
	if click_left and not click_right:
		pyautogui.click(button='left')
	if not click_left and click_right:
		pyautogui.click(button='right')

def main():
	try:
		while(True):
			values_dict = fetch_data()
			gyro_dict = values_dict['gyro']
			speech_dict = values_dict['speech']
			wink_dict = values_dict['wink']
			move_cursor(gyro_dict, 0.005, 0.02)
			click_cursor(wink_dict)
	except Exception as e:
		print(e)
			
if __name__ == "__main__":
	main()