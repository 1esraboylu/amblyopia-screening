# Eye Symmetry-Based Amblyopia Screening

This is a Python-based desktop application that helps detect possible signs of amblyopia (lazy eye) by analyzing eye symmetry through a webcam.

The tool tracks vertical and horizontal differences between both eyes, gives immediate visual feedback, and logs test results in a `.csv` file. It is designed to support early screening efforts, particularly for children.

---

## 💻 Features

- Real-time eye tracking with webcam
- Measures vertical and horizontal eye symmetry
- Easy GUI interface with Start / Finish Test buttons
- Saves test results with timestamp and name
- Local-only, privacy-respecting design

---

## 🛠 Technologies Used

- Python 3.11+
- OpenCV
- MediaPipe
- Tkinter
- CSV for data logging

---

## 📁 Files

| File | Description |
|------|-------------|
| `amblyopia_gui.py` | Main application |
| `test_results.csv` | Automatically generated after test |
| `requirements.txt` | Required packages |
| `README.md` | This file |

---

## ▶️ How to Run

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
