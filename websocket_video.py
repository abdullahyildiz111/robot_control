from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import base64
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

video_capture = cv2.VideoCapture(0)

def capture_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('video_frame', {'data': 'data:image/jpeg;base64,' + frame}, namespace='/video')
        time.sleep(0.1)  # Adjust sleep time as needed

@socketio.on('connect', namespace='/video')
def test_connect():
    print('Client connected')

@app.route('/')
def index():
    return render_template('video.html')

if __name__ == '__main__':
    # Start the video capture thread
    threading.Thread(target=capture_frames, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
