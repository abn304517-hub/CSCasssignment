# Eye Masker Application – Code Explanation

## Overview

This Python program uses **OpenCV (cv2)** and a webcam to detect a person's face and eyes in real time. When eyes are detected, the application draws solid purple circles over them, effectively masking the eyes.

---

# Import Statement

```python
import cv2
```

- Imports the OpenCV library.
- OpenCV provides tools for image processing, video capture, object detection, and drawing graphics.

---

# Class Definition

```python
class EyeMaskerApp:
```

The application is organized into a class called `EyeMaskerApp`.

Benefits:
- Keeps related code together.
- Makes the program easier to maintain and extend.

---

# Constructor (`__init__`)

```python
def __init__(self):
```

Runs automatically when an object of the class is created.

## Initialize Webcam

```python
self.cap = cv2.VideoCapture(0)
```

- Opens the default webcam.
- `0` represents the first camera connected to the computer.

---

## Load Haar Cascade Classifiers

### Face Detector

```python
self.face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
```

### Eye Detector

```python
self.eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)
```

These XML files contain pre-trained Haar Cascade models used for object detection.

- Face cascade detects faces.
- Eye cascade detects eyes.

---

## Verify Classifiers Loaded Correctly

```python
if self.face_cascade.empty() or self.eye_cascade.empty():
    raise IOError("Unable to load one or more cascade classifier XML files.")
```

Checks whether the XML files were loaded successfully.

If not:
- An error is raised.
- The application stops immediately.

---

# Main Processing Loop

```python
def run(self):
```

This method starts the application.

---

## Display Instructions

```python
print("Eye Masker Started.")
print("Press 'q' to Quit")
```

Displays information to the user.

---

## Infinite Loop

```python
while True:
```

Continuously:
1. Captures webcam frames.
2. Detects faces.
3. Detects eyes.
4. Draws masks.
5. Displays results.

---

# Capture Frame

```python
ret, frame = self.cap.read()
```

- `ret` indicates success or failure.
- `frame` contains the captured image.

---

## Handle Camera Failure

```python
if not ret:
    print("Failed to grab frame from camera.")
    break
```

Stops the application if the camera cannot provide a frame.

---

# Mirror the Image

```python
frame = cv2.flip(frame, 1)
```

Flips the frame horizontally.

Reason:
- Creates a mirror-like effect.
- Feels more natural for users.

---

# Convert to Grayscale

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

Converts the image from color to grayscale.

Why?
- Haar Cascade detectors work more efficiently on grayscale images.
- Reduces processing time.

---

# Face Detection

```python
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100, 100)
)
```

Detects all faces in the frame.

### Parameters

#### scaleFactor = 1.1

Searches for faces at multiple sizes.

#### minNeighbors = 5

Higher values reduce false detections.

#### minSize = (100, 100)

Ignores very small detected objects.

---

# Loop Through Detected Faces

```python
for x, y, w, h in faces:
```

Each face is represented by:

- `x` = left position
- `y` = top position
- `w` = width
- `h` = height

---

# Create Face Region of Interest (ROI)

```python
roi_gray = gray[y:y+h, x:x+w]
roi_color = frame[y:y+h, x:x+w]
```

ROI means **Region of Interest**.

Instead of searching the entire image for eyes:

- Search only inside the face.
- Faster processing.
- Fewer false detections.

---

# Eye Detection

```python
eyes = self.eye_cascade.detectMultiScale(
    roi_gray,
    scaleFactor=1.1,
    minNeighbors=10,
    minSize=(15, 15)
)
```

Detects eyes only within the detected face.

### Parameters

#### minNeighbors = 10

A stricter setting that helps avoid false eye detections.

#### minSize = (15, 15)

Ignores tiny objects.

---

# Loop Through Detected Eyes

```python
for ex, ey, ew, eh in eyes:
```

Each eye is represented by:

- `ex` = x position
- `ey` = y position
- `ew` = width
- `eh` = height

---

# Calculate Circle Position

```python
eye_center = (ex + ew // 2, ey + eh // 2)
```

Computes the center point of the eye.

---

# Calculate Circle Radius

```python
radius = int(max(ew, eh) * 0.6)
```

Uses the larger eye dimension to determine the mask size.

The factor `0.6` slightly enlarges the circle to cover the eye fully.

---

# Draw Eye Mask

```python
cv2.circle(
    roi_color,
    eye_center,
    radius,
    (255, 0, 128),
    thickness=-1
)
```

Draws a solid purple circle.

### Parameters

| Parameter | Meaning |
|------------|---------|
| roi_color | Image to draw on |
| eye_center | Circle center |
| radius | Circle size |
| (255,0,128) | Purple color in BGR |
| thickness=-1 | Fill circle completely |

Result:
- Each detected eye is covered with an opaque purple mask.

---

# Display Result

```python
cv2.imshow("Opaque Eye Masker", frame)
```

Shows the processed video stream in a window titled:

**Opaque Eye Masker**

---

# Exit Condition

```python
if cv2.waitKey(1) & 0xFF == ord("q"):
    break
```

Checks keyboard input.

If the user presses:

```text
q
```

the loop exits.

---

# Cleanup

```python
self.cap.release()
cv2.destroyAllWindows()
```

Releases system resources:

- Stops webcam access.
- Closes all OpenCV windows.

---

# Program Entry Point

```python
if __name__ == "__main__":
    app = EyeMaskerApp()
    app.run()
```

This block runs only when the file is executed directly.

Steps:
1. Create an `EyeMaskerApp` object.
2. Start the application.

---

# Execution Flow Summary

```text
Start Program
      |
      v
Open Webcam
      |
      v
Load Face & Eye Classifiers
      |
      v
Capture Frame
      |
      v
Convert to Grayscale
      |
      v
Detect Faces
      |
      v
Detect Eyes Inside Faces
      |
      v
Draw Purple Eye Masks
      |
      v
Display Frame
      |
      v
Press 'q'?
   |      |
  No      Yes
   |       |
   +-------+
       |
       v
 Release Camera
 Close Windows
 End Program
```

## Key OpenCV Concepts Demonstrated

1. Webcam video capture.
2. Image flipping.
3. Color-to-grayscale conversion.
4. Haar Cascade face detection.
5. Haar Cascade eye detection.
6. Region of Interest (ROI) optimization.
7. Drawing shapes on images.
8. Real-time video processing.
