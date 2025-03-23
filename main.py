from tkinter import *
from tkinter import messagebox
import math

# ---------------------------- Constants ------------------------------- #

FONT_NAME = "Courier"
FRST_CLR = "#BCB8B1"
SCND_CLR = "#463F3A"
THRD_CLR = "#8A817C"
FRTH_CLR = "#F4F3EE"
FFTH_CLR = "#E0AFA0"
timer = None
glass_img = None
water_counter = 0
img_list = []

def reset_glass_counter():
    global img_list
    global water_counter
    img_list = []
    water_counter = 0
    glass_canvas.delete('all')

def add_glass():
    global img_list
    global glass_img
    global water_counter
    water_counter += 1
    img_list = []
    glass_img = PhotoImage(file="waterglass-32.png")
    if water_counter < 9:
        for _ in range(water_counter):
            img_list.append(glass_img)
        x = 32
        offset_x = 0
        for item in img_list:
            glass_canvas.create_image(x + offset_x, 32, image=item)
            offset_x += 30
    else:
        for _ in range(8):
            img_list.append(glass_img)
        x = 32
        offset_x = 0
        for item in img_list:
            glass_canvas.create_image(x + offset_x, 32, image=item)
            offset_x += 30
        messagebox.showinfo(title="Hey!", message="That's probably enough of water! "
                                                           "You should check with your doctor "
                                                           "about the right amount for you!")

# ---------------------------- Timer ------------------------------- #
def reset_timer():
    global timer
    if timer is not None:
        window.after_cancel(timer)
        timer_canvas.itemconfig(timer_text, text="00:00")
        start_button["state"] = "active"
        minutes_input["state"] = "normal"
        minutes_input.bind('<Return>', start_timer_on_enter)

def start_timer_on_enter(_event):
    if len(minutes_input.get()) != 0:
         start_timer()
    else:
        messagebox.showinfo(title="Warning", message="Please, enter amount of minutes for timer.")

def start_timer():
    interval_min = 60
    if len(minutes_input.get()) != 0:
        try:
            interval_min = int(minutes_input.get())
        except ValueError:
            messagebox.showinfo(title="Warning", message="Please, enter a whole number.")
            minutes_input.delete(0, END)
        else:
            interval_min = abs(interval_min)
            if interval_min == 0:
                messagebox.showinfo(title="Warning", message="Amount of minutes can't be 0.")
                minutes_input.delete(0, END)
            elif interval_min > 999:
                messagebox.showinfo(title="Warning", message="Exceeds the limit.")
                minutes_input.delete(0, END)
            else:
                minutes_input.delete(0, END)
                interval_sec = interval_min * 60
                count_down(interval_sec)
                start_button["state"] = "disabled"
                minutes_input["state"] = "disabled"

    else:
        interval_sec = interval_min * 60
        count_down(interval_sec)
        start_button["state"] = "disabled"
        minutes_input["state"] = "disabled"

def count_down(count):
    minutes_input.unbind('<Return>')
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    timer_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        window.attributes('-topmost', 1)
        messagebox.showinfo(title="Water Reminder", message="Probably should have a glass of water!")
        start_button["state"] = "active"
        minutes_input["state"] = "normal"
        minutes_input.bind('<Return>', start_timer_on_enter)
        timer_canvas.itemconfig(timer_text, text="00:00")

# ---------------------------- UI ------------------------------- #

window = Tk()
window.title("Water Int")
window.config(padx=100, pady=50, bg=FRST_CLR)
window.minsize(width=700, height=500)
window.maxsize(width=720, height=600)

glass_canvas = Canvas(width=270, height=60, bg=FRST_CLR)
glass_canvas.grid(row=1, column=1, columnspan=2, sticky="W", pady=(30, 30))

title_label = Label(text="Track your water intake",bg=FRST_CLR,fg=SCND_CLR,font=(FONT_NAME, 25, 'bold'))
title_label.grid(row=0, column=0,pady=(0, 30), columnspan=3,  sticky="WE")

count_label = Label(text="Amount of glasses",bg=FRST_CLR,fg=SCND_CLR,font=(FONT_NAME, 14, 'bold'))
count_label.grid(column=0, row=1, sticky="W")

add_glass_button = Button(text="Add a glass", font=(FONT_NAME, 12, "bold"), command=add_glass,
                          bg=FRTH_CLR, fg=SCND_CLR, highlightthickness=0,
                          relief="flat", activebackground=FRTH_CLR)
add_glass_button.grid(column=0, row=2, sticky="W")

reset_glass_button = Button(text="Reset glass counter", font=(FONT_NAME, 12, "bold"),
                            command=reset_glass_counter, bg=FRTH_CLR, fg=SCND_CLR,
                            highlightthickness=0, relief="flat", activebackground=FRTH_CLR)
reset_glass_button.grid(column=1, row=2, sticky="E")

remind_me_label = Label(text="Remind me in (min): ",
                        bg=FRST_CLR,fg=SCND_CLR,font=(FONT_NAME, 14, 'bold'))
remind_me_label.grid(column=0, row=4, pady=30, sticky="W")

minutes_input = Entry(width=10)
minutes_input.grid(column=1, row=4, sticky="W")
minutes_input.bind('<Return>', start_timer_on_enter)

start_button = Button(text="Start timer", font=(FONT_NAME, 12, "bold"), command=start_timer,
                      bg=FRTH_CLR, fg=SCND_CLR, highlightthickness=0,
                      relief="flat", activebackground=FRTH_CLR)
start_button.grid(column=0, row=5, sticky="W")

reset_button = Button(text="Reset timer", font=(FONT_NAME, 12, "bold"), command=reset_timer,
                      bg=FRTH_CLR, fg=SCND_CLR, highlightthickness=0,
                      relief="flat", activebackground=FRTH_CLR)
reset_button.grid(column=2, row=5, sticky="W")

timer_canvas = Canvas(width=120, height=120, bg=FRST_CLR )
timer_text = timer_canvas.create_text(60, 60, text="00:00", fill=SCND_CLR, font=(FONT_NAME, 20, "bold"))
timer_canvas.grid(column=1, row=5, sticky="W")

window.mainloop()