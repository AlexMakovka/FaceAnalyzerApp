import cv2
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from analyzer import analyze_face
from utils import save_frame, log_result, create_statistics_figure

class FaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Analyzer")
        self.configure(bg='black')

        self.video_frame = tk.Frame(self, bg='black')
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)

        self.controls_frame = tk.Frame(self, bg='black')
        self.controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        self.panel = tk.Label(self.video_frame)
        self.panel.pack()

        self.lbl_count = tk.Label(self.controls_frame, text="Лиц: 0", font=("Arial", 14), fg='white', bg='black')
        self.lbl_count.pack(anchor='w', pady=5)

        self.lbl_gender = tk.Label(self.controls_frame, text="Пол: —", font=("Arial", 14), fg='white', bg='black')
        self.lbl_gender.pack(anchor='w', pady=5)

        self.lbl_age = tk.Label(self.controls_frame, text="Возраст: —", font=("Arial", 14), fg='white', bg='black')
        self.lbl_age.pack(anchor='w', pady=5)

        self.lbl_emotion = tk.Label(self.controls_frame, text="Эмоция: —", font=("Arial", 14), fg='white', bg='black')
        self.lbl_emotion.pack(anchor='w', pady=5)

        self.btn_start = tk.Button(self.controls_frame, text="▶ Старт", width=12, command=self.start_video,
                                   bg='gray20', fg='white', font=("Arial", 12))
        self.btn_start.pack(fill='x', pady=5)

        self.btn_stop = tk.Button(self.controls_frame, text="⏸ Стоп", width=12, command=self.stop_video,
                                  bg='gray20', fg='white', font=("Arial", 12))
        self.btn_stop.pack(fill='x', pady=5)

        self.btn_save = tk.Button(self.controls_frame, text="💾 Сохранить", width=12, command=self.save_image,
                                  bg='gray20', fg='white', font=("Arial", 12))
        self.btn_save.pack(fill='x', pady=5)

        self.btn_stats = tk.Button(self.controls_frame, text="☑ Статистика", width=12, command=self.show_statistics,
                                   bg='gray20', fg='white', font=("Arial", 12))
        self.btn_stats.pack(fill='x', pady=5)

        self.btn_exit = tk.Button(self.controls_frame, text="❌ Выйти", width=12, command=self.on_close,
                                  bg='gray20', fg='white', font=("Arial", 12))
        self.btn_exit.pack(fill='x', pady=5)

        self.vs = None
        self.thread = None
        self.stop_event = threading.Event()
        self.current_frame = None
        self.N = 5
        self.frame_count = 0

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_video(self):
        if self.vs is None:
            self.vs = cv2.VideoCapture(0)
            if not self.vs.isOpened():
                messagebox.showerror("Ошибка", "Не удалось открыть камеру.")
                return
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.video_loop, daemon=True)
            self.thread.start()

    def video_loop(self):
        while not self.stop_event.is_set():
            ret, frame = self.vs.read()
            if not ret:
                break
            self.current_frame = frame.copy()
            self.frame_count += 1
            analysis = None

            if self.frame_count % self.N == 0:
                analysis = analyze_face(frame)

                if analysis:
                    x, y, w, h = analysis['region']
                    gender = analysis['gender']
                    age = analysis['age']
                    emotion = analysis['emotion']

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = f"{gender}, {age}, {emotion}"
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2)

                    log_result(gender, age, emotion)
                    self.lbl_gender.config(text=f"Пол: {gender}")
                    self.lbl_age.config(text=f"Возраст: {age}")
                    self.lbl_emotion.config(text=f"Эмоция: {emotion}")
                    self.lbl_count.config(text="Лиц: 1")
                else:
                    self.lbl_gender.config(text="Пол: —")
                    self.lbl_age.config(text="Возраст: —")
                    self.lbl_emotion.config(text="Эмоция: —")
                    self.lbl_count.config(text="Лиц: 0")

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image_tk = ImageTk.PhotoImage(image)
            self.panel.config(image=image_tk)
            self.panel.image = image_tk

        if self.vs is not None:
            self.vs.release()
            self.vs = None

    def stop_video(self):
        self.stop_event.set()

    def save_image(self):
        if self.current_frame is not None:
            save_frame(self.current_frame)
            messagebox.showinfo("Сохранено", "Кадр сохранён в папку captures.")
        else:
            messagebox.showwarning("Ошибка", "Нет кадра для сохранения.")

    def show_statistics(self):
        fig = create_statistics_figure()
        if fig:
            fig.show()
        else:
            messagebox.showinfo("Статистика", "Нет данных для отображения статистики.")

    def on_close(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=1)
        if self.vs is not None:
            self.vs.release()
        self.destroy()