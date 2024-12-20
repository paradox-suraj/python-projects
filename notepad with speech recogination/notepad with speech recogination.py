import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import speech_recognition as sr
import pyttsx3
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import os

class FloatingTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("\u2728 Floating Task Manager \u2728")
        self.root.geometry("300x500+100+100")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg="#f0f0f0")

        # Custom Fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.task_font = Font(family="Helvetica", size=12)

        # Pyttsx3 Engine Initialization
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Title Header
        title_frame = tk.Frame(self.root, bg="#7289da", relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame, text="\u2728 My Task Manager \u2728", bg="#7289da", fg="white",
            font=self.title_font, pady=10
        )
        title_label.pack()

        # Task Display Frame
        self.scrollable_frame = tk.Frame(self.root, bg="#fefbd8")
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=10)

        # Task Input Box
        self.task_input = tk.Entry(input_frame, font=self.task_font, fg="#333", width=30)
        self.task_input.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)

        # Mic Button
        mic_button = tk.Button(
            input_frame, text="\ud83c\udfa4", bg="#43b581", fg="white",
            font=("Helvetica", 12, "bold"), command=self.start_recording
        )
        mic_button.pack(side=tk.LEFT, padx=10)

        # Add Task Button
        add_task_button = tk.Button(
            input_frame, text="\u2795 Add Task", bg="#43b581", fg="white",
            font=("Helvetica", 10, "bold"), command=self.add_task
        )
        add_task_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Close Button
        close_button = tk.Button(
            self.root, text="\u274c Close", bg="#f04747", fg="white",
            font=("Helvetica", 10, "bold"), command=self.hide_window
        )
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Recording Animation
        self.recording_animation = tk.Label(self.root, text="", bg="#f0f0f0", fg="#f04747", font=("Helvetica", 12))
        self.recording_animation.pack()

        # Inactivity Timer
        self.inactivity_timer = None
        self.inactivity_timeout = 5 * 1000  # 5 seconds to turn invisible
        self.reset_timer()

        # Bind events to reset inactivity timer
        self.root.bind_all("<Motion>", self.reset_timer)
        self.root.bind_all("<Button>", self.reset_timer)
        self.root.bind_all("<KeyPress>", self.reset_timer)

        # Handle click on invisible window
        self.root.bind("<Button-1>", self.on_click)

    def add_task(self):
        task_text = self.task_input.get().strip()
        if task_text:
            self.display_task(task_text)
            self.speak(f"Task added: {task_text}")
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")

    def display_task(self, task_text):
        task_frame = tk.Frame(self.scrollable_frame, bg="#f9fafc", bd=2, relief=tk.RAISED, padx=5, pady=5)
        task_frame.pack(fill=tk.X, pady=5)

        task_label = tk.Label(task_frame, text=task_text, bg="#f9fafc", font=self.task_font)
        task_label.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(task_frame, text="\u2714\ufe0f Complete", bg="#43b581", fg="white", 
                                     command=lambda: self.complete_task(task_frame))
        complete_button.pack(side=tk.RIGHT, padx=10)

    def complete_task(self, task_frame):
        task_frame.destroy()
        self.speak("Task completed.")

    def start_recording(self):
        threading.Thread(target=self.record_audio).start()

    def record_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.show_recording_animation("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                self.show_recording_animation("Processing...")
                task_text = recognizer.recognize_google(audio)
                self.task_input.delete(0, tk.END)
                self.task_input.insert(0, task_text)
                self.speak(f"You said: {task_text}")
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand you.")
            except sr.RequestError:
                self.speak("Could not request results, please check your connection.")
            except Exception as e:
                print(e)
                self.speak("An error occurred.")
        self.show_recording_animation("")

    def show_recording_animation(self, text):
        self.recording_animation.config(text=text)

    def speak(self, text):
        threading.Thread(target=self._speak_thread, args=(text,)).start()

    def _speak_thread(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def hide_window(self):
        self.root.attributes("-alpha", 0.1)  # Set to almost invisible
        self.root.attributes("-disabled", False)

    def on_click(self, event):
        self.root.attributes("-alpha", 1.0)  # Make fully visible again

    def reset_timer(self, event=None):
        if self.inactivity_timer:
            self.root.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.root.after(self.inactivity_timeout, self.hide_window)

# Create the main Tkinter window and initialize the Floating Task Manager
root = tk.Tk()
app = FloatingTaskManager(root)
root.mainloop()
