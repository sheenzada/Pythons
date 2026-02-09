def play (user_choice):
    computer = random.choice([-1, 0 , 1])

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

    if computer == user_num:
        result = "It's a Draw ="
    elif (computer == 1 and user_num == -1) or \
         (computer == -1 and user_num == 0) or \
         (computer == 0 and user_num == 1):
        result = "You Lose X"
    else:
        result = "You Win *"
    result_label.config(
        text=f"You choice :  {user_choice}\nComputer choice"
    )


    root = tk.Tk()
    root.title("Snake Water Gun Game")
    root.geometry("350x330")
    root.config(bg="#0f1c2a")


    title = tk.Label(
        root,
        text="Snake $ Water ! Gun %",
        font=("Arial" , 16 , "bold"),
        bg="#5f362b",
        fg="#facc15"
    )
    title.pack(pady=15)


    btn_snake = tk.Button(
        root,
        text="Snake $",
        width = 18
    )