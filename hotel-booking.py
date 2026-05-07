# Simple Hotel Booking Form using Tkinter (Python GUI)

import tkinter as tk
from tkinter import messagebox

def book_hotel():
    name = entry_name.get()
    checkin = entry_checkin.get()
    checkout = entry_checkout.get()
    guests = entry_guests.get()
    room = room_type.get()

    if name == "" or checkin == "" or checkout == "" or guests == "":
        messagebox.showerror("Error", "Please fill all fields")
    else:
        summary = f"""
Booking Confirmed!

Name: {name}
Check-in: {checkin}
Check-out: {checkout}
Guests: {guests}
Room Type: {room}
"""
        messagebox.showinfo("Booking Success", summary)

# Main Window
root = tk.Tk()
root.title("Hotel Booking Form")
root.geometry("400x400")

# Title
title = tk.Label(root, text="Hotel Booking Form", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Name
tk.Label(root, text="Full Name").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

# Check-in
tk.Label(root, text="Check-in Date").pack()
entry_checkin = tk.Entry(root, width=30)
entry_checkin.pack(pady=5)

# Check-out
tk.Label(root, text="Check-out Date").pack()
entry_checkout = tk.Entry(root, width=30)
entry_checkout.pack(pady=5)

# Guests
tk.Label(root, text="Number of Guests").pack()
entry_guests = tk.Entry(root, width=30)
entry_guests.pack(pady=5)

# Room Type
tk.Label(root, text="Room Type").pack()

room_type = tk.StringVar(value="Standard")

tk.Radiobutton(root, text="Standard", variable=room_type, value="Standard").pack()
tk.Radiobutton(root, text="Deluxe", variable=room_type, value="Deluxe").pack()
tk.Radiobutton(root, text="Suite", variable=room_type, value="Suite").pack()

# Submit Button
book_btn = tk.Button(root, text="Book Now", command=book_hotel,
                     bg="blue", fg="white", width=20)
book_btn.pack(pady=20)

# Run App
root.mainloop()