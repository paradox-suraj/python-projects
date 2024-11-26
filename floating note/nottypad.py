"""
import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

class FloatingTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Floating Task Manager ✨")
        self.root.geometry("400x600+100+100")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#f0f0f0")  # Light background for a modern look

        # Custom Fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.task_font = Font(family="Helvetica", size=12)

        # Title Header
        title_frame = tk.Frame(self.root, bg="#7289da", relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame, text="✨ My Task Manager ✨", bg="#7289da", fg="white",
            font=self.title_font, pady=10
        )
        title_label.pack()

        # Decorative Border Frame
        border_frame = tk.Frame(self.root, bg="#99aab5", relief=tk.SUNKEN, bd=3)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Task Display Frame (Scrollable)
        self.scrollable_frame = tk.Frame(border_frame, bg="#fefbd8")
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=10)

        # Task Input Box
        self.task_input = tk.Entry(input_frame, font=self.task_font, fg="#333", width=30)
        self.task_input.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)

        # Bind the <Return> key event to the add_task method
        self.task_input.bind('<Return>', lambda event: self.add_task())

        # Add Task Button
        add_task_button = tk.Button(
            input_frame, text="➕ Add Task", bg="#43b581", fg="white",
            font=("Helvetica", 10, "bold")
        )
        add_task_button.pack(side=tk.RIGHT, padx=10, pady=10)
        add_task_button.config(command=self.add_task)  # Bind add_task function to the button

        # Close Button
        close_button = tk.Button(
            self.root, text="✖️ Close", bg="#f04747", fg="white",
            font=("Helvetica", 10, "bold"), command=self.root.destroy
        )
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Bind focus events
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)

        # Set initial transparency level
        self.root.attributes("-alpha", 1.0)

    def add_task(self):
        task_text = self.task_input.get().strip()
        if task_text:
            # Add task to the display or database
            print(f"Adding task: {task_text}")
            # Update the display with the new task
            self.display_task(task_text)
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")

    def display_task(self, task_text):
        task_frame = tk.Frame(self.scrollable_frame, bg="#f9fafc", bd=2, relief=tk.RAISED, padx=5, pady=5)
        task_frame.pack(fill=tk.X, pady=5)

        task_label = tk.Label(task_frame, text=task_text, bg="#f9fafc", font=self.task_font)
        task_label.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(task_frame, text="✔️ Complete", bg="#43b581", fg="white", command=lambda: self.complete_task(task_text))
        complete_button.pack(side=tk.RIGHT, padx=10)

    def complete_task(self, task_text):
        # Remove task from the display or database
        print(f"Completing task: {task_text}")
        # Update the display by removing the completed task
        for child in self.scrollable_frame.winfo_children():
            if child.winfo_children()[0]["text"] == task_text:
                child.destroy()

    def on_focus_in(self, event):
        self.root.attributes("-alpha", 1.0)  # Set full visibility when focused

    def on_focus_out(self, event):
        self.root.attributes("-alpha", 0.5) # Set partial visibility when not focused


# Create the main Tkinter window and initialize the Floating Task Manager
root = tk.Tk()
app = FloatingTaskManager(root)

# Run the Tkinter main loop
root.mainloop()
                             

"""

import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font

class FloatingTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Floating Task Manager ✨")
        self.root.geometry("300x500+100+100")  # Smaller window size
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#f0f0f0")  # Light background for a modern look

        # Custom Fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.task_font = Font(family="Helvetica", size=12)

        # Title Header
        title_frame = tk.Frame(self.root, bg="#7289da", relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame, text="✨ My Task Manager ✨", bg="#7289da", fg="white",
            font=self.title_font, pady=10
        )
        title_label.pack()

        # Decorative Border Frame
        border_frame = tk.Frame(self.root, bg="#99aab5", relief=tk.SUNKEN, bd=3)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Task Display Frame (Scrollable)
        self.scrollable_frame = tk.Frame(border_frame, bg="#fefbd8")
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=10)

        # Task Input Box
        self.task_input = tk.Entry(input_frame, font=self.task_font, fg="#333", width=30)
        self.task_input.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)

        # Bind the <Return> key event to the add_task method
        self.task_input.bind('<Return>', lambda event: self.add_task())

        # Add Task Button
        add_task_button = tk.Button(
            input_frame, text="➕ Add Task", bg="#43b581", fg="white",
            font=("Helvetica", 10, "bold"), command=self.add_task
        )
        add_task_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Close Button
        close_button = tk.Button(
            self.root, text="✖️ Close", bg="#f04747", fg="white",
            font=("Helvetica", 10, "bold"), command=self.root.destroy
        )
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Bind focus events
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)

        # Set initial transparency level for when the app is out of focus
        self.is_invisible = False
        self.root.attributes("-alpha", 1.0)

    def add_task(self):
        task_text = self.task_input.get().strip()
        if task_text:
            # Add task to the display
            self.display_task(task_text)
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")

    def display_task(self, task_text):
        task_frame = tk.Frame(self.scrollable_frame, bg="#f9fafc", bd=2, relief=tk.RAISED, padx=5, pady=5)
        task_frame.pack(fill=tk.X, pady=5)

        task_label = tk.Label(task_frame, text=task_text, bg="#f9fafc", font=self.task_font)
        task_label.pack(side=tk.LEFT, padx=10)

        complete_button = tk.Button(task_frame, text="✔️ Complete", bg="#43b581", fg="white", 
                                     command=lambda: self.complete_task(task_frame))
        complete_button.pack(side=tk.RIGHT, padx=10)

    def complete_task(self, task_frame):
        # Remove the task from the display
        task_frame.destroy()

    def on_focus_in(self, event):
        """Make the window fully visible when focused."""
        self.is_invisible = False
        self.root.attributes("-alpha", 1.0)  # Set full visibility

    def on_focus_out(self, event):
        """Make the window partially transparent or invisible when not focused."""
        if not self.is_invisible:
            self.root.attributes("-alpha", 0.3)  # Set low transparency


# Create the main Tkinter window and initialize the Floating Task Manager
root = tk.Tk()
app = FloatingTaskManager(root)

# Run the Tkinter main loop
root.mainloop()
