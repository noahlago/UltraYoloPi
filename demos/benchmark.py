from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("yolo11n.pt")

# Benchmark YOLO11n speed and accuracy on the COCO8 dataset for all all export formats
results = model.benchmark(data="coco8.yaml", imgsz=640)