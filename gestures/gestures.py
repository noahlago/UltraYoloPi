from ultralytics import YOLO
import cv2
from picamera2 import Picamera2

#Load and train model 
#TODO Save + reuse trained model to avoid unnecessary retraining
yolo_model = YOLO("yolo11n.pt")
yolo_model.train(data="hand_gesture_dataset.yaml", epochs=50, imgsz=640)
yolo_model.export(format="onnx")

#PiCamera setup (using a PiCamera v3)
picam = Picamera2()
picam.preview_configuration.main.size = (640, 480)
picam.preview_configuration.main.format = "RGB888"
picam.configure("preview")
picam.start()

def handle_gesture(gesture):
    match(gesture):
        case "thumbs_up":
            print("Thumbs Up!")
        case "open_palm":
            print("Open Palm!")
        case "fist":
            print("Fist!")
        case "thumbs_down":
            print("Thumbs Down!")
        case "point":
            print("Point!")
        case _: #default
            print("Unkown gesture: {gesture}")

