import customtkinter as ctk
from tkinter import messagebox
from coffee_ai import CoffeeAI
from orders import Order

API_KEY = "YOUR_OPENAI_API_KEY"

class CoffeeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("☕ AI Coffee Shop")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.ai = CoffeeAI(API_KEY)

        self.orders = []

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="AI Coffee Assistant",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Customer Name",
            width=300
        )
        self.name_entry.pack(pady=10)

        self.mood_entry = ctk.CTkEntry(
            self,
            placeholder_text="Mood (happy, tired, stressed...)",
            width=300
        )
        self.mood_entry.pack(pady=10)

        self.weather_entry = ctk.CTkEntry(
            self,
            placeholder_text="Weather",
            width=300
        )
        self.weather_entry.pack(pady=10)

        recommend_btn = ctk.CTkButton(
            self,
            text="Get AI Recommendation",
            command=self.get_recommendation,
            height=40
        )
        recommend_btn.pack(pady=20)

        self.output = ctk.CTkTextbox(
            self,
            width=700,
            height=250
        )
        self.output.pack(pady=20)

        order_btn = ctk.CTkButton(
            self,
            text="Place Order",
            command=self.place_order,
            fg_color="green"
        )
        order_btn.pack(pady=10)

    def get_recommendation(self):

        mood = self.mood_entry.get()
        weather = self.weather_entry.get()

        if not mood or not weather:
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            result = self.ai.recommend_coffee(mood, weather)

            self.output.delete("1.0", "end")
            self.output.insert("end", result)

        except Exception as e:
            messagebox.showerror("AI Error", str(e))

    def place_order(self):

        customer = self.name_entry.get()

        if not customer:
            messagebox.showerror("Error", "Enter customer name")
            return

        text = self.output.get("1.0", "end").strip()

        if not text:
            messagebox.showerror("Error", "Get recommendation first")
            return

        order = Order(
            customer_name=customer,
            drink="AI Special Coffee",
            price=9.99
        )

        self.orders.append(order)

        messagebox.showinfo(
            "Order Placed",
            order.summary()
        )