import uuid
from datetime import datetime

class Order:
    def __init__(self, customer_name, drink, price):
        self.order_id = str(uuid.uuid4())[:8]
        self.customer_name = customer_name
        self.drink = drink
        self.price = price
        self.time = datetime.now()

    def summary(self):
        return f"""
Order ID: {self.order_id}
Customer: {self.customer_name}
Drink: {self.drink}
Price: ${self.price}
Time: {self.time.strftime('%H:%M:%S')}
"""