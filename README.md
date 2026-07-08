# Emotion Detection Using CNN

## Overview

This project implements a **Convolutional Neural Network (CNN)** for facial emotion recognition using grayscale facial images. The model is trained to classify images into seven different emotion categories using TensorFlow and Keras.

## Features

- Image preprocessing and normalization
- Grayscale image classification
- CNN architecture built with TensorFlow/Keras
- Training with validation split
- Model evaluation on test dataset
- Emotion prediction for new images
- Training and validation accuracy/loss visualization
- Model saving for future inference

## Emotion Classes

| Label | Emotion |
|--------|----------|
| 0 | Angry |
| 1 | Disgust |
| 2 | Fear |
| 3 | Happy |
| 4 | Sad |
| 5 | Surprise |
| 6 | Neutral |

## Project Structure

```
project/
│
├── images/
│   ├── train/
│   │   ├── 0/
│   │   ├── 1/
│   │   ├── ...
│   │   └── 6/
│   │
│   └── test/
│       ├── 0/
│       ├── 1/
│       ├── ...
│       └── 6/
│
├── model/
│   └── emotion_detection_model.h5
│
├── cnn.ipynb
└── README.md
```

## Technologies Used

- Python
- TensorFlow
- Keras
- NumPy
- OpenCV
- Matplotlib
- Scikit-learn

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/emotion-detection-cnn.git
cd emotion-detection-cnn
```

Install the required dependencies:

```bash
pip install tensorflow keras numpy opencv-python matplotlib scikit-learn
```

## Dataset

The dataset should be organized as follows:

```
images/
├── train/
│   ├── 0/
│   ├── 1/
│   ├── 2/
│   ├── 3/
│   ├── 4/
│   ├── 5/
│   └── 6/
│
└── test/
    ├── 0/
    ├── 1/
    ├── 2/
    ├── 3/
    ├── 4/
    ├── 5/
    └── 6/
```

Each folder contains facial images belonging to its corresponding emotion class.

## Model Architecture

The CNN consists of:

- Conv2D (64 filters)
- MaxPooling2D
- Dropout (0.25)

- Conv2D (128 filters)
- MaxPooling2D
- Dropout (0.25)

- Conv2D (256 filters)
- MaxPooling2D
- Dropout (0.25)

- Flatten Layer

- Dense Layer (128 neurons)
- Dropout (0.5)

- Output Layer (7 neurons, Softmax activation)

## Training

The model uses:

- Optimizer: Adam
- Learning Rate: 0.0001
- Loss Function: Categorical Crossentropy
- Batch Size: 32
- Epochs: 10
- Validation Split: 20%

Run the notebook:

```bash
jupyter notebook cnn.ipynb
```

or

```bash
jupyter lab
```

## Model Evaluation

After training, the model is evaluated on the test dataset.

Example output:

```
Test accuracy: XX.XX%
```

The trained model is saved as:

```
model/emotion_detection_model.h5
```

## Predicting Emotion

The notebook includes a `predict_emotion()` function that predicts the emotion of a new facial image.

Example:

```python
emotion = predict_emotion("sample.jpg")
print(emotion)
```

## Results

The notebook generates plots for:

- Training Accuracy
- Validation Accuracy
- Training Loss
- Validation Loss

These graphs help monitor the learning performance of the CNN during training.

## Future Improvements

- Increase dataset size
- Apply data augmentation
- Use transfer learning models
- Hyperparameter tuning
- Real-time emotion detection using webcam
- Improve prediction accuracy with deeper architectures

## Author

Developed as a CNN-based facial emotion recognition project using TensorFlow and Keras.
