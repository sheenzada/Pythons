import tkinter as tk
import random

# Function to play the game
def play(user_choice):
    computer = random.choice([-1, 0, 1])

    youDict = {
        "snake": 1,
        "water": -1,
        "gun": 0
    }

    reverseDict = {
        1: "snake",
        -1: "water",
        0: "gun"
    }

    user_num = youDict[user_choice]
    computer_choice = reverseDict[computer]

    # Decide result
    if computer == user_num:
        result = "It's a Draw!"
    elif (computer == 1 and user_num == -1) or \
         (computer == -1 and user_num == 0) or \
         (computer == 0 and user_num == 1):
        result = "You Lose!"
    else:
        result = "You Win!"

    # Update the label
    result_label.config(
        text=f"You chose: {user_choice}\nComputer chose: {computer_choice}\nResult: {result}"
    )

# Tkinter window
root = tk.Tk()
root.title("Snake Water Gun Game")
root.geometry("350x350")
root.config(bg="#0f1c2a")

# Title label
title = tk.Label(
    root,
    text="Snake $ Water ! Gun %",
    font=("Arial", 16, "bold"),
    bg="#5f362b",
    fg="#facc15"
)
title.pack(pady=15)

# Buttons
btn_snake = tk.Button(
    root,
    text="Snake $",
    width=18,
    command=lambda: play("snake")
)
btn_snake.pack(pady=5)

btn_water = tk.Button(
    root,
    text="Water !",
    width=18,
    command=lambda: play("water")
)
btn_water.pack(pady=5)

btn_gun = tk.Button(
    root,
    text="Gun %",
    width=18,
    command=lambda: play("gun")
)
btn_gun.pack(pady=5)

# Result label
result_label = tk.Label(
    root,
    text="Make your choice!",
    font=("Arial", 12),
    bg="#0f1c2a",
    fg="white"
)
result_label.pack(pady=20)

root.mainloop()
