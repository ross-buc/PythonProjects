from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.clear()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.lives = 3
        self.update_scoreboard(block=False)

    def update_scoreboard(self, block):
        if self.lives == 0:
            self.clear()
            self.goto(0, 0)
            self.write("Game Over", align="center", font=("Courier", 80, "bold"))
        elif block:
            self.clear()
            self.goto(0, 0)
            self.write("You Won!!!", align="center", font=("Courier", 80, "bold"))
        else:
            self.clear()
            self.goto(0, 265)
            self.write(
                f"Lives left: {self.lives}",
                align="center",
                font=("Courier", 24, "bold"),
            )
