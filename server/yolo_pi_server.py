from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import threading

#Flask initialization
app = Flask(__name__)
CORS(app)  #Cross origin requests enabled

#Load the trained model for hand gestures
model = YOLO("yolo11n.pt")

#PiCamera initialization and settings
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

current_gesture = "None"  #Temporarily stores the gesture recognized by the yolo model

def generate_frames():
    global current_gesture
    while True:
        frame = picam2.capture_array()

        #Run yolo model on the captured image
        results = model(frame)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  #id of the detected result
                confidence = float(box.conf[0])

                #Available gestures
                gesture_names = ["thumbs_up", "open_palm", "fist", "thumbs_down", "point"] 
                if class_id < len(gesture_names):
                    current_gesture = gesture_names[class_id]

        #Attach the detected gesture to the frame
        annotated_frame = results[0].plot()

        #Convert the frame to a jpeg image
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        #Return/yield the frame 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture')
def get_gesture():
    return jsonify({"gesture": current_gesture})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)