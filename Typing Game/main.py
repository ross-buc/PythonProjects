"""
A Python project using Tkinter to test how many words per minute a person can type
"""
import tkinter as tk
import random
import math


class TypingGame:
    """
    A class to handle the Typing game
    """

    def __init__(self):
        """
        Initialize the TypingGame class.

        This sets up the initial attributes, such as the word list, random word, and Tkinter components.
        """
        self.timer = None
        self.score = 0
        self.word_list = [
            "lion",
            "tree",
            "fire",
            "bird",
            "lake",
            "book",
            "door",
            "desk",
            "lamp",
            "baby",
            "star",
            "ship",
            "moon",
            "fish",
            "hand",
            "frog",
            "park",
            "rain",
            "snow",
            "song",
            "bell",
            "toad",
            "love",
            "idea",
            "game",
            "apple",
            "chair",
            "cloud",
            "dance",
            "plate",
            "brush",
            "drift",
            "frame",
            "glass",
            "juice",
            "knife",
            "mouse",
            "paper",
            "shirt",
            "spoon",
            "train",
            "watch",
            "bagel",
            "boxer",
            "brick",
            "candy",
            "daisy",
            "dream",
            "fence",
            "grape",
            "banana",
            "purple",
            "guitar",
            "monkey",
            "rocket",
            "planet",
            "rabbit",
            "dragon",
            "summer",
            "sunset",
            "basket",
            "flower",
            "island",
            "castle",
            "bridge",
            "sponge",
            "cookie",
            "pencil",
            "turtle",
            "forest",
            "chicken",
            "elephant",
            "holiday",
            "journey",
            "musical",
            "monster",
            "morning",
            "octopus",
            "penguin",
            "princess",
            "rainbow",
            "sandbox",
            "shampoo",
            "squirrel",
            "teacher",
            "toucan",
            "vampire",
            "whisper",
            "wonder",
            "zeppelin",
        ]

        self.random_word = random.choice(self.word_list)

        self.root = tk.Tk()

        self.window = tk.Canvas(self.root, width=400, height=300)
        self.window.pack()

        self.current_score = tk.StringVar()
        self.current_score.set(f"Your current score is {self.score} ")
        self.label0 = tk.Label(self.root, textvariable=self.current_score)
        self.label0.config(font=("helvetica", 14))
        self.window.create_window(200, 180, window=self.label0)

        self.label1 = tk.Label(self.root, text="Type the word below")
        self.label1.config(font=("helvetica", 18))
        self.window.create_window(200, 25, window=self.label1)

        self.label2 = tk.Label(self.root, text=self.random_word)
        self.label2.config(font=("helvetica", 14))
        self.window.create_window(200, 100, window=self.label2)

        self.entry1 = tk.Entry(self.root, state=tk.DISABLED)
        self.window.create_window(200, 140, window=self.entry1)

        self.timer_text = self.window.create_text(
            200, 225, text="00:00", fill="black", font=("helvetica", 14, "bold")
        )

        self.button_start = tk.Button(self.root, text="Start", command=self.start_timer)
        self.button_start.pack()

        self.button_reset = tk.Button(self.root, text="Reset", command=self.reset)
        self.button_reset.pack()

        self.entry1.after(100, self.check_input)

    def check_input(self):
        """Check the user's input and updates the score if correct"""
        typed_word = self.entry1.get()
        if typed_word == self.random_word:
            print("Correct!")
            self.generate_random_word()
            self.entry1.delete(0, "end")
            self.score += 1
            self.current_score.set(f"Your current score is {self.score} ")
        self.entry1.after(100, self.check_input)

    def generate_random_word(self):
        """Generate a new random word for the game."""
        previous_choice = self.random_word
        while self.random_word == previous_choice:
            self.random_word = random.choice(self.word_list)
        self.label2.config(text=self.random_word)

    def start_timer(self):
        """Starts the countdown from 60 seconds and enables typing in the entry field"""
        self.count_down(60)
        self.button_start.config(state=tk.DISABLED)
        self.entry1.config(state=tk.NORMAL)
        self.entry1.focus_set()

    def count_down(self, count):
        """
        Perform the countdown for the timer.
        Args:
            count (int): The initial count value in seconds.
        """
        count_min = math.floor(count / 60)
        count_sec = count % 60
        self.window.itemconfigure(
            self.timer_text,
            text=f"{'{:02d}'.format(count_min)}:{'{:02d}'.format(count_sec)}",
        )
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
        else:
            self.window.itemconfigure(self.timer_text, text="00:00")
            self.entry1.config(state=tk.DISABLED)
            final_score = f"Your final score was {self.score} "
            self.current_score.set(final_score)

    def reset(self):
        """Reset the game to its initial state."""
        self.score = 0
        self.current_score.set(f"Your current score is {self.score} ")
        self.generate_random_word()
        self.entry1.delete(0, "end")
        self.button_start.config(state=tk.NORMAL)
        self.entry1.config(state=tk.DISABLED)
        self.window.after_cancel(self.timer)
        self.window.itemconfigure(self.timer_text, text="00:00")

    def run(self):
        """Run the Tkinter event loop to start the game."""
        self.root.mainloop()


game = TypingGame()
game.run()
