from tkinter import *
from pandas import *
import random

BACKGROUND_COLOR = "#B1DDC6"
new_word = {}
data_dict = {}

# Get new word from to-learn list, catching exceptions
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    og_data = pandas.read_csv("es_en_1000.csv")
    data_dict = og_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


# Flip the card and show English translation
def flip_card():
    global flip_timer, new_word
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    english = new_word["English"]
    canvas.itemconfig(card_word, text=english, fill="white")


# Generate new word from csv
def new_card():
    global new_word
    new_word = random.choice(data_dict)
    spanish = new_word["Espanol"]
    canvas.itemconfig(card_word, text=spanish, fill="black")
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_img, image=card_front_img)
    window.after(3000, flip_card)


# Remove the current card from word list
def is_known():
    data_dict.remove(new_word)
    data = pandas.DataFrame(data_dict)
    data.to_csv("words_to_learn.csv", index=False)
    new_card()


# UI building
window = Tk()
window.title("Spanish flash card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_img = canvas.create_image(400, 236, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=1, row=1, columnspan=2)

unknown_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=new_card)
unknown_button.grid(column=1, row=2)

known_img = PhotoImage(file="images/right.png")
known_button = Button(image=known_img, highlightthickness=0, command=is_known)
known_button.grid(column=2, row=2)

new_card()

window.mainloop()
