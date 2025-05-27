# UltraYoloPi: Hand Gesture Recognition System

A real-time hand gesture recognition system using YOLO object detection on a Raspberry Pi with web interface and continuous learning capabilities.

## Overview

UltraYoloPi is a machine learning project that combines computer vision and deep learning to recognize hand gestures in real-time. The system uses:

- **YOLOv8 (YOLO11n)** for fast and accurate gesture detection
- **Raspberry Pi** with a camera module for image capture
- **Flask** backend for image processing and API services
- **Express.js** for the web interface
- **User feedback** collection to improve model accuracy over time

The system can detect five hand gestures: 👍 thumbs up, 👎 thumbs down, ✋ open palm, ✊ fist, and 👉 pointing.

## System Architecture

```
┌─────────────────┐     ┌───────────────────┐     ┌────────────────────┐
│  Raspberry Pi   │     │  Flask Backend    │     │  Express Frontend  │
│  (Camera + YOLO)│────▶│  (Port 5000)      │────▶│  (Port 3000)       │
└─────────────────┘     └───────────────────┘     └────────────────────┘
                                 ▲                          │
                                 │                          │
                                 └──────────────────────────┘
                                       User Feedback
```

### Components:

1. **Camera Module**: Captures real-time video frames
2. **YOLO Model**: Processes frames to detect hand gestures
3. **Flask Server**: Handles image processing and exposes APIs
4. **SQLite Database**: Stores user feedback for model improvement
5. **Express Server**: Serves the web interface
6. **Web Interface**: Displays results and collects feedback

## Prerequisites

- Raspberry Pi 4 or newer (with at least 2GB RAM)
- Raspberry Pi Camera Module
- Python 3.7+
- Node.js 14+
- Internet connection for initial setup

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ultrayolopi.git
cd ultrayolopi
```

### 2. Set Up the Python Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt
```

### 3. Download the YOLO Model

```bash
# Download the pre-trained YOLOv8n model
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O yolo11n.pt
```

### 4. Set Up the Web Server

```bash
# Navigate to the web server directory
cd yolo_webserver

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

### 5. Create Required Directories

```bash
# Create directory for storing processed images
mkdir -p server/recently_processed
```

## Running the System

### 1. Start the Flask Server

```bash
# In one terminal
cd server
python yolo_pi_server.py
```

### 2. Start the Express Web Server

```bash
# In another terminal
cd yolo_webserver
node server.js
```

### 3. Access the Web Interface

Open your browser and navigate to:
```
http://[raspberry_pi_ip]:3000
```

Replace `[raspberry_pi_ip]` with your Raspberry Pi's IP address.

## Usage

### Viewing Gesture Recognition

1. Ensure that the camera is enabled (privacy mode is disabled)
2. Position your hand in front of the camera
3. Make one of the five supported gestures
4. The system will display the detected gesture in real-time
5. Recent detections appear below the main video feed

### Providing Feedback for Model Improvement

1. Review the detected gestures in the "Recent Detections" section
2. For each detection:
   - Click "✔️ Correct" if the detection is accurate
   - Click "❌ Incorrect" if the detection is wrong
     - When clicked, you'll be prompted to enter the correct gesture
3. Your feedback will be used to improve the model over time

## System Features

### Real-time Processing

The system processes camera frames periodically (every 0.5 seconds) to balance performance and responsiveness. This approach ensures:
- Smooth operation on Raspberry Pi hardware
- Reduced CPU and memory usage
- Adequate responsiveness for gesture detection

### Error Handling

The system includes robust error handling to manage various failure modes:
- Camera connection issues
- Model inference failures
- Network communication problems
- Database errors

### Continuous Learning

The system improves over time through:
- Collection of user feedback on detection accuracy
- Periodic model retraining using incorrectly classified images
- Automatic model updates without requiring system restart

## API Reference

### Flask Backend (Port 5000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/video_feed` | GET | Live video stream with gesture annotations |
| `/gesture` | GET | Current detected gesture as JSON |
| `/recent` | GET | List of 10 most recent detections |
| `/image/<filename>` | GET | Specific image from detection history |
| `/feedback` | POST | Submit user feedback about detections |

### Express Frontend (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/gesture` | GET | Proxy to Flask gesture endpoint |
| `/recent` | GET | Proxy to Flask recent endpoint |
| `/feedback` | POST | Proxy to Flask feedback endpoint |

## Troubleshooting

### Video Feed Not Loading

- Ensure the camera is properly connected to the Raspberry Pi
- Check that the Picamera2 module is correctly installed
- Verify the Flask server is running on port 5000
- Check network connectivity between your browser and the Raspberry Pi

### Detection Accuracy Issues

- Ensure adequate lighting in the environment
- Position your hand clearly in the camera's field of view
- Provide feedback for incorrect detections to improve the model
- Check the model file exists and is correctly loaded
- Switch to a more powerful yolo model if your system capabilities permit it

### Connection Errors

- Verify both Flask and Express servers are running
- Check network connectivity between the servers
- Ensure the correct IP addresses are being used in configuration
- Check physical camera connection to the board

## Advanced Configuration

### Adjusting Inference Frequency

To change how often the system processes frames, modify the `INF_INT` variable in `server/yolo_pi_server.py`:

```python
INF_INT = 0.5  # Process frames every 0.5 seconds
```

### Adjusting Confidence Threshold

To change the minimum confidence level for gesture detection, modify the code in `generate_frames()`:

```python
if detected != "None" and confidence > 0.4:  # Adjust this threshold
    current_gesture = detected
```

### Customizing the Web Interface

The web interface can be customized by modifying files in the `yolo_webserver/public` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for the YOLO implementation
- [Flask](https://flask.palletsprojects.com/) for the Python web framework
- [Express.js](https://expressjs.com/) for the Node.js web framework

---

*This project was created for educational purposes to learn about computer vision and machine learning. It is a WIP.*