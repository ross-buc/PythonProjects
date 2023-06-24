from turtle import Turtle
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.shapesize(0.9, 0.9)
        self.penup()
        self.new_x_num = 10
        self.new_y_num = 10
        self.move_speed = 0.05
        self.start = True

    def move(self):
        if self.start:
            self.goto(0, -200)
            self.start = False
        new_x = self.xcor() + self.new_x_num
        new_y = self.ycor() + self.new_y_num
        self.goto(new_x, new_y)

    def bounce(self, top, left):
        if top:
            self.new_y_num *= -1
            self.new_x_num *= +1
        elif left:
            self.new_x_num *= -1
            self.new_y_num *= +1
        else:
            self.new_y_num *= +1
            self.new_x_num *= -1

    def paddle_bounce(self, paddle):
        self.new_y_num *= -1

        # Calculate the x-direction adjustment based on the paddle hit position
        paddle_hit_pos = self.xcor() - paddle.xcor()
        if paddle_hit_pos < -30:
            self.new_x_num = -15
        elif paddle_hit_pos < 0:
            self.new_x_num = -10
        elif paddle_hit_pos < 30:
            self.new_x_num = 10
        else:
            self.new_x_num = 15

        self.move_speed *= 0.95

    def reset(self):
        self.goto(0, -250)
        self.move_speed = 0.05
        self.new_y_num *= -1
        self.new_x_num = random.choice([-15, 15])
