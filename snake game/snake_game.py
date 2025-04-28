import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import pygame
import json

pygame.mixer.init()


class HighScoreManager:
    def __init__(self):
        self.scores = {"easy": 0, "medium": 0, "hard": 0}
        self.load_scores()

    def load_scores(self):
        try:
            with open("high_scores.json", "r") as f:
                self.scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_scores()

    def save_scores(self):
        with open("high_scores.json", "w") as f:
            json.dump(self.scores, f)

    def update_score(self, difficulty, score):
        if score > self.scores[difficulty]:
            self.scores[difficulty] = score
            self.save_scores()
            return True
        return False


class StartMenu:
    def __init__(self, master, high_score_manager):
        self.master = master
        self.hsm = high_score_manager
        self.master.title("Snake Game - Difficulty Selection")
        self.master.geometry("400x300")
        self.master.configure(bg="#2E3440")

        self.title_label = tk.Label(
            master,
            text="SNAKE GAME",
            font=("Arial", 24, "bold"),
            fg="#88C0D0",
            bg="#2E3440"
        )
        self.title_label.pack(pady=20)

        self.difficulty_frame = tk.Frame(master, bg="#2E3440")
        self.difficulty_frame.pack()

        self.difficulty = tk.StringVar(value="medium")

        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard")
        ]

        for text, mode in difficulties:
            frame = tk.Frame(self.difficulty_frame, bg="#2E3440")
            frame.pack(fill="x", pady=5)

            rb = tk.Radiobutton(
                frame,
                text=text,
                variable=self.difficulty,
                value=mode,
                font=("Arial", 12),
                fg="#D8DEE9",
                bg="#2E3440",
                selectcolor="#3B4252",
                activebackground="#2E3440",
                activeforeground="#D8DEE9"
            )
            rb.pack(side="left")

            score_label = tk.Label(
                frame,
                text=f"High Score: {self.hsm.scores[mode]}",
                font=("Arial", 10),
                fg="#88C0D0",
                bg="#2E3440"
            )
            score_label.pack(side="right", padx=20)

        self.start_button = tk.Button(
            master,
            text="Start Game",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg="#A3BE8C",
            fg="#2E3440",
            activebackground="#8FBCBB",
            activeforeground="#2E3440"
        )
        self.start_button.pack(pady=20)

    def start_game(self):
        self.master.destroy()
        root = tk.Tk()
        game = SnakeGame(root, self.difficulty.get(), self.hsm)
        root.mainloop()


class Snake:
    def __init__(self, canvas, cell_size):
        self.canvas = canvas
        self.cell_size = cell_size
        self.direction = "Right"
        self.next_direction = "Right"
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.previous_body = self.body.copy()

        self.head_color = "#2D5730"
        self.body_color = "#3CB371"
        self.tail_color = "#90EE90"

    def draw(self, interpolated_positions):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(interpolated_positions):
            x0 = x * self.cell_size
            y0 = y * self.cell_size
            x1 = x0 + self.cell_size
            y1 = y0 + self.cell_size

            if i == 0:
                color = self.head_color
            elif i == len(interpolated_positions) - 1:
                color = self.tail_color
            else:
                color = self.body_color

            self.canvas.create_oval(
                x0 + 3, y0 + 3, x1 - 3, y1 - 3,
                fill=color, outline="#1E3520", width=2,
                tag="snake"
            )

    def move(self):
        self.previous_body = self.body.copy()
        head_x, head_y = self.body[0]
        self.direction = self.next_direction

        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, width, height):
        head_x, head_y = self.body[0]
        if (head_x < 0 or head_x >= width or
                head_y < 0 or head_y >= height):
            return True
        for segment in self.body[1:]:
            if segment == self.body[0]:
                return True
        return False


class Food:
    def __init__(self, canvas, cell_size, width, height):
        self.canvas = canvas
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.generate()

    def generate(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.position = (x, y)
        self.canvas.delete("food")

        x0 = x * self.cell_size + self.cell_size // 4
        y0 = y * self.cell_size + self.cell_size // 4
        x1 = x0 + self.cell_size // 2
        y1 = y0 + self.cell_size // 2

        self.canvas.create_oval(
            x0, y0, x1, y1,
            fill="#FF0000", outline="#8B0000", width=2,
            tag="food"
        )
        self.canvas.create_polygon(
            x1 - 2, y0 - 2,
            x1 + self.cell_size // 4, y0 - self.cell_size // 4,
            x1 - 2, y0 - self.cell_size // 8,
            fill="#00FF00", outline="#006400", width=1,
            tag="food"
        )


class GameOverDialog(tk.Toplevel):
    def __init__(self, parent, score, difficulty, hsm):
        super().__init__(parent)
        self.title("Game Over")
        self.hsm = hsm
        self.difficulty = difficulty
        self.score = score

        self.configure(bg="#2E3440")
        self.geometry("300x200")

        new_high = self.hsm.update_score(difficulty, score)

        tk.Label(self, text="Game Over!", font=("Arial", 16),
                 bg="#2E3440", fg="#88C0D0").pack(pady=10)

        score_text = f"Score: {score}\nHigh Score: {self.hsm.scores[difficulty]}"
        if new_high:
            score_text += "\nNew High Score!"

        tk.Label(self, text=score_text, font=("Arial", 12),
                 bg="#2E3440", fg="#D8DEE9").pack(pady=5)

        btn_frame = tk.Frame(self, bg="#2E3440")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Retry", command=lambda: self.close("retry")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Change Difficulty", command=lambda: self.close("menu")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Quit", command=lambda: self.close("quit")).pack(side="left", padx=5)

        self.result = None

    def close(self, result):
        self.result = result
        self.destroy()


class SnakeGame:
    def __init__(self, master, difficulty, hsm):
        self.master = master
        self.difficulty = difficulty
        self.hsm = hsm

        self.cell_size = 30
        self.width = 20
        self.height = 15
        self.speed = self.set_difficulty()
        self.last_update = time.time()
        self.progress = 0.0

        self.load_sounds()

        self.canvas = tk.Canvas(
            master,
            width=self.width * self.cell_size,
            height=self.height * self.cell_size,
            bg="#3B4252",
            highlightthickness=0
        )
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(
            master,
            text=f"Score: {self.score} | High Score: {self.hsm.scores[self.difficulty]}",
            font=("Arial", 14, "bold"),
            fg="#D8DEE9",
            bg="#2E3440",
            padx=20,
            pady=10
        )
        self.score_label.pack(fill="x")

        self.snake = Snake(self.canvas, self.cell_size)
        self.food = Food(self.canvas, self.cell_size, self.width, self.height)

        self.master.bind("<Key>", self.handle_keypress)
        self.canvas.focus_set()
        self.game_loop()
        self.animation_loop()

    def set_difficulty(self):
        return {
            "easy": 300,
            "medium": 200,
            "hard": 150
        }[self.difficulty]

    def load_sounds(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.eat_sound = pygame.mixer.Sound("sounds/eat.wav")
            self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
        except Exception as e:
            print(f"Sound error: {e}. Continuing without sounds.")
            self.eat_sound = None
            self.game_over_sound = None

    def handle_keypress(self, event):
        key = event.keysym
        current_dir = self.snake.direction
        if (key == "Up" and current_dir != "Down" or
                key == "Down" and current_dir != "Up" or
                key == "Left" and current_dir != "Right" or
                key == "Right" and current_dir != "Left"):
            self.snake.next_direction = key

    def interpolate_positions(self):
        current_time = time.time()
        dt = current_time - self.last_update
        self.progress = min(dt / (self.speed / 1000), 1.0)

        interpolated = []
        for i in range(len(self.snake.body)):
            if i < len(self.snake.previous_body):
                px, py = self.snake.previous_body[i]
            else:
                px, py = self.snake.body[i]

            cx, cy = self.snake.body[i]
            ix = px + (cx - px) * self.progress
            iy = py + (cy - py) * self.progress
            interpolated.append((ix, iy))

        return interpolated

    def animation_loop(self):
        interpolated = self.interpolate_positions()
        self.snake.draw(interpolated)
        self.master.after(16, self.animation_loop)

    def game_loop(self):
        if time.time() - self.last_update >= self.speed / 1000:
            self.last_update = time.time()

            self.snake.move()

            if self.snake.check_collision(self.width, self.height):
                self.game_over()
                return

            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.score += 10
                self.score_label.config(
                    text=f"Score: {self.score} | High Score: {self.hsm.scores[self.difficulty]}"
                )
                self.food.generate()
                if self.eat_sound:
                    self.eat_sound.play()

        self.master.after(16, self.game_loop)

    def game_over(self):
        if self.game_over_sound:
            self.game_over_sound.play()

        dialog = GameOverDialog(self.master, self.score, self.difficulty, self.hsm)
        self.master.wait_window(dialog)

        if dialog.result == "retry":
            self.master.destroy()
            root = tk.Tk()
            SnakeGame(root, self.difficulty, self.hsm)
            root.mainloop()
        elif dialog.result == "menu":
            self.master.destroy()
            root = tk.Tk()
            StartMenu(root, self.hsm)
            root.mainloop()
        elif dialog.result == "quit":
            self.master.destroy()


if __name__ == "__main__":
    hsm = HighScoreManager()
    root = tk.Tk()
    menu = StartMenu(root, hsm)
    root.mainloop()