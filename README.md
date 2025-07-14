# 🎥 Virtual Background Application

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-enabled-green)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-SelfieSegmentation-orange)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A simple and powerful desktop application that allows users to apply **virtual backgrounds** or **blur effects** to their webcam video in real-time and record the output. Built with **OpenCV**, **MediaPipe**, and a user-friendly **Tkinter GUI**.

---

## ✨ Features

- 🖼️ Apply a custom **image or looping video** as your virtual background
- 🔍 Use **real-time background blur** without needing a green screen
- 🎥 Preview webcam feed live before recording
- 💾 Record and save the output video (`.avi` format)
- 🎛️ Easy-to-use desktop GUI with mode selection

---

## SCREENSHOTS ##
![image ult](https://github.com/reyansh2002/Virtual-Background-Application/blob/d99c2e9cc0fcdd09b2681af22d70989549bddf8d/%F0%9F%8E%A5%20Virtual%20Background%20Recorder%2004-05-2025%2022_31_50.png)




## 🛠️ Tech Stack

- **Language**: Python 3
- **GUI**: Tkinter
- **Video Processing**: OpenCV
- **Segmentation**: MediaPipe Selfie Segmentation
- **Data Handling**: NumPy

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/virtual-background-app.git
   cd virtual-background-app
   
2. **Install dependencies**

   ```bash
   pip install opencv-python mediapipe numpy

## 🚀 Usage

   Run the application:

   ```bash
    python g.py
   ```

**In the GUI:**

1. Choose a background mode:

     -Virtual Background – select an image/video file as your background

     -Blur Background – blur the real-time background

2. Click Pick Background (only for virtual mode)

3. Click Preview Webcam to see live feed

4. Click Start Recording to begin capturing video

5. Press q in the preview window to stop recording

📂 The final video is saved as output_virtual_background.avi in the current directory.

---

## 🧠 How It Works ##

1. Utilizes MediaPipe Selfie Segmentation to separate the foreground (person) from the background.

2. Applies:

   -Gaussian Blur for the blur effect.

   -A user-selected image or video as the virtual background.

3. Captures and writes the final video using OpenCV VideoWriter.

---

## 📁 Project Structure ##

```bash

📁 virtual-background-app/
├── g.py                       # Main application script
├── output_virtual_background.avi  # Output file after recording
```
---

## ❗ Requirements ##

Python 3.7+

Webcam access

Supported image/video file formats for virtual background:

Images: .jpg, .jpeg, .png

Videos: .mp4, .avi, .mov

---

## 🙌 Acknowledgements ##

MediaPipe by Google

OpenCV

Tkinter – Python GUI Library






