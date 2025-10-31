# FaceAnalyzerApp

An interactive face analysis application with a graphical interface.
It allows users to load images or videos, detect faces, analyze them, and save the results in CSV format.
Captured frames are automatically saved in the `captures` folder.

> ⚠️ Note: The description is based on the repository structure.
> You can adjust the *Features* and *Technologies* sections if your implementation differs.

---

## 🚀 Features

* 📷 Use a webcam/video input (GUI: `gui.py`)
* 🙂 Face detection and basic metric extraction (`analyzer.py`)
* 💾 Export results to `results.csv`
* 🖼️ Save analyzed frames to the `captures/` folder
* ⚙️ Utility functions for processing (`utils.py`)

---

## 📂 Project Structure

```
FaceAnalyzerApp/
├─ Main.py            # Entry point of the app
├─ gui.py             # GUI: forms, buttons, event handlers
├─ analyzer.py        # Face detection and analysis logic
├─ utils.py           # Helper functions and utilities
├─ requirements.txt   # Python dependencies
├─ results.csv        # Example / output CSV file
└─ captures/          # Saved image frames
```

---

## 🧠 Demo

* Example captured frames: [`captures/`](./captures)
* Example results: [`results.csv`](./results.csv)

  <img width="1276" height="528" alt="image" src="https://github.com/user-attachments/assets/82ee120b-fabc-4674-adfb-6e9329a50d53" />


---

## 🧩 Requirements

* Python **3.9+** (recommended: 3.10 or 3.11)
* OS: Windows, macOS, or Linux
* System libraries for **OpenCV / dlib / MediaPipe**, depending on your setup
  (see `requirements.txt` for exact dependencies)

---

## ⚙️ Installation

```bash
# 1) Clone the repository
git clone https://github.com/AlexMakovka/FaceAnalyzerApp.git
cd FaceAnalyzerApp

# 2) Create and activate a virtual environment
python -m venv .venv
. .venv/Scripts/Activate.ps1  # Windows PowerShell

# macOS / Linux:
# python3 -m venv .venv
# source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python Main.py
```

A graphical window will open.
Select your input source (image, video, or webcam), perform the analysis, and save results as needed.

---

## 💡 Usage Guide

1. Launch the app using `python Main.py`.
2. Choose your input (image/video/webcam) in the GUI.
3. Click **Analyze** to start detection.
4. View results directly in the interface.
5. Save:

   * Results table → `results.csv`
   * Image frames → `captures/`

---

## ⚙️ Configuration

* Thresholds, file paths, or export options (if applicable) can be adjusted inside
  `utils.py`, `analyzer.py`, or `gui.py`.
* You can also create a `config.example.yaml` or `.json` for reusable settings.

---

## 🧰 Technologies Used

* **Python**
* **OpenCV / MediaPipe / dlib** for face analysis
* **NumPy / Pandas** for data processing

---

## 📑 Data Output

* **`results.csv`** — contains detected face data.
* **`captures/`** — stores the saved or annotated frames.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch `feature/...`
3. Open a Pull Request describing your changes
