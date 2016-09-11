# import autogui, blink
from flask import Flask, request
import json
app = Flask(__name__)

@app.route("/gyroscope", methods=['POST'])
def gyro():
    gyro_data = request.data
    print gyro_data
    print type(gyro_data)
    gyro_dict = json.dumps(gyro_data)
    print gyro_dict
    # autogui.move_cursor(gyro_dict, 0.005, 0.02)
    return gyro_data

@app.route("/speechtotext", methods=['POST'])
def speechtotext():
    speech_data = request.data
    speech_dict = json.loads(speech_data)
    return "fi"

@app.route("/wink", methods=['POST'])
def wink():
    wink_data = request.data
    wink_dict = json.loads(wink_data)
    autogui.click_cursor(wink_dict)
    return wink_data

if __name__ == "__main__":
    app.run()
