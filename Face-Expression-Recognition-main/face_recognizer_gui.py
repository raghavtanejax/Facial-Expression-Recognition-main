import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import threading
from collections import deque, Counter
import time


class FaceRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Expression Recognizer")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set to fullscreen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')  # Maximize window on Windows
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e2e")

        self.is_running = False
        self.current_mode = None
        self.cap = None
        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        if self.face_detector.empty():
            raise RuntimeError("Unable to load Haar cascade. Ensure OpenCV data files are installed.")

        self.prev_frame = None
        self.prediction_buffer = deque(maxlen=15)
        self.primary_color = "#5cf4ff"
        self.secondary_color = "#0f172a"

        self.expression_var = tk.StringVar(value="Awaiting Signal")
        self.confidence_var = tk.StringVar(value="0% confidence")
        self.capture_state = tk.StringVar(value="Camera idle")
        self.fps_var = tk.StringVar(value="0 fps")

        self.frames_processed = 0
        self.last_frame_time = time.time()
        self.frames_shown = 0
        self.metric_labels = {}

        # Setup UI
        self.setup_styles()
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#05060d")

        main_frame = tk.Frame(self.root, bg="#05060d")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        headline_frame = tk.Frame(main_frame, bg="#05060d")
        headline_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        tk.Label(
            headline_frame,
            text="Zenith Emotion Studio",
            font=("Space Grotesk", 28, "bold"),
            fg="white",
            bg="#05060d",
        ).pack(side=tk.LEFT)

        badge = tk.Label(
            headline_frame,
            text="LIVE VISION STACK",
            font=("Segoe UI", 10, "bold"),
            fg=self.primary_color,
            bg="#11182c",
            padx=20,
            pady=8,
        )
        badge.pack(side=tk.RIGHT)

        hero_panel = tk.Frame(main_frame, bg="#0a1324", bd=0, highlightbackground="#13203c", highlightthickness=1)
        hero_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        hero_panel.grid_rowconfigure(1, weight=1)

        hero_text = tk.Frame(hero_panel, bg="#0a1324")
        hero_text.pack(fill=tk.X, padx=24, pady=24)

        tk.Label(
            hero_text,
            text="Decode human emotion streams in realtime.",
            font=("Space Grotesk", 22, "bold"),
            fg="white",
            bg="#0a1324",
        ).pack(anchor="w")
        tk.Label(
            hero_text,
            text="Collect datasets, train the classifier, and monitor expressions from a single luxury dashboard.",
            font=("Segoe UI", 11),
            fg="#9db4d6",
            bg="#0a1324",
            wraplength=420,
            justify=tk.LEFT,
            pady=6,
        ).pack(anchor="w")

        control_frame = tk.Frame(hero_panel, bg="#0a1324")
        control_frame.pack(fill=tk.X, padx=24, pady=(0, 24))
        control_frame.grid_columnconfigure((0, 1), weight=1)

        button_config = {
            "font": ("Segoe UI", 11, "bold"),
            "height": 2,
            "relief": tk.FLAT,
            "cursor": "hand2",
            "bd": 0,
        }

        self.generate_btn = tk.Button(
            control_frame,
            text="📸 Generate Dataset",
            command=self.start_generate_dataset,
            bg="#1dd6b9",
            fg="#05060d",
            activebackground="#14b89f",
            activeforeground="#05060d",
            **button_config,
        )
        self.generate_btn.grid(row=0, column=0, padx=8, pady=6, sticky="ew")

        self.train_btn = tk.Button(
            control_frame,
            text="🧠 Train Classifier",
            command=self.train_classifier,
            bg="#2a7fff",
            fg="white",
            activebackground="#246ae0",
            activeforeground="white",
            **button_config,
        )
        self.train_btn.grid(row=0, column=1, padx=8, pady=6, sticky="ew")

        self.recognize_btn = tk.Button(
            control_frame,
            text="🔍 Recognize",
            command=self.start_recognition,
            bg="#ffb545",
            fg="#05060d",
            activebackground="#e79e2a",
            activeforeground="#05060d",
            **button_config,
        )
        self.recognize_btn.grid(row=1, column=0, padx=8, pady=6, sticky="ew")

        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop Stream",
            command=self.stop_camera,
            bg="#ff5e5b",
            fg="white",
            activebackground="#d94d4a",
            activeforeground="white",
            state=tk.DISABLED,
            **button_config,
        )
        self.stop_btn.grid(row=1, column=1, padx=8, pady=6, sticky="ew")

        metrics_frame = tk.Frame(hero_panel, bg="#0a1324")
        metrics_frame.pack(fill=tk.X, padx=24, pady=(0, 24))
        metrics_frame.grid_columnconfigure((0, 1), weight=1)

        self.metric_labels = {
            "expression": self._create_metric_card(metrics_frame, "CURRENT EMOTION", "—", 0),
            "confidence": self._create_metric_card(metrics_frame, "CONFIDENCE", "0%", 1),
        }

        right_panel = tk.Frame(main_frame, bg="#05060d")
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        right_panel.grid_rowconfigure(1, weight=1)

        video_card = tk.Frame(right_panel, bg="#0f172a", bd=0, highlightbackground="#172750", highlightthickness=1)
        video_card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))

        video_header = tk.Frame(video_card, bg="#0f172a")
        video_header.pack(fill=tk.X, padx=20, pady=16)

        tk.Label(
            video_header,
            textvariable=self.expression_var,
            font=("Space Grotesk", 18, "bold"),
            fg="white",
            bg="#0f172a",
        ).pack(anchor="w")
        tk.Label(
            video_header,
            textvariable=self.confidence_var,
            font=("Segoe UI", 10),
            fg="#9db4d6",
            bg="#0f172a",
        ).pack(anchor="w")

        video_container = tk.Frame(video_card, bg="#01030a", width=700, height=420)
        video_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        video_container.pack_propagate(False)

        self.video_frame = tk.Label(video_container, bg="#000000", text="📷", font=("Arial", 48), fg="#4a4a6a")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        dashboard_card = tk.Frame(right_panel, bg="#0f172a", bd=0, highlightbackground="#172750", highlightthickness=1)
        dashboard_card.grid(row=1, column=0, sticky="ew")

        dash_header = tk.Frame(dashboard_card, bg="#0f172a")
        dash_header.pack(fill=tk.X, padx=20, pady=16)

        tk.Label(
            dash_header,
            text="Session Insights",
            font=("Space Grotesk", 16, "bold"),
            fg="white",
            bg="#0f172a",
        ).pack(side=tk.LEFT)
        tk.Label(
            dash_header,
            textvariable=self.capture_state,
            font=("Segoe UI", 10),
            fg=self.primary_color,
            bg="#0f172a",
        ).pack(side=tk.RIGHT)

        stats_grid = tk.Frame(dashboard_card, bg="#0f172a")
        stats_grid.pack(fill=tk.X, padx=20, pady=(0, 20))
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)

        self.metric_labels["frames"] = self._create_stat_chip(
            stats_grid, "Frames", "0", 0
        )
        self.metric_labels["fps"] = self._create_stat_chip(stats_grid, "Frame Rate", "0 fps", 1)
        self.metric_labels["mode"] = self._create_stat_chip(stats_grid, "Mode", "Idle", 2)

        self.status_label = tk.Label(
            dashboard_card,
            text="Ready",
            font=("Segoe UI", 11, "bold"),
            fg="#1dd6b9",
            bg="#0f172a",
            pady=4,
        )
        self.status_label.pack(anchor="w", padx=20)

        self.info_label = tk.Label(
            dashboard_card,
            text="",
            font=("Segoe UI", 10),
            fg="#9db4d6",
            bg="#0f172a",
            wraplength=500,
            pady=6,
        )
        self.info_label.pack(anchor="w", padx=20, pady=(0, 20))

        footer = tk.Label(
            self.root,
            text="Crafted with OpenCV + Tkinter",
            font=("Segoe UI", 9),
            bg="#05060d",
            fg="#53607c",
        )
        footer.pack(side=tk.BOTTOM, pady=6)

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", background="#0a1324", foreground="white")
        style.configure("Card.TFrame", background="#0f172a", borderwidth=0)
        style.configure("Stat.TLabel", background="#0f172a", foreground=self.primary_color, font=("Segoe UI", 10, "bold"))

    def _create_metric_card(self, parent, title, value, column):
        card = tk.Frame(parent, bg="#111b33", highlightbackground="#1c2b4f", highlightthickness=1)
        card.grid(row=0, column=column, padx=8, sticky="ew")

        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#7488b0", bg="#111b33").pack(anchor="w", padx=16, pady=(16, 0))
        label = tk.Label(card, text=value, font=("Space Grotesk", 20, "bold"), fg="white", bg="#111b33")
        label.pack(anchor="w", padx=16, pady=(4, 16))
        return label

    def _create_stat_chip(self, parent, title, value, column):
        chip = tk.Frame(parent, bg="#111b33", highlightbackground="#1c2b4f", highlightthickness=1)
        chip.grid(row=0, column=column, padx=6, sticky="ew")
        tk.Label(chip, text=title, font=("Segoe UI", 9, "bold"), fg="#7488b0", bg="#111b33").pack(anchor="w", padx=12, pady=(12, 0))
        label = tk.Label(chip, text=value, font=("Space Grotesk", 16, "bold"), fg="white", bg="#111b33")
        label.pack(anchor="w", padx=12, pady=(2, 12))
        return label

    def update_expression_metrics(self, expression, confidence_pct):
        def _update():
            self.expression_var.set(expression.upper())
            self.confidence_var.set(f"{confidence_pct}% confidence")
            if "expression" in self.metric_labels:
                self.metric_labels["expression"].config(text=expression.title())
            if "confidence" in self.metric_labels:
                self.metric_labels["confidence"].config(text=f"{confidence_pct}%")
        self.root.after(0, _update)

    def update_capture_badge(self, text):
        self.root.after(0, lambda: self.capture_state.set(text))

    def update_mode_label(self, text):
        if "mode" in self.metric_labels:
            self.root.after(0, lambda: self.metric_labels["mode"].config(text=text))

    def update_status(self, text, color="#1dd6b9"):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))

    def update_info(self, text):
        self.root.after(0, lambda: self.info_label.config(text=text))

    def update_frame_counter(self, value):
        if "frames" in self.metric_labels:
            self.root.after(0, lambda: self.metric_labels["frames"].config(text=str(value)))

    def update_fps(self, fps_value):
        if "fps" in self.metric_labels:
            self.root.after(0, lambda: self.metric_labels["fps"].config(text=f"{fps_value:.1f} fps"))

    def start_generate_dataset(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Please stop the current operation first")
            return

        # Custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Expression Label")
        dialog.geometry("400x200")
        dialog.configure(bg="#2d2d44")
        dialog.resizable(False, False)

        tk.Label(
            dialog,
            text="Enter Expression Label",
            font=("Segoe UI", 14, "bold"),
            bg="#2d2d44",
            fg="white",
        ).pack(pady=20)

        tk.Label(
            dialog,
            text="(e.g., happy, sad, angry, surprised)",
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#9ca3af",
        ).pack()

        entry = tk.Entry(dialog, font=("Segoe UI", 12), width=25, bg="#1e1e2e", fg="white", insertbackground="white")
        entry.pack(pady=15)
        entry.focus()

        result = {"expression": None}

        def on_ok():
            result["expression"] = entry.get()
            dialog.destroy()

        def on_enter(event):
            on_ok()

        entry.bind("<Return>", on_enter)

        btn_frame = tk.Frame(dialog, bg="#2d2d44")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Start",
            command=on_ok,
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#6b7280",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=10,
            relief=tk.FLAT,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

        expression = result["expression"]
        if not expression:
            return

        expression = expression.strip().lower()
        self.current_mode = "generate"
        self.expression_label = expression
        self.img_id = 0
        self.prev_frame = None
        self.frames_shown = 0
        self.frames_processed = 0
        self.last_frame_time = time.time()

        # Create folder
        self.expression_folder = os.path.join("data", expression)
        if not os.path.exists(self.expression_folder):
            os.makedirs(self.expression_folder)

        self.is_running = True
        self.toggle_buttons(False)
        self.update_mode_label("Dataset")
        self.update_capture_badge(f"Collecting • {expression}")
        self.update_status(f"Collecting '{expression}' expressions...", "#ffb545")
        self.update_info("📸 Press 'Stop' or collect 200 images to finish")

        threading.Thread(target=self.generate_dataset_loop, daemon=True).start()

    def generate_dataset_loop(self):
        self.cap = cv2.VideoCapture(0)

        while self.is_running and self.img_id < 200:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60))

            for (x, y, w_box, h_box) in faces:
                self.img_id += 1

                cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (16, 185, 129), 3)
                cv2.putText(
                    frame,
                    f"Captured: {self.img_id}/200",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (16, 185, 129),
                    3,
                )

                cropped_face = frame[y : y + h_box, x : x + w_box]
                if cropped_face.size > 0:
                    cropped_face = cv2.resize(cropped_face, (48, 48))
                    gray_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)
                    file_name_path = os.path.join(
                        self.expression_folder, f"{self.expression_label}_{self.img_id}.jpg"
                    )
                    cv2.imwrite(file_name_path, gray_face)
                    self.update_frame_counter(self.img_id)

            self.display_frame(frame)

        self.stop_camera()
        self.update_status("Dataset collection complete", "#1dd6b9")
        self.update_mode_label("Idle")
        self.update_capture_badge("Camera idle")
        self.root.after(
            0,
            lambda: messagebox.showinfo(
                "Complete", f"✅ Collection for '{self.expression_label}' completed!\n{self.img_id} images saved."
            ),
        )

    def start_recognition(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Please stop the current operation first")
            return

        if not os.path.exists("expression_classifier.xml"):
            messagebox.showerror("Error", "❌ Classifier not found.\nPlease train the classifier first.")
            return

        self.current_mode = "recognize"
        self.is_running = True
        self.toggle_buttons(False)
        self.update_mode_label("Recognition")
        self.update_capture_badge("Recognizing • live stream")
        self.update_status("Recognizing expressions...", "#ffb545")
        self.update_info("🔍 Press 'Stop' to finish")
        self.prediction_buffer.clear()
        self.prev_frame = None
        self.frames_shown = 0
        self.frames_processed = 0
        self.last_frame_time = time.time()

        threading.Thread(target=self.recognition_loop, daemon=True).start()

    def recognition_loop(self):
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("expression_classifier.xml")

        label_map = self.load_label_map()

        self.cap = cv2.VideoCapture(0)

        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = self.draw_expression(frame, clf, label_map)
            self.display_frame(frame)

        self.stop_camera()

    def draw_expression(self, img, clf, label_map):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60))

        for (x, y, w_box, h_box) in faces:
            face_region = img[y : y + h_box, x : x + w_box]
            if face_region.size == 0:
                continue

            face_gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.resize(face_gray, (200, 200))

            label, confidence = clf.predict(face_gray)
            stable = self.update_prediction_buffer(label, confidence)
            if not stable:
                continue

            stable_label, avg_confidence = stable
            confidence_pct = max(0, min(100, int(100 * (1 - avg_confidence / 400))))

            expression = label_map.get(stable_label, "Unknown")
            display_text = f"{expression.upper()} ({confidence_pct}%)"
            self.update_expression_metrics(expression, confidence_pct)

            cv2.rectangle(img, (x, y), (x + w_box, y + h_box), (16, 185, 129), 3)

            text_size = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            cv2.rectangle(img, (x, y - 35), (x + text_size[0] + 10, y), (16, 185, 129), -1)

            cv2.putText(img, display_text, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return img

    def update_prediction_buffer(self, label, confidence):
        self.prediction_buffer.append((label, confidence))
        if len(self.prediction_buffer) < 4:
            return None

        label_counts = Counter(lbl for lbl, _ in self.prediction_buffer)
        best_label, count = label_counts.most_common(1)[0]

        required = max(4, len(self.prediction_buffer) // 2)
        if count < required:
            return None

        avg_conf = np.mean([conf for lbl, conf in self.prediction_buffer if lbl == best_label])
        return best_label, avg_conf

    def load_label_map(self, filepath="label_map.txt"):
        label_map = {}
        try:
            with open(filepath, "r") as f:
                for line in f:
                    label, expression = line.strip().split(":")
                    label_map[int(label)] = expression
        except Exception as e:
            print("Error loading label map:", e)
        return label_map

    def train_classifier(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Please stop the current operation first")
            return

        if not os.path.exists("data"):
            messagebox.showerror("Error", "❌ No data folder found.\nPlease generate dataset first.")
            return

        self.update_info("🧠 This may take a moment...")
        self.update_status("Training classifier...", "#5cf4ff")
        self.update_mode_label("Training")
        self.update_capture_badge("Training pipeline")
        self.toggle_buttons(False)

        threading.Thread(target=self.train_classifier_thread, daemon=True).start()

    def train_classifier_thread(self):
        try:
            faces = []
            labels = []
            label_map = {}
            current_label = 0

            for expression in os.listdir("data"):
                expression_path = os.path.join("data", expression)
                if not os.path.isdir(expression_path):
                    continue

                label_map[expression] = current_label

                for image_file in os.listdir(expression_path):
                    try:
                        img_path = os.path.join(expression_path, image_file)
                        img = Image.open(img_path).convert("L")
                        img_np = np.array(img, "uint8")
                        faces.append(img_np)
                        labels.append(current_label)
                    except Exception as e:
                        continue

                current_label += 1

            labels = np.array(labels, dtype=np.int32)

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, labels)
            clf.write("expression_classifier.xml")

            with open("label_map.txt", "w") as f:
                for expression, label in label_map.items():
                    f.write(f"{label}:{expression}\n")

            self.update_status("Training completed!", "#1dd6b9")
            self.update_info("")
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", f"✅ Classifier trained successfully!\n{len(label_map)} expressions learned."
                ),
            )
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"❌ Training failed:\n{str(e)}"))
            self.update_status("Training failed", "#ff5e5b")
        finally:
            self.root.after(0, lambda: self.toggle_buttons(True))
            self.update_mode_label("Idle")
            self.update_capture_badge("Camera idle")

    def display_frame(self, frame):
        self.frames_shown += 1
        self.update_frame_counter(self.frames_shown)

        self.frames_processed += 1
        elapsed = time.time() - self.last_frame_time
        if elapsed >= 1:
            fps_value = self.frames_processed / elapsed
            self.update_fps(fps_value)
            self.frames_processed = 0
            self.last_frame_time = time.time()

        if self.prev_frame is not None and self.prev_frame.shape == frame.shape:
            frame = cv2.addWeighted(frame, 0.72, self.prev_frame, 0.28, 0)
        self.prev_frame = frame.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk, text="")

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.prev_frame = None
        self.prediction_buffer.clear()
        self.frames_shown = 0
        self.frames_processed = 0
        self.update_frame_counter(0)
        self.update_fps(0.0)
        self.update_capture_badge("Camera idle")
        self.update_mode_label("Idle")
        self.video_frame.configure(image="", text="📷", font=("Arial", 48), fg="#4a4a6a")
        self.update_status("Ready", "#1dd6b9")
        self.update_info("")
        self.toggle_buttons(True)

    def toggle_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.generate_btn.config(state=state)
        self.train_btn.config(state=state)
        self.recognize_btn.config(state=state)
        self.stop_btn.config(state=tk.DISABLED if enabled else tk.NORMAL)

    def on_closing(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognizerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
