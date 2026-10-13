import os
import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
from src.preprocess import preprocess_canvas_image

class DigitRecognizerApp:
    def __init__(self, root, model_path="models/digit_model.h5"):
        self.root = root
        self.root.title("Digit Recognition - Neural Network Output")

        self.root.geometry("920x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

        if not os.path.exists(model_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file mô hình tại {model_path}.\nVui lòng chạy notebook huấn luyện trước!")
            self.model = None
        else:
            self.model = tf.keras.models.load_model(model_path)

        self.canvas_size = 320
        self.brush_size = 18

        self.image_pil = Image.new("L", (self.canvas_size, self.canvas_size), color=0)
        self.draw = ImageDraw.Draw(self.image_pil)

        self._build_ui()

    def _build_ui(self):
        title_label = tk.Label(
            self.root, text="Handwritten Digit Recognition", 
            font=("Arial", 20, "bold"), bg="#F0F0F0", fg="#000000"
        )
        title_label.pack(pady=15)

        main_frame = tk.Frame(self.root, bg="#F0F0F0")
        main_frame.pack(padx=15, pady=5, fill="both", expand=True)

        left_frame = tk.LabelFrame(main_frame, text=" Draw a Digit ", font=("Arial", 11, "bold"), bg="#F0F0F0")
        left_frame.pack(side="left", padx=10, pady=5, fill="both")

        self.canvas = tk.Canvas(
            left_frame, width=self.canvas_size, height=self.canvas_size, 
            bg="black", highlightthickness=1, highlightbackground="#CCCCCC"
        )
        self.canvas.pack(padx=15, pady=15)

        self.canvas.bind("<B1-Motion>", self._paint)
        self.canvas.bind("<ButtonPress-1>", self._paint)

        btn_frame = tk.Frame(left_frame, bg="#F0F0F0")
        btn_frame.pack(pady=10)

        clear_btn = tk.Button(btn_frame, text="Clear", font=("Arial", 10), width=10, command=self.clear_canvas)
        clear_btn.grid(row=0, column=0, padx=10)

        predict_btn = tk.Button(btn_frame, text="Predict", font=("Arial", 10, "bold"), width=10, command=self.predict_digit)
        predict_btn.grid(row=0, column=1, padx=10)

        right_frame = tk.LabelFrame(main_frame, text=" Neural Network Output ", font=("Arial", 11, "bold"), bg="#F0F0F0")
        right_frame.pack(side="right", padx=10, pady=5, fill="both", expand=True)

        grid_container = tk.Frame(right_frame, bg="#F0F0F0")
        grid_container.pack(expand=True, pady=15, padx=10)

        self.digit_cards = []
        for i in range(10):
            row = 0 if i < 5 else 1
            col = i % 5

            card = tk.Frame(grid_container, bg="#FFFFFF", relief="solid", bd=1, width=62, height=90)
            card.pack_propagate(False)
            card.grid(row=row, column=col, padx=4, pady=8)

            lbl_num = tk.Label(card, text=str(i), font=("Arial", 20, "bold"), bg="#FFFFFF", fg="#A0A0A0")
            lbl_num.pack(pady=(10, 2))

            lbl_conf = tk.Label(card, text="0.0%", font=("Arial", 8), bg="#FFFFFF", fg="#A0A0A0")
            lbl_conf.pack()

            self.digit_cards.append({"card": card, "num": lbl_num, "conf": lbl_conf})

        self.lbl_prediction = tk.Label(
            self.root, text="Prediction: None (Confidence: 0.0%)", 
            font=("Arial", 15, "bold"), bg="#F0F0F0", fg="#000000"
        )
        self.lbl_prediction.pack(side="bottom", pady=20)

    def _paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")

        self.draw.ellipse([x1, y1, x2, y2], fill=255, outline=255)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image_pil = Image.new("L", (self.canvas_size, self.canvas_size), color=0)
        self.draw = ImageDraw.Draw(self.image_pil)

        for card_info in self.digit_cards:
            card_info["num"].config(fg="#A0A0A0")
            card_info["conf"].config(text="0.0%", fg="#A0A0A0")

        self.lbl_prediction.config(text="Prediction: None (Confidence: 0.0%)")

    def predict_digit(self):
        if self.model is None:
            messagebox.showerror("Lỗi", "Mô hình chưa được tải!")
            return

        input_data = preprocess_canvas_image(self.image_pil)


        predictions = self.model.predict(input_data)[0]
        predicted_digit = int(np.argmax(predictions))
        max_confidence = predictions[predicted_digit] * 100

        for i in range(10):
            conf_val = predictions[i] * 100
            card_info = self.digit_cards[i]

            card_info["conf"].config(text=f"{conf_val:.1f}%")

            if i == predicted_digit:

                card_info["num"].config(fg="#008000")  
                card_info["conf"].config(fg="#008000")
            else:
                card_info["num"].config(fg="#A0A0A0")
                card_info["conf"].config(fg="#A0A0A0")

        self.lbl_prediction.config(
            text=f"Prediction: {predicted_digit} (Confidence: {max_confidence:.1f}%)"
        )