import tkinter as tk
from src.gui import DigitRecognizerApp

def main():
    root = tk.Tk()
    app = DigitRecognizerApp(root, model_path="models/digit_model.h5")
    root.mainloop()

if __name__ == "__main__":
    main()