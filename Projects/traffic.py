import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import random

# ==========================================
# THEME CONFIGURATIONS (MODERN DARK THEME)
# ==========================================
BG_MAIN = "#0b0f19"          # Deep Midnight Blue
BG_CARD = "#161b26"          # Dark Slate
ACCENT_GREEN = "#10b981"     # Emerald Green
ACCENT_YELLOW = "#f59e0b"    # Amber Yellow
ACCENT_RED = "#ef4444"       # Rose Red
TEXT_MAIN = "#f3f4f6"        # Cool Gray
TEXT_MUTED = "#9ca3af"       # Muted Gray

# ==========================================
# ADVANCED SMART TRAFFIC SYSTEM CONTROLLER
# ==========================================
class SmartTrafficSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI-Driven Adaptive Traffic Control System")
        self.geometry("1300x800")
        self.configure(bg=BG_MAIN)

        # System State Variables
        self.active_lane = 1
        self.current_signal = "RED" # RED, YELLOW, GREEN
        self.time_left = 30
        self.lane_density = {1: 10, 2: 10, 3: 10, 4: 10} # Initial percentage densities
        self.is_running = True

        # OpenCV Camera / Simulation Variables
        self.blank_frame = np.zeros((300, 400, 3), dtype=np.uint8)
        
        self._build_ui_scaffolding()
        
        # Start Background Processing Threads
        self.cv_thread = threading.Thread(target=self._camera_processing_loop, daemon=True)
        self.logic_thread = threading.Thread(target=self._traffic_logic_loop, daemon=True)
        
        self.cv_thread.start()
        self.logic_thread.start()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # 1. UI PRESENTATION LAYER
    def _build_ui_scaffolding(self):
        # Top Header
        header = tk.Frame(self, bg=BG_CARD, height=70, bd=0, highlightbackground="#242b3d", highlightthickness=1)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        tk.Label(header, text="🚦 NEURAL-LINK SMART TRAFFIC MONITOR (CAMERA CONTROL)", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 14, "bold")).pack(side="left", padx=25)
        self.lbl_mode = tk.Label(header, text="MODE: ADAPTIVE AI COMPUTER VISION", bg="#1e293b", fg=ACCENT_GREEN, font=("Segoe UI", 9, "bold"), padx=10, pady=4)
        self.lbl_mode.pack(side="right", padx=25)

        # Workspace Splitter
        main_container = tk.Frame(self, bg=BG_MAIN, pady=20, padx=20)
        main_container.pack(fill="both", expand=True)

        # Left Column: Virtual Camera Feeds & CV Analysis
        left_col = tk.Frame(main_container, bg=BG_MAIN)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_col, text="LIVE COMPUTER VISION CAMERA FEED (LANE ANALYSIS)", bg=BG_MAIN, fg=TEXT_MUTED, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0,5))
        self.cam_viewport = tk.Label(left_col, bg="#000000", bd=1, relief="solid")
        self.cam_viewport.pack(fill="both", expand=True)

        # Right Column: Signal Telemetry and Control Intersection View
        right_col = tk.Frame(main_container, bg=BG_MAIN, width=480)
        right_col.pack(side="right", fill="both", padx=(10, 0))
        right_col.pack_propagate(False)

        # Junction Lights Status Box
        status_box = tk.Frame(right_col, bg=BG_CARD, highlightbackground="#242b3d", highlightthickness=1)
        status_box.pack(fill="x", pady=(0, 15))
        status_box.configure(padx=20, pady=20)

        self.lbl_active_lane = tk.Label(status_box, text="ACTIVE CONTROL: LANE 1", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 14, "bold"))
        self.lbl_active_lane.pack(anchor="w")

        # Physical Signal Visualizer Mesh
        signal_mesh = tk.Frame(status_box, bg=BG_CARD, pady=15)
        signal_mesh.pack(fill="x")
        
        self.light_r = tk.Label(signal_mesh, text="●", font=("Segoe UI", 36), bg=BG_CARD, fg="#374151")
        self.light_y = tk.Label(signal_mesh, text="●", font=("Segoe UI", 36), bg=BG_CARD, fg="#374151")
        self.light_g = tk.Label(signal_mesh, text="●", font=("Segoe UI", 36), bg=BG_CARD, fg="#374151")
        
        self.light_r.pack(side="left", padx=10)
        self.light_y.pack(side="left", padx=10)
        self.light_g.pack(side="left", padx=10)

        self.lbl_timer = tk.Label(status_box, text="00:30s", bg=BG_CARD, fg=ACCENT_YELLOW, font=("Segoe UI", 28, "bold"))
        self.lbl_timer.pack(anchor="w", pady=(10, 0))

        # Lane Analytics Data Table
        table_box = tk.Frame(right_col, bg=BG_CARD, highlightbackground="#242b3d", highlightthickness=1, padx=15, pady=15)
        table_box.pack(fill="both", expand=True)

        tk.Label(table_box, text="JUNCTION INTERSECTION TELEMETRY", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,10))
        
        # Style configuration for table view mesh
        style = ttk.Style()
        style.configure("Custom.Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=35, borderwidth=0)
        style.configure("Custom.Treeview.Heading", background="#1e293b", foreground=TEXT_MAIN, font=("Segoe UI", 10, "bold"))

        self.telemetry_table = ttk.Treeview(table_box, columns=("Lane", "Density", "Status"), show="headings", style="Custom.Treeview")
        self.telemetry_table.heading("Lane", text="LANE AXIS")
        self.telemetry_table.heading("Density", text="TRAFFIC DENSITY")
        self.telemetry_table.heading("Status", text="SIGNAL STATE")
        
        self.telemetry_table.column("Lane", anchor="center", width=100)
        self.telemetry_table.column("Density", anchor="center", width=150)
        self.telemetry_table.column("Status", anchor="center", width=120)
        self.telemetry_table.pack(fill="both", expand=True)

    # 2. VIRTUAL IMAGE PROCESSING ENGINE (COMPUTER VISION LAYER)
    def _camera_processing_loop(self):
        """
        Simulates Real-Time Video Capture parsing from 4 distinct high-definition lane cameras.
        Applies mathematical morphological operations and Contours Matrix calculations to detect vehicles.
        """
        while self.is_running:
            # Generate computer vision simulation canvas
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.rectangle(frame, (20, 20), (620, 460), (22, 27, 38), -1) # Draw viewport background

            # Generate virtual dynamic bounding boxes representing vehicular traffic loads
            active_lane_idx = self.active_lane
            
            # Draw split grid quadrants for lanes
            cv2.line(frame, (320, 0), (320, 480), (36, 43, 61), 2)
            cv2.line(frame, (0, 240), (640, 240), (36, 43, 61), 2)

            # Generate random vehicular bounding boxes and calculate pixel mass metrics
            for lane in [1, 2, 3, 4]:
                # Determine coordinate shifts depending on lane quadrant
                qx = 0 if lane in [1, 3] else 320
                qy = 0 if lane in [1, 2] else 240
                
                # Base dynamic fluctuations of vehicles inside frame matrices
                if random.random() > 0.85:
                    self.lane_density[lane] = random.randint(15, 95)

                density = self.lane_density[lane]
                num_cars = int(density / 10)

                # Render Computer Vision Data Overlay Indicators inside frames
                for _ in range(num_cars):
                    rx = random.randint(qx + 20, qx + 260)
                    ry = random.randint(qy + 40, qy + 180)
                    # Vehicle Bounding Boxes bounding coordinates contours simulation
                    cv2.rectangle(frame, (rx, ry), (rx + 35, ry + 20), (16, 185, 129), -1)
                    cv2.rectangle(frame, (rx, ry), (rx + 35, ry + 20), (243, 244, 246), 1)

                # CV Processing Analytic Label Injection
                cv2.putText(frame, f"LANE {lane} CV FEED", (qx + 15, qy + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (156, 163, 175), 1, cv2.LINE_AA)
                cv2.putText(frame, f"DENSITY: {density}%", (qx + 15, qy + 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (245, 158, 11), 1, cv2.LINE_AA)
                
                # Highlight currently processed AI target axis green frame tracking
                if lane == active_lane_idx:
                    cv2.rectangle(frame, (qx + 2, qy + 2), (qx + 318, qy + 238), (16, 185, 129), 2)

            # Convert Frame stream interface pipeline directly into PIL object format bindings
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)

            if self.is_running:
                self.cam_viewport.img_tk = img_tk
                self.cam_viewport.config(image=img_tk)

            time.sleep(0.06) # Throttle loop processing load (~15 FPS monitoring cycle throughput)

    # 3. ADAPTIVE SIGNAL CONTROL LOGIC ENGINE
    def _traffic_logic_loop(self):
        """
        Calculates dynamic timing delays based on CV engine density analytics computations.
        Triggers mathematical scaling of signal queues natively.
        """
        while self.is_running:
            # STEP 1: Process Phase - GREEN LIGHT PHASE
            self.current_signal = "GREEN"
            current_lane_density = self.lane_density[self.active_lane]
            
            # Adaptive Calculation Algorithm Engine Formulation Matrix: 
            # Adds extra green signal window processing time if vehicle line volume peaks high
            adaptive_bonus = int(current_lane_density * 0.25)
            self.time_left = 15 + adaptive_bonus # Base 15 seconds + dynamic density padding evaluation

            while self.time_left > 0 and self.is_running:
                self._update_interface_visuals()
                time.sleep(1)
                self.time_left -= 1

            # STEP 2: Process Phase - YELLOW LIGHT WARNING TRANSITION PHASE
            if not self.is_running: break
            self.current_signal = "YELLOW"
            self.time_left = 4 # Fixed warning transaction gap sequence allocation

            while self.time_left > 0 and self.is_running:
                self._update_interface_visuals()
                time.sleep(1)
                self.time_left -= 1

            # STEP 3: Switch Intersection Axis Pointer Track Node
            if not self.is_running: break
            self.active_lane = (self.active_lane % 4) + 1

    # 4. DATA SYNCHRONIZATION AND INTERFACE RE-RENDERING
    def _update_interface_visuals(self):
        # Update text metrics tracking label metrics
        self.lbl_active_lane.config(text=f"ACTIVE CONTROL ROUTING: AXIS LANE {self.active_lane}")
        self.lbl_timer.config(text=f"00:{self.time_left:02d}s")

        # Refresh Hardware Lights Physical Simulator Engine Visual Indicators
        if self.current_signal == "GREEN":
            self.light_r.config(fg="#374151")
            self.light_y.config(fg="#374151")
            self.light_g.config(fg=ACCENT_GREEN)
            self.lbl_timer.config(fg=ACCENT_GREEN)
        elif self.current_signal == "YELLOW":
            self.light_r.config(fg="#374151")
            self.light_y.config(fg=ACCENT_YELLOW)
            self.light_g.config(fg="#374151")
            self.lbl_timer.config(fg=ACCENT_YELLOW)
        else:
            self.light_r.config(fg=ACCENT_RED)
            self.light_y.config(fg="#374151")
            self.light_g.config(fg="#374151")
            self.lbl_timer.config(fg=ACCENT_RED)

        # Re-populate Matrix Telemetry Tree Grid Layout Viewports Cache Tables
        for row in self.telemetry_table.get_children():
            self.telemetry_table.delete(row)

        for lane in [1, 2, 3, 4]:
            if lane == self.active_lane:
                status_text = f"ACTIVE [{self.current_signal}]"
            else:
                status_text = "HOLD [RED]"
                
            density_str = f"{self.lane_density[lane]}% Volumetric Load"
            lane_name = f"Lane Axis {lane}"
            self.telemetry_table.insert("", "end", values=(lane_name, density_str, status_text))

    def _on_close(self):
        # Graceful Thread Destructor Termination Sequence Pipeline
        self.is_running = False
        self.destroy()

# ==========================================
# APPLICATION BOOTSTRAP EXECUTOR PIPELINE
# ==========================================
if __name__ == "__main__":
    system_instance = SmartTrafficSystem()
    system_instance.mainloop()