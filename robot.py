#!/usr/bin/env python3
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import RPi.GPIO as gpio
import cv2
import subprocess
import time
import re

app = Flask(__name__)
socketio = SocketIO(app)

# GPIO setup

# GPIO pins
önSağPin = 13  # Replace with your GPIO pin numbers
önSolPin = 11
arkaİleriPin = 16
arkaGeriPin = 18

# Initialize GPIO pins

gpio.setmode(gpio.BOARD)
gpio.setup(önSağPin, gpio.OUT)
gpio.setup(önSolPin, gpio.OUT)
gpio.setup(arkaİleriPin, gpio.OUT)
gpio.setup(arkaGeriPin, gpio.OUT)



# OpenCV video capture
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
video_capture.set(cv2.CAP_PROP_FPS, 5)




@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # Adjust the quality here
            _, buffer = cv2.imencode('.jpg', frame, encode_param)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('control')
def handle_control(data):
    direction = data['direction']
    action = data['action']

    # Replace the following comments with your actual GPIO control logic
    if direction == 'forward' and action == 'start':
        print('Robot moving forward')
        gpio.output(arkaİleriPin, gpio.HIGH)
        gpio.output(arkaGeriPin, gpio.LOW)
    elif direction == 'backward' and action == 'start':
        print('Robot moving backward')
        gpio.output(arkaİleriPin, gpio.LOW)
        gpio.output(arkaGeriPin, gpio.HIGH)
    elif direction == 'left' and action == 'start':
        print('Robot turning left')
        gpio.output(önSağPin, gpio.LOW)
        gpio.output(önSolPin, gpio.HIGH)
    elif direction == 'right' and action == 'start':
        print('Robot turning right')
        gpio.output(önSağPin, gpio.HIGH)
        gpio.output(önSolPin, gpio.LOW)
    elif action == 'stop':
        print('Robot stopped')
        gpio.output(önSağPin, gpio.LOW)
        gpio.output(önSolPin, gpio.LOW)
        gpio.output(arkaİleriPin, gpio.LOW)
        gpio.output(arkaGeriPin, gpio.LOW)



if __name__ == '__main__':
    #start_ngrok()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
