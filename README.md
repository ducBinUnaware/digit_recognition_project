# 🖊️ Handwritten Digit Recognition System

An end-to-end Machine Learning and Computer Vision application designed to recognize handwritten digits ($0 - 9$) drawn on a canvas in real-time. Built using **TensorFlow/Keras (CNN)**, **OpenCV**, and a **Tkinter Graphical User Interface**.


## 🛠️ Requirements & Installation

### 1. Prerequisites
Make sure you have **Python 3.8 - 3.11** installed on your machine.

### 2. Clone or Download the Repository
```bash
git clone <repository_url>
cd digit_recognition_project
```

### 3. Create a Virtual Environment (Optional but Recommended)

* **Windows:**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install all required libraries using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Guide

### Step 1: Train the CNN Model
If `models/digit_model.h5` is not yet generated, open and execute the training notebook:
```bash
jupyter notebook notebooks/train.ipynb
```
* Execute all cells in `train.ipynb`.
* The notebook includes synthetic data generation for European/Asian-style digit `1` (hooked top / base stroke) to improve recognition accuracy.
* The trained model will automatically save to `models/digit_model.h5`.

### Step 2: Run the GUI Application
Once the model file exists, launch the interactive user interface from the root directory:
```bash
python main.py
```

---

## 🖥️ Application Features

* **Interactive Canvas**: Draw any handwritten digit ($0 - 9$) with white stroke on a dark background.
* **Center of Mass Preprocessing**: Automatically centers and pads drawn numbers to mirror standard MNIST spatial distribution.
* **Confidence Breakdown**: Displays continuous confidence percentages across all 10 digit classes.
* **Model Accuracy Safeguard**: Enhanced against common digit shape misclassifications (e.g., distinguishing complex `1` shapes from `4` and `9`).

---

## ⚙️ Tech Stack

* **Language**: Python 3
* **Deep Learning**: TensorFlow / Keras (Convolutional Neural Networks)
* **Computer Vision**: OpenCV, Pillow, SciPy
* **Data Visualization**: Matplotlib, Seaborn, Scikit-learn
* **GUI Engine**: Tkinter