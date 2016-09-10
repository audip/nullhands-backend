# import autogui
from flask import Flask, request
app = Flask(__name__)

@app.route("/gyroscope", methods=['POST'])
def gyro():
    gyro_data = request
    print(gyro_data)
    return gyro_data

@app.route("/speechtotext", methods=['POST'])
def speechtotext():
    return "fi"

if __name__ == "__main__":
    app.run()
