# Hand Gesture Controlled Drawing Application

This project is a hand gesture-controlled drawing application that utilizes OpenCV and MediaPipe to detect hand movements and gestures. The application allows users to draw on a virtual canvas using their fingers. The index and middle fingers are used for selecting colors or the eraser, while the index finger alone is used for drawing.

## Features

- **Hand Detection**: Detects hands and hand landmarks using MediaPipe.
- **Drawing**: Draw on the screen using the index finger.
- **Color Selection**: Change brush color by selecting from a predefined palette using both the index and middle fingers.
- **Eraser**: Erase parts of the drawing using the eraser tool.
- **Real-time**: Works in real-time using a webcam.

## Prerequisites

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ganjbakhshali/Hand-Gesture-Controlled-Drawing.git
    cd Hand-Gesture-Controlled-Drawing
    ```

2. Install the required Python packages:
    ```bash
    pip install opencv-python mediapipe numpy
    ```

## Usage

1. Ensure you have a webcam connected to your computer.
2. Place your drawing tool images in the `images` directory.
3. Run the application:
    ```bash
    python virtualPainter.py
    ```

