import pyautogui
import threading
import time
import json
import requests
import Queue

baseURL = 'https://camera-db.firebaseio.com'
dataQueue = Queue.Queue()

class fetch_data(threading.Thread):
	def __init__(self, q):
		self.q = q
		threading.Thread.__init__(self)

		def fetch_data():
    		firebase = requests.get('%s/%s.json' % (baseURL, 'values'))
    		return firebase.json()

		def run(self):
			while True:
				data = fetch_data()
				self.q.put(data)


# def fetch_data():
#     firebase = requests.get('%s/%s.json' % (baseURL, 'values'))
#     return firebase.json()

def callback():
	print "lol i have no fucking clue when callback is called"

def move_cursor(gyro_data, x_threshold, y_threshold):
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
			data = dataQueue.get()
			gyro_dict, speech_dict, wink_dict = data['gyro'],data['speech'],data['wink']
			move_cursor(gyro_dict, 0.005, 0.02)
			click_cursor(wink_dict)
	except Exception as e:
		print(e)
			
if __name__ == "__main__":
	thread = fetch_data(dataQueue)
	thread.start()
	main()