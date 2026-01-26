import ipywidgets as widgets
from IPython.display import display, clear_output
import json
import os

# ---------- DATA FOLDER ----------
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({}, f)

# ---------- LOGIN SCREEN ----------
def login_screen():
    clear_output()
    print("=== LOGIN ===")
    
    username_input = widgets.Text(description="Username:")
    password_input = widgets.Password(description="Password:")
    login_button = widgets.Button(description="Login", button_style='success')
    register_button = widgets.Button(description="Register", button_style='info')
    output = widgets.Output()
    
    def try_login(b):
        with output:
            output.clear_output()
            username = username_input.value.strip()
            password = password_input.value.strip()
            if not username or not password:
                print("Enter both username and password!")
                return
            with open("data/users.json", "r") as f:
                users = json.load(f)
            if username in users and users[username] == password:
                print(f"Welcome back, {username}!")
                main_menu(username)
            else:
                print("Invalid username or password!")

    def go_register(b):
        registration_screen()
    
    login_button.on_click(try_login)
    register_button.on_click(go_register)
    
    display(username_input, password_input, login_button, register_button, output)

# ---------- REGISTRATION SCREEN ----------
def registration_screen():
    clear_output()
    print("=== REGISTER ===")
    
    username_input = widgets.Text(description="Username:")
    password_input = widgets.Password(description="Password:")
    register_button = widgets.Button(description="Register", button_style='success')
    back_button = widgets.Button(description="Back", button_style='warning')
    output = widgets.Output()
    
    def try_register(b):
        with output:
            output.clear_output()
            username = username_input.value.strip()
            password = password_input.value.strip()
            if not username or not password:
                print("Enter both username and password!")
                return
            with open("data/users.json", "r") as f:
                users = json.load(f)
            if username in users:
                print("Username already exists!")
            else:
                users[username] = password
                with open("data/users.json", "w") as f:
                    json.dump(users, f)
                print("Registration successful! Go to login.")
    
    def back(b):
        login_screen()
    
    register_button.on_click(try_register)
    back_button.on_click(back)
    
    display(username_input, password_input, register_button, back_button, output)

# ---------- MAIN MENU ----------
def main_menu(username):
    clear_output()
    print(f"=== Welcome {username}! ===")
    
    start_button = widgets.Button(description="Start Game", button_style='success')
    exit_button = widgets.Button(description="Exit", button_style='danger')
    output = widgets.Output()
    
    def start_game(b):
        with output:
            output.clear_output()
            print("Game would start here!")
            # Here you can call the TruckSimulation game

    def exit_game(b):
        clear_output()
        print("Thank you for playing!")
    
    start_button.on_click(start_game)
    exit_button.on_click(exit_game)
    
    display(start_button, exit_button, output)

# ---------- START PROJECT ----------
login_screen()
