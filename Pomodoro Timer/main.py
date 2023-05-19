from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
stop = False
reps = 0
timer = None


def main():
    # ---------------------------- TIMER RESET ------------------------------- #

    def reset():
        global reps

        window.after_cancel(timer)
        label_checkmark.config(text="")
        canvas.itemconfigure(timer_text, text="00:00")
        label_title.config(
            text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 32, "normal")
        )
        reps = 0

    # ---------------------------- TIMER MECHANISM ------------------------------- #

    def start_timer():
        global reps
        reps += 1

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            label_title.config(
                text="Break", fg=RED, bg=YELLOW, font=(FONT_NAME, 32, "normal")
            )
            count_down(long_break_sec)
        elif reps % 2 == 0:
            label_title.config(
                text="Break", fg=PINK, bg=YELLOW, font=(FONT_NAME, 32, "normal")
            )
            count_down(short_break_sec)
        else:
            label_title.config(
                text="Work", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 32, "normal")
            )
            count_down(work_sec)

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

    def count_down(count):
        global reps
        global timer

        count_min = math.floor(count / 60)
        count_sec = count % 60
        canvas.itemconfigure(
            timer_text,
            text=f"{'{:02d}'.format(count_min)}:{'{:02d}'.format(count_sec)}",
        )
        if count > 0:
            timer = window.after(1000, count_down, count - 1)
        else:
            start_timer()
            marks = ""
            work_sessions = math.floor(reps / 2)
            for _ in range(work_sessions):
                marks += "✔"
            label_checkmark.config(text=marks)

    # ---------------------------- UI SETUP ------------------------------- #

    window = Tk()
    window.title("Pomodoro")
    window.config(padx=100, pady=50, bg=YELLOW)

    canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
    image = PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=image)
    timer_text = canvas.create_text(
        100, 130, text="00:00", fill="white", font=(FONT_NAME, 26, "bold")
    )
    canvas.grid(column=1, row=1)

    label_title = Label(
        text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 32, "normal")
    )
    label_title.grid(column=1, row=0)

    label_checkmark = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14, "normal"))
    label_checkmark.grid(column=1, row=3)

    button_start = Button(text="Start", command=start_timer)
    button_start.grid(column=0, row=2)

    button_reset = Button(text="Reset", command=reset)
    button_reset.grid(column=2, row=2)

    window.mainloop()


if __name__ == "__main__":
    main()
