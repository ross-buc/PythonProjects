"""
A python game based on the Atari game Breakout
"""
from turtle import *
import time
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from blocks import Blocks

blocks = Blocks()
screen = Screen()
paddle = Paddle((0, -250))
scoreboard = Scoreboard()
ball = Ball()


screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Breakout")
screen.tracer(0)


screen.onkey(paddle.left, "Left")
screen.onkey(paddle.right, "Right")
screen.listen()


def main():
    game_is_on = True
    last_bounce = 0
    while game_is_on:
        if not scoreboard.lives:
            game_is_on = False
            scoreboard.update_scoreboard(block=False)
            break
        if blocks.blocks:
            time.sleep(ball.move_speed)
            screen.update()
            ball.move()
            # Detects collision with left or right wall of the screen
            if ball.ycor() > 280:
                ball.bounce(top=True, left=False)
            elif ball.xcor() < -370:
                ball.bounce(top=False, left=True)
            elif ball.xcor() > 370:
                ball.bounce(top=False, left=False)
            else:
                pass

            # Detects collision with brick
            for block in blocks.blocks:
                if ball.distance(block) < 20:
                    ball.bounce(top=True, left=False)
                    blocks.blocks.remove(block)
                    block.hideturtle()

            # Detects collision with paddle
            if time.time() - last_bounce > 1:
                if (
                    abs(ball.ycor() - paddle.ycor()) < 28
                    and abs(ball.xcor() - paddle.xcor()) < 35
                ):
                    ball.paddle_bounce(paddle=paddle)
                    last_bounce = time.time()

            # Detects if the ball goes past the paddle
            if ball.ycor() < -310:
                scoreboard.lives -= 1
                scoreboard.update_scoreboard(block=False)
                ball.reset()
        else:
            game_is_on = False
            scoreboard.update_scoreboard(block=True)
            break

    screen.exitonclick()


if __name__ == "__main__":
    main()
