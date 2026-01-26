import ipywidgets as widgets
from IPython.display import display, clear_output
import random

# --- Designer UI Components ---
title = widgets.HTML("<h1>🚛 Truck Delivery Pro</h1><p>Navigate to the 🏁. Watch your ⛽!</p>")
grid_size = 7
truck_pos = [0, 0]
goal_pos = [6, 6]
fuel = 20
obstacles = [[2, 1], [2, 2], [4, 4], [4, 5], [1, 4], [5, 1]]

def create_grid():
    grid_rows = []
    for r in range(grid_size):
        row_widgets = []
        for c in range(grid_size):
            # Styling logic
            color = "#f0f0f0"
            label = "⬜"
            
            if [r, c] == truck_pos:
                color = "#4CAF50" # Green for truck
                label = "🚛"
            elif [r, c] == goal_pos:
                color = "#FFD700" # Gold for warehouse
                label = "🏁"
            elif [r, c] in obstacles:
                color = "#555" # Dark for obstacles
                label = "🚧"
                
            btn = widgets.Button(
                description=label,
                disabled=True,
                layout=widgets.Layout(width='45px', height='45px', margin='2px'),
                style={'button_color': color}
            )
            row_widgets.append(btn)
        grid_rows.append(widgets.HBox(row_widgets))
    return widgets.VBox(grid_rows)

# --- Game Logic ---
output = widgets.Output()
status_label = widgets.HTML(f"<b>Fuel: {fuel} | Status: Driving...</b>")

def move_truck(change):
    global truck_pos, fuel
    if fuel <= 0: return

    direction = change.description
    new_pos = list(truck_pos)

    if direction == "UP" and truck_pos[0] > 0: new_pos[0] -= 1
    elif direction == "DOWN" and truck_pos[0] < grid_size - 1: new_pos[0] += 1
    elif direction == "LEFT" and truck_pos[1] > 0: new_pos[1] -= 1
    elif direction == "RIGHT" and truck_pos[1] < grid_size - 1: new_pos[1] += 1

    if new_pos in obstacles:
        with output:
            print("💥 Crashed into a barrier! -2 Fuel")
        fuel -= 2
    else:
        truck_pos = new_pos
        fuel -= 1

    update_display()
    check_win_loss()

def check_win_loss():
    if truck_pos == goal_pos:
        status_label.value = "<b style='color:green;'>🏆 MISSION COMPLETE! Delivery successful.</b>"
        disable_buttons()
    elif fuel <= 0:
        status_label.value = "<b style='color:red;'>💀 OUT OF FUEL! Game Over.</b>"
        disable_buttons()
    else:
        status_label.value = f"<b>Fuel: {fuel} | Status: Moving...</b>"

def disable_buttons():
    for b in [btn_up, btn_down, btn_left, btn_right]:
        b.disabled = True

# --- Controller Layout ---
btn_up = widgets.Button(description="UP", layout=widgets.Layout(width='60px'))
btn_down = widgets.Button(description="DOWN", layout=widgets.Layout(width='60px'))
btn_left = widgets.Button(description="LEFT", layout=widgets.Layout(width='60px'))
btn_right = widgets.Button(description="RIGHT", layout=widgets.Layout(width='60px'))

for b in [btn_up, btn_down, btn_left, btn_right]:
    b.on_click(move_truck)

controls = widgets.VBox([
    widgets.HBox([widgets.Label(width='60px'), btn_up]),
    widgets.HBox([btn_left, btn_down, btn_right])
], layout=widgets.Layout(align_items='center', margin='20px 0'))

game_container = widgets.VBox()

def update_display():
    game_container.children = [title, status_label, create_grid(), controls, output]

update_display()
display(game_container)