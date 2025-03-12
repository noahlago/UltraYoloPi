from ultralytics import YOLO

#Load YOLO model
# yolo_model = YOLO("yolo11n.yaml") #build new model
yolo_model = YOLO("yolo11n.pt") #pretrained model
# yolo_model = YOLO("yolo11n.yaml").load("yolo11n.pt") #YAML build, apply existing weights

# yolo_model.train(data="coco8.yaml", epochs=100, imgsz=640)

yolo_model.train(data="hand_gesture_dataset.yaml", epochs=50, imgsz=640)


yolo_model.export(format="onnx")

#scp runs/train/weights/best.onnx pi@raspberrypi.local:/home/pi/
