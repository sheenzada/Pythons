import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("☕ Coffee Shop Management System")
root.geometry("900x650")
root.configure(bg="#1e1e2f")

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 12, "bold"),
    background="#d97706",
    foreground="white",
    padding=10
)

style.configure(
    "TLabel",
    background="#1e1e2f",
    foreground="white",
    font=("Arial", 12)
)

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="☕ MODERN COFFEE SHOP",
    font=("Arial", 28, "bold"),
    bg="#1e1e2f",
    fg="#ffcc70"
)
title.pack(pady=20)

# ---------------- ANIMATION ----------------
colors = ["#ffcc70", "#ff7b54", "#ffb703", "#8ecae6"]

def animate(index=0):
    title.config(fg=colors[index])
    root.after(500, animate, (index + 1) % len(colors))

animate()

# ---------------- MENU ----------------
menu_frame = tk.Frame(root, bg="#2a2a40")
menu_frame.pack(pady=20, padx=20, fill="both")

tk.Label(
    menu_frame,
    text="Coffee Menu",
    font=("Arial", 20, "bold"),
    bg="#2a2a40",
    fg="white"
).pack(pady=10)

items = {
    "Espresso": 250,
    "Cappuccino": 350,
    "Latte": 400,
    "Mocha": 450,
    "Americano": 300,
    "Cold Coffee": 500
}

entries = {}

for item, price in items.items():
    row = tk.Frame(menu_frame, bg="#2a2a40")
    row.pack(fill="x", padx=20, pady=5)

    tk.Label(
        row,
        text=f"{item} - Rs {price}",
        bg="#2a2a40",
        fg="white",
        font=("Arial", 12)
    ).pack(side="left")

    entry = ttk.Entry(row, width=10)
    entry.pack(side="right")

    entries[item] = entry

# ---------------- BILL AREA ----------------
bill_text = tk.Text(
    root,
    height=12,
    width=70,
    bg="#111827",
    fg="white",
    font=("Consolas", 11)
)
bill_text.pack(pady=20)

# ---------------- FUNCTIONS ----------------
def calculate_bill():
    bill_text.delete(1.0, tk.END)

    total = 0

    bill_text.insert(tk.END, "======== COFFEE SHOP BILL ========\n\n")

    for item, price in items.items():
        qty = entries[item].get()

        if qty.strip():
            qty = int(qty)

            item_total = qty * price
            total += item_total

            bill_text.insert(
                tk.END,
                f"{item:15} x {qty:<3} = Rs {item_total}\n"
            )

    tax = total * 0.05
    grand_total = total + tax

    bill_text.insert(
        tk.END,
        "\n----------------------------------\n"
    )

    bill_text.insert(
        tk.END,
        f"Subtotal : Rs {total:.2f}\n"
    )

    bill_text.insert(
        tk.END,
        f"Tax (5%) : Rs {tax:.2f}\n"
    )

    bill_text.insert(
        tk.END,
        f"Total    : Rs {grand_total:.2f}\n"
    )

    bill_text.insert(
        tk.END,
        "\nThank You For Visiting ☕"
    )

def clear_all():
    for entry in entries.values():
        entry.delete(0, tk.END)

    bill_text.delete(1.0, tk.END)

# ---------------- BUTTONS ----------------
button_frame = tk.Frame(root, bg="#1e1e2f")
button_frame.pack(pady=10)

ttk.Button(
    button_frame,
    text="Generate Bill",
    command=calculate_bill
).grid(row=0, column=0, padx=10)

ttk.Button(
    button_frame,
    text="Clear",
    command=clear_all
).grid(row=0, column=1, padx=10)

ttk.Button(
    button_frame,
    text="Exit",
    command=root.destroy
).grid(row=0, column=2, padx=10)

# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Designed with Python ❤️",
    font=("Arial", 10),
    bg="#1e1e2f",
    fg="gray"
)
footer.pack(side="bottom", pady=10)

root.mainloop()