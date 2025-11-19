# 🎭 Face Expression Recognizer

A modern, user-friendly desktop application for facial expression recognition using computer vision and machine learning. Built with Python, OpenCV, MediaPipe, and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **📸 Dataset Generation**: Capture facial expressions in real-time using your webcam
- **🧠 Model Training**: Train a custom classifier on your collected expressions
- **🔍 Real-time Recognition**: Detect and classify facial expressions with confidence scores
- **🎨 Modern UI**: Dark-themed, intuitive interface with emoji icons
- **⚡ Fast Processing**: Powered by MediaPipe for efficient face detection

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Webcam

### Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python face_recognizer_gui.py
```

## 📖 How to Use

### 1. Generate Dataset

1. Click **"📸 Generate Dataset"**
2. Enter an expression label (e.g., `happy`, `sad`, `angry`, `surprised`, `neutral`)
3. Position your face in front of the camera
4. The app will automatically capture 200 images of your expression
5. Click **"⏹️ Stop"** to finish early if needed
6. Repeat for different expressions (recommended: at least 3-5 expressions)

### 2. Train Classifier

1. After collecting datasets for multiple expressions, click **"🧠 Train Classifier"**
2. Wait for the training to complete (usually takes a few seconds)
3. You'll see a success message when training is done

### 3. Recognize Expressions

1. Click **"🔍 Recognize Expression"**
2. Your webcam will activate and start detecting expressions in real-time
3. The app will display:
   - Green bounding box around detected faces
   - Expression label with confidence percentage
4. Click **"⏹️ Stop"** when finished

## 📁 Project Structure

```
face-expression-recognizer/
├── face_recognizer_gui.py      # Main application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── data/                        # Generated datasets (created automatically)
│   ├── happy/
│   ├── sad/
│   └── ...
├── expression_classifier.xml    # Trained model (created after training)
└── label_map.txt               # Expression labels mapping (created after training)
```

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Tkinter**: GUI framework
- **OpenCV**: Computer vision and image processing
- **MediaPipe**: Face detection
- **PIL (Pillow)**: Image handling
- **NumPy**: Numerical operations

## 💡 Tips for Best Results

- **Good Lighting**: Ensure your face is well-lit for better detection
- **Multiple Angles**: Capture expressions from slightly different angles
- **Exaggerate Expressions**: Make clear, distinct facial expressions
- **Variety**: Train with at least 3-5 different expressions
- **Consistency**: Keep similar distance from camera during capture

## 🎯 Recommended Expressions

- Happy 😊
- Sad 😢
- Angry 😠
- Surprised 😲
- Neutral 😐
- Fearful 😨
- Disgusted 🤢

## ⚙️ Technical Details

- **Face Detection**: MediaPipe Face Detection (model_selection=1)
- **Classifier**: LBPH (Local Binary Patterns Histograms) Face Recognizer
- **Image Size**: 48x48 pixels (grayscale) for training
- **Recognition Size**: 200x200 pixels for prediction
- **Dataset Size**: Up to 200 images per expression

## 🐛 Troubleshooting

**Camera not working?**
- Check if your webcam is connected and not being used by another application
- Try restarting the application

**Low accuracy?**
- Collect more training images (at least 150-200 per expression)
- Ensure good lighting conditions
- Make distinct facial expressions
- Retrain the classifier with more varied data

**Application not starting?**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Created with ❤️ using Python and OpenCV

---

**Powered by OpenCV & MediaPipe**
