import cv2
from picamera2 import Picamera2
from ultralytics import YOLO 

#Camera initialization
picam = Picamera2()
picam.preview_configuration.main.size = (1280, 720)
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.align
picam.configure("preview")
picam.start

