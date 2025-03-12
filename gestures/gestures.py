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

while True:
    #use PiCamera to capture an image
    frame = picam.capture_array()

    #run YOLO recognition
    results = yolo_model(frame)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  #detected class ID
            confidence = float(box.conf[0])  #confidence score
            
            #identify and handle gesture from class_id 
            gesture_names = ["thumbs_up", "open_palm", "fist", "thumbs_down", "point"]  #available gestures
            if class_id < len(gesture_names):
                detected = gesture_names[class_id]
                print(f"Detected: {detected} with confidence {confidence:.2f}")
                
                handle_gesture(detected) #handle each gesture

    #plot and display annotated results
    annotated_frame = results[0].plot()
    cv2.imshow("Hand Gesture Recognition", annotated_frame)

    #terminate the loop if q for 'quit' is entered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#close opened instances
cv2.destroyAllWindows()
picam.close()