# Development and Usage Guide for UltraYoloPi

This document provides detailed technical information about the implementation, development setup, and customization options for the UltraYoloPi hand gesture recognition system.

## Table of Contents

1. [Technical Implementation Details](#technical-implementation-details)
2. [Development Environment Setup](#development-environment-setup)
3. [System Requirements](#system-requirements)
4. [Performance Considerations](#performance-considerations)
5. [Machine Learning Model Details](#machine-learning-model-details)
6. [Continuous Learning System](#continuous-learning-system)
7. [Advanced Configuration](#advanced-configuration)
8. [Custom Gesture Training](#custom-gesture-training)
9. [Extending the System](#extending-the-system)
10. [Security Considerations](#security-considerations)

## Technical Implementation Details

### Flask Backend Architecture

The Flask backend (`server/yolo_pi_server.py`) is structured around these components:

- **Camera Interface**: Uses `picamera2` library to capture frames from the Pi camera
- **YOLO Integration**: Loads and runs the YOLOv8 nano model for detection
- **Image Processing**: Processes frames and annotates detected gestures
- **REST API**: Exposes endpoints for gesture detection and image access
- **Feedback DB**: SQLite database to store user feedback
- **Auto-Retraining**: Background thread that periodically retrains the model

### Express Frontend Architecture

The Express server (`yolo_webserver/server.js`) provides:

- **Static File Serving**: Delivers the HTML, CSS, and JavaScript for the web interface
- **API Proxying**: Forwards API requests to the Flask backend
- **Error Handling**: Manages connection issues and provides useful error responses

### Data Flow

1. Camera captures frames
2. Flask processes frames with YOLO at intervals
3. Detected gestures are stored with image data
4. Web interface displays the video stream and detection results
5. User provides feedback on detection accuracy
6. System stores feedback in SQLite database
7. Background process uses feedback to retrain model

## Development Environment Setup

### Complete Local Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ultrayolopi.git
cd ultrayolopi

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-mock flake8 black

# Install Node.js dependencies
cd yolo_webserver
npm install
npm install --save-dev nodemon

# Set up pre-commit hooks (optional)
cd ..
pip install pre-commit
pre-commit install

# Create configuration for development
cp config.example.py config.py
# Edit config.py with your development settings
```

### Required Python Packages

```
flask==2.0.1
flask-cors==3.0.10
opencv-python==4.5.3.56
picamera2==0.3.9
ultralytics==8.0.43
numpy==1.21.2
sqlite3==2.6.0
```

### Required Node.js Packages

```
express==4.17.1
axios==0.21.4
cors==2.8.5
```

## System Requirements

### Minimum Hardware Requirements

- Raspberry Pi 4 (2GB RAM minimum, 4GB recommended)
- Raspberry Pi Camera Module v2 or better
- 16GB microSD card (Class 10)
- Power supply with at least 2.5A output

### Recommended Hardware

- Raspberry Pi 4 (4GB or 8GB RAM)
- Raspberry Pi High-Quality Camera
- 32GB microSD card (Class 10, A1 rating)
- Proper cooling solution (heatsink or fan)
- 5V/3A power supply

### Operating System

- Raspberry Pi OS (64-bit recommended)
- Python 3.7+ with pip
- Node.js 14+ with npm

## Performance Considerations

### Optimizing for Raspberry Pi

- **Inference Interval**: The default 0.5-second interval can be adjusted based on your Pi's capabilities
- **Resolution**: The system uses 640x480px resolution by default, which can be lowered for better performance
- **Model Size**: YOLOv8n is chosen for its balance of speed and accuracy on the Pi

### Memory Usage

- The system requires approximately 500MB of RAM when running
- To reduce memory usage:
  - Decrease the resolution (e.g., to 320x240)
  - Increase the inference interval
  - Reduce the number of stored recent images

### CPU Usage

- CPU usage spikes during inference (every 0.5s by default)
- Average CPU usage is around 30-40% on a Raspberry Pi 4
- The background retraining process can cause temporary high CPU usage

## Machine Learning Model Details

### YOLO Model Specifications

- Model: YOLOv8n (nano version)
- Input resolution: 640x480
- Classes: 5 gesture types
- Inference time: ~100ms on Raspberry Pi 4

### Gesture Classes

The model is trained to recognize five distinct hand gestures:

1. `thumbs_up` (index: 0)
2. `open_palm` (index: 1) 
3. `fist` (index: 2)
4. `thumbs_down` (index: 3)
5. `point` (index: 4)

### Confidence Thresholding

- Default confidence threshold: 0.4 (40%)
- Detection below this threshold are ignored
- This can be adjusted in the code to balance between:
  - False positives (lower threshold)
  - False negatives (higher threshold)

## Continuous Learning System

### Feedback Collection

The system collects two types of feedback:
1. **Correct Detection**: Confirms the model was accurate
2. **Incorrect Detection**: Provides the correct label for misclassified gestures

### Database Schema

The feedback is stored in a SQLite database with the following structure:

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    image_filename TEXT,
    detected_gesture TEXT,
    is_correct INTEGER,
    user_label TEXT
)
```

### Retraining Process

1. The system periodically checks for incorrect detections in the database
2. If sufficient incorrect detections exist, it:
   - Creates a dataset.yaml file with the feedback data
   - Runs fine-tuning on the existing model
   - Loads the improved model weights
3. This process happens in the background every hour

## Advanced Configuration

### Configuration Parameters

Key parameters that can be modified in `yolo_pi_server.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `INF_INT` | 0.5 | Seconds between inference runs |
| `recent.maxlen` | 10 | Number of recent images to store |
| `confidence threshold` | 0.4 | Minimum confidence to accept a detection |

### Environment Variables

You can use environment variables to configure the system without changing code:

```bash
# Example of using environment variables
export FLASK_PORT=5050
export EXPRESS_PORT=3030
export DB_PATH=/custom/path/feedback.db
export IMG_FOLDER=/custom/path/images

# Then run the servers
python server/yolo_pi_server.py
node yolo_webserver/server.js
```

### Custom Logging

To enable detailed logging for debugging:

```python
# Add to yolo_pi_server.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='ultrayolopi.log'
)
```

## Custom Gesture Training

### Training on Your Own Gestures

To train the system on custom gestures:

1. **Collect Training Data**:
   - Create a dataset of images for each gesture
   - Organize in the YOLO dataset format
   - Label images using a tool like LabelImg

2. **Prepare Dataset YAML**:
   ```yaml
   # custom_gestures.yaml
   train: path/to/train/images
   val: path/to/val/images
   names:
     0: your_gesture_1
     1: your_gesture_2
     # Add more as needed
   ```

3. **Train the Model**:
   ```bash
   # From the project root
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt').train(data='custom_gestures.yaml', epochs=100)"
   ```

4. **Update the Code**:
   - Replace the gesture_names list in `yolo_pi_server.py`
   - Update the web interface to display the new gesture names

## Extending the System

### Adding New Features

#### 1. Gesture Sequence Recognition

Modify the code to detect sequences of gestures:

```python
# Add to yolo_pi_server.py
gesture_history = deque(maxlen=5)  # Store last 5 gestures

# In the generate_frames function, after updating current_gesture:
gesture_history.append(current_gesture)

# Add a new API endpoint
@app.route('/gesture_sequence')
def get_gesture_sequence():
    return jsonify({"sequence": list(gesture_history)})
```

#### 2. Gesture-Based Control Actions

```python
# Add function to interpret gestures as commands
def interpret_gesture_command(gesture):
    commands = {
        "thumbs_up": "INCREASE",
        "thumbs_down": "DECREASE",
        "fist": "STOP",
        "open_palm": "START",
        "point": "SELECT"
    }
    return commands.get(gesture, "NONE")

# Add a new API endpoint
@app.route('/command')
def get_command():
    command = interpret_gesture_command(current_gesture)
    return jsonify({"command": command})
```

### Integration with Other Systems

#### 1. MQTT Integration

```bash
# Install paho-mqtt
pip install paho-mqtt
```

```python
# Add to yolo_pi_server.py
import paho.mqtt.client as mqtt

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# In the generate_frames function, after updating current_gesture:
mqtt_client.publish("ultrayolopi/gesture", current_gesture)
```

#### 2. REST API Extensions

```python
# Add custom API endpoints for integration
@app.route('/api/v1/status')
def get_status():
    return jsonify({
        "running": True,
        "current_gesture": current_gesture,
        "model_version": "YOLOv8n",
        "uptime": time.time() - start_time
    })
```

## Security Considerations

### Network Security

- By default, the servers bind to all interfaces (0.0.0.0)
- For production, consider:
  - Enabling HTTPS
  - Adding authentication
  - Limiting access to specific IP addresses

### Data Privacy

- Images are stored temporarily on disk
- Consider adding an option to disable image storage
- Add a data retention policy for the feedback database

### Implementation Example:

```python
# Add authentication to Flask
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == os.environ.get('API_KEY', 'default_key'):
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return decorated

# Then use the decorator on routes
@app.route('/gesture')
@require_api_key
def get_gesture():
    return jsonify({"gesture": current_gesture})
```

---

This development guide is intended for developers and advanced users who want to customize and extend the UltraYoloPi system. For basic setup and usage, refer to the main README.md file.