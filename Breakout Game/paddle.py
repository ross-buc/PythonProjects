from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.6, stretch_len=4.5)
        self.color("white")
        self.penup()
        self.goto(position)

    def left(self):
        x_cor = self.xcor()
        y_cor = self.ycor()
        self.goto((x_cor - 50), y_cor)

    def right(self):
        x_cor = self.xcor()
        y_cor = self.ycor()
        self.goto((x_cor + 50), y_cor)
