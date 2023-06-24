from turtle import Turtle


class Blocks(Turtle):
    def __init__(self):
        super().__init__()
        self.start_positions = [
            (240, "red"),
            (215, "orange"),
            (190, "yellow"),
            (165, "green"),
            (140, "blue"),
        ]
        self.blocks = []

        for y, color in self.start_positions:
            start_x = -382
            for _ in range(19):
                new_block = Turtle()
                new_block.speed("fastest")
                new_block.shape("square")
                new_block.shapesize(stretch_wid=0.7, stretch_len=1.5)
                new_block.color(color)
                new_block.penup()
                new_block.setx(start_x)
                new_block.sety(y)
                self.blocks.append(new_block)
                start_x += 42
