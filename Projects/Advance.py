import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# CONFIGURATION & THEME CONSTANTS
# ==========================================
THEME_BG = "#0f172a"          # Slate 900
THEME_SURFACE = "#1e293b"     # Slate 800
THEME_ACCENT = "#10b981"      # Emerald 500
THEME_ACCENT_HOVER = "#059669"# Emerald 600
THEME_TEXT = "#f8fafc"        # Slate 50
THEME_TEXT_MUTED = "#94a3b8"  # Slate 400
THEME_BORDER = "#334155"      # Slate 700

# ==========================================
# DATABASE CONTROLLER (DATA LAYER)
# ==========================================
class DatabaseController:
    def __init__(self, db_name="coffee_shop.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            # Inventory Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)
            # Sales Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    items_summary TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    tax REAL NOT NULL,
                    discount REAL NOT NULL,
                    total REAL NOT NULL
                )
            """)
            conn.commit()
        self._seed_default_data()

    def _seed_default_data(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Seed Admin Account if empty
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "Admin"))
            
            # Seed Menu Items if empty
            cursor.execute("SELECT COUNT(*) FROM menu")
            if cursor.fetchone()[0] == 0:
                default_items = [
                    ('Espresso', 'Coffee', 3.50),
                    ('Americano', 'Coffee', 4.00),
                    ('Caffè Latte', 'Coffee', 4.50),
                    ('Cappuccino', 'Coffee', 4.50),
                    ('Mocha', 'Coffee', 5.00),
                    ('Matcha Latte', 'Tea', 5.20),
                    ('Croissant', 'Bakery', 3.80),
                    ('Blueberry Muffin', 'Bakery', 4.00),
                    ('Cheesecake', 'Bakery', 5.50)
                ]
                cursor.executemany("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", default_items)
            conn.commit()

    def authenticate(self, username, password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            return cursor.fetchone()

    def fetch_menu(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, category, price FROM menu")
            return cursor.fetchall()

    def log_sale(self, summary, subtotal, tax, discount, total):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO sales (timestamp, items_summary, subtotal, tax, discount, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, summary, subtotal, tax, discount, total))
            conn.commit()

    def fetch_analytics(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total), COUNT(id) FROM sales")
            summary = cursor.fetchone()
            
            cursor.execute("SELECT timestamp, total FROM sales ORDER BY id DESC LIMIT 10")
            recent_sales = cursor.fetchall()
            return summary, recent_sales

# ==========================================
# UI COMPONENTS & WRAPPERS
# ==========================================
class ModernButton(tk.Button):
    def __init__(self, master, text, command=None, variant="primary", **kwargs):
        bg_color = THEME_ACCENT if variant == "primary" else THEME_SURFACE
        fg_color = THEME_TEXT if variant == "primary" else THEME_TEXT_MUTED
        active_bg = THEME_ACCENT_HOVER if variant == "primary" else THEME_BORDER

        super().__init__(
            master, text=text, command=command, bg=bg_color, fg=fg_color,
            activebackground=active_bg, activeforeground=THEME_TEXT, bd=0,
            font=("Segoe UI", 10, "bold"), cursor="hand2", relief="flat", padx=15, pady=8, **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=active_bg))
        self.bind("<Leave>", lambda e: self.config(bg=bg_color))

# ==========================================
# APPLICATION CORE ARCHITECTURE
# ==========================================
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BrewMaster Pro OS — POS System")
        self.geometry("1280x768")
        self.configure(bg=THEME_BG)
        
        self.db = DatabaseController()
        self.current_user = None
        
        # Setup Global UI Styling Configs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", bg=THEME_SURFACE, fg=THEME_TEXT, fieldbg=THEME_SURFACE, 
                        bordercolor=THEME_BORDER, rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", bg=THEME_BORDER, fg=THEME_TEXT, font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[('selected', THEME_ACCENT)], foreground=[('selected', THEME_TEXT)])
        
        # Init Master Container Frame
        self.container = tk.Frame(self, bg=THEME_BG)
        self.container.pack(fill="both", expand=True)
        
        self.show_login_view()

    def switch_view(self, view_class):
        for child in self.container.winfo_children():
            child.destroy()
        frame = view_class(self.container, self)
        frame.pack(fill="both", expand=True)

    def show_login_view(self):
        self.switch_view(LoginView)

    def show_main_app(self):
        self.switch_view(MainWorkspaceView)

# ==========================================
# VIEW: AUTHENTICATION WINDOW
# ==========================================
class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME_BG)
        self.controller = controller
        
        # Layout Engine
        frame = tk.Frame(self, bg=THEME_SURFACE, bd=1, highlightbackground=THEME_BORDER, highlightthickness=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        # Components
        lbl_title = tk.Label(frame, text="BREWMASTER PRO", bg=THEME_SURFACE, fg=THEME_ACCENT, font=("Segoe UI", 20, "bold"))
        lbl_title.pack(pady=(40, 5))
        
        lbl_subtitle = tk.Label(frame, text="Sign in to access your register workspace", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 9))
        lbl_subtitle.pack(pady=(0, 30))
        
        # Form Elements
        wrapper_user = tk.Frame(frame, bg=THEME_SURFACE)
        wrapper_user.pack(fill="x", padx=40, pady=10)
        tk.Label(wrapper_user, text="USERNAME", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.ent_user = tk.Entry(wrapper_user, bg=THEME_BG, fg=THEME_TEXT, insertbackground=THEME_TEXT, bd=0, font=("Segoe UI", 11))
        self.ent_user.pack(fill="x", ipady=8, pady=(4, 0))
        self.ent_user.insert(0, "admin") # Helper Dev Shortcut Default
        
        wrapper_pass = tk.Frame(frame, bg=THEME_SURFACE)
        wrapper_pass.pack(fill="x", padx=40, pady=15)
        tk.Label(wrapper_pass, text="PASSWORD", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.ent_pass = tk.Entry(wrapper_pass, bg=THEME_BG, fg=THEME_TEXT, insertbackground=THEME_TEXT, bd=0, show="*", font=("Segoe UI", 11))
        self.ent_pass.pack(fill="x", ipady=8, pady=(4, 0))
        self.ent_pass.insert(0, "admin123") # Helper Dev Shortcut Default
        
        btn_login = ModernButton(frame, text="AUTHENTICATE SYSTEM", command=self.attempt_login)
        btn_login.pack(fill="x", padx=40, pady=(25, 0))

    def attempt_login(self):
        user = self.ent_user.get()
        password = self.ent_pass.get()
        auth_state = self.controller.db.authenticate(user, password)
        
        if auth_state:
            self.controller.current_user = {"username": user, "role": auth_state[0]}
            self.controller.show_main_app()
        else:
            messagebox.showerror("Security Clearance Failure", "Invalid core system credentials provided.")

# ==========================================
# VIEW: MAIN POS REGISTER WORKSPACE
# ==========================================
class MainWorkspaceView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME_BG)
        self.controller = controller
        self.cart = {}
        
        self._build_scaffolding()
        self._load_menu_data()

    def _build_scaffolding(self):
        # 1. TOP NAV BAR CONTROL ARCHITECTURE
        navbar = tk.Frame(self, bg=THEME_SURFACE, height=65)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        lbl_brand = tk.Label(navbar, text="☕ BREWMASTER POS", bg=THEME_SURFACE, fg=THEME_TEXT, font=("Segoe UI", 14, "bold"))
        lbl_brand.pack(side="left", padx=20)
        
        lbl_session = tk.Label(navbar, text=f"OPERATOR: {self.controller.current_user['username'].upper()} ({self.controller.current_user['role']})", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 9, "bold"))
        lbl_session.pack(side="left", padx=30)

        ModernButton(navbar, text="LOGOUT RUNTIME", variant="secondary", command=self.controller.show_login_view).pack(side="right", padx=15)
        
        # 3-Column Work Area Windowing Layout
        self.left_panel = tk.Frame(self, bg=THEME_BG)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(15, 7), pady=15)
        
        self.center_panel = tk.Frame(self, bg=THEME_BG, width=420)
        self.center_panel.pack(side="left", fill="both", padx=(7, 7), pady=15)
        self.center_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(self, bg=THEME_BG, width=380)
        self.right_panel.pack(side="right", fill="both", padx=(7, 15), pady=15)
        self.right_panel.pack_propagate(False)

        self._build_menu_grid()
        self._build_cart_view()
        self._build_analytics_panel()

    # 2. LEFT PANEL: INTERACTIVE MENU PRODUCTS GRID
    def _build_menu_grid(self):
        lbl_sec = tk.Label(self.left_panel, text="LIVE STATION MENU", bg=THEME_BG, fg=THEME_TEXT, font=("Segoe UI", 12, "bold"))
        lbl_sec.pack(anchor="w", pady=(0, 10))
        
        self.menu_canvas = tk.Canvas(self.left_panel, bg=THEME_BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.left_panel, orient="vertical", command=self.menu_canvas.yview)
        self.grid_frame = tk.Frame(self.menu_canvas, bg=THEME_BG)
        
        self.grid_frame.bind("<Configure>", lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all")))
        self.menu_canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.menu_canvas.pack(side="left", fill="both", expand=True)

    def _load_menu_data(self):
        # Flush existing items if any
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        items = self.controller.db.fetch_menu()
        row, col = 0, 0
        
        for name, category, price in items:
            card = tk.Frame(self.grid_frame, bg=THEME_SURFACE, highlightbackground=THEME_BORDER, highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Setup dynamic uniform layout resizing parameters
            self.grid_frame.columnconfigure(col, weight=1, minsize=160)
            
            lbl_item = tk.Label(card, text=name, bg=THEME_SURFACE, fg=THEME_TEXT, font=("Segoe UI", 11, "bold"), wraplength=140, justify="center")
            lbl_item.pack(pady=(15, 2))
            
            lbl_cat = tk.Label(card, text=category.upper(), bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 7, "bold"))
            lbl_cat.pack()
            
            lbl_price = tk.Label(card, text=f"${price:.2f}", bg=THEME_SURFACE, fg=THEME_ACCENT, font=("Segoe UI", 12, "bold"))
            lbl_price.pack(pady=(10, 15))
            
            # Direct Closure Binding injection tracking card instance metrics
            card.bind("<Button-1>", lambda e, n=name, p=price: self._add_to_cart(n, p))
            lbl_item.bind("<Button-1>", lambda e, n=name, p=price: self._add_to_cart(n, p))
            lbl_price.bind("<Button-1>", lambda e, n=name, p=price: self._add_to_cart(n, p))
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    # 3. CENTER PANEL: TRANSACTION CART BUS ENGINE
    def _build_cart_view(self):
        tk.Label(self.center_panel, text="CURRENT TRANSACTION CART", bg=THEME_BG, fg=THEME_TEXT, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Modern Treeview Core implementation
        wrapper = tk.Frame(self.center_panel, bg=THEME_SURFACE)
        wrapper.pack(fill="both", expand=True)
        
        self.cart_tree = ttk.Treeview(wrapper, columns=("Price", "Qty", "Total"), show="headings", selectmode="browse")
        self.cart_tree.heading("Price", text="PRICE")
        self.cart_tree.heading("Qty", text="QTY")
        self.cart_tree.heading("Total", text="TOTAL")
        
        self.cart_tree.column("#0", width=0, stretch=tk.NO)
        self.cart_tree.column("Price", width=80, anchor="center")
        self.cart_tree.column("Qty", width=60, anchor="center")
        self.cart_tree.column("Total", width=90, anchor="center")
        self.cart_tree.pack(fill="both", expand=True)
        
        # Operational Config Forms Layer
        config_form = tk.Frame(self.center_panel, bg=THEME_SURFACE, highlightbackground=THEME_BORDER, highlightthickness=1)
        config_form.pack(fill="x", pady=(15, 0))
        config_form.configure(padx=15, pady=15)
        
        tk.Label(config_form, text="DISCOUNT CODE OR VALUE ($)", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.ent_discount = tk.Entry(config_form, bg=THEME_BG, fg=THEME_TEXT, insertbackground=THEME_TEXT, bd=0, font=("Segoe UI", 11))
        self.ent_discount.pack(fill="x", ipady=6, pady=(4, 10))
        self.ent_discount.insert(0, "0.00")
        self.ent_discount.bind("<KeyRelease>", lambda e: self._recalculate_totals())

        # Mathematical Transaction Receipt breakdown View
        self.summary_wrapper = tk.Frame(self.center_panel, bg=THEME_SURFACE, padx=15, pady=15, highlightbackground=THEME_BORDER, highlightthickness=1)
        self.summary_wrapper.pack(fill="x", pady=(15, 0))
        
        self.lbl_subtotal = tk.Label(self.summary_wrapper, text="Subtotal: $0.00", bg=THEME_SURFACE, fg=THEME_TEXT, font=("Segoe UI", 10))
        self.lbl_subtotal.pack(anchor="w")
        self.lbl_tax = tk.Label(self.summary_wrapper, text="Tax (GST 13%): $0.00", bg=THEME_SURFACE, fg=THEME_TEXT, font=("Segoe UI", 10))
        self.lbl_tax.pack(anchor="w", pady=2)
        self.lbl_total = tk.Label(self.summary_wrapper, text="Total: $0.00", bg=THEME_SURFACE, fg=THEME_ACCENT, font=("Segoe UI", 14, "bold"))
        self.lbl_total.pack(anchor="w", pady=(5, 10))
        
        ModernButton(self.summary_wrapper, text="CHECKOUT & PRINT INVOICE", command=self._finalize_transaction).pack(fill="x")

    def _add_to_cart(self, name, price):
        if name in self.cart:
            self.cart[name]['qty'] += 1
        else:
            self.cart[name] = {'price': price, 'qty': 1}
        self._refresh_cart_tree()

    def _refresh_cart_tree(self):
        # Wipe rows out UI Cache memory tracking pointer references
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        for name, details in self.cart.items():
            total_item_cost = details['price'] * details['qty']
            # Re-insert structure format variables mappings matching declarations
            self.cart_tree.insert("", "end", iid=name, text=name, values=(f"${details['price']:.2f}", details['qty'], f"${total_item_cost:.2f}"))
            
        # For displaying the custom items column correctly via text reference
        for col in ["Price", "Qty", "Total"]:
            self.cart_tree.heading(col, text=col)
        
        # Override structural anomaly tracking column rendering mechanics 
        self.cart_tree.heading("#0", text="ITEM NAME", anchor="w")
        self.cart_tree.column("#0", width=150, stretch=tk.YES)
        
        self._recalculate_totals()

    def _recalculate_totals(self):
        subtotal = sum(d['price'] * d['qty'] for d in self.cart.values())
        tax = subtotal * 0.13 # Constant standard flat taxation mapping evaluation logic
        
        try:
            discount = float(self.ent_discount.get())
        except ValueError:
            discount = 0.00
            
        total = (subtotal + tax) - discount
        if total < 0: total = 0.00
        
        # Cache variables explicitly to object pointer scope allocation
        self.computed_subtotal = subtotal
        self.computed_tax = tax
        self.computed_discount = discount
        self.computed_total = total
        
        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        self.lbl_tax.config(text=f"Tax (GST 13%): ${tax:.2f}")
        self.lbl_total.config(text=f"Total Amount Due: ${total:.2f}")

    def _finalize_transaction(self):
        if not self.cart:
            messagebox.showwarning("Empty Transaction State", "Cannot commit an empty sales register queue.")
            return
            
        summary_payload = ", ".join([f"{k} (x{v['qty']})" for k, v in self.cart.items()])
        
        # Write Pipeline directly into Data Layer
        self.controller.db.log_sale(
            summary_payload, 
            self.computed_subtotal, 
            self.computed_tax, 
            self.computed_discount, 
            self.computed_total
        )
        
        # Fire Virtual Invoice Pipeline Printer execution
        self._print_receipt_invoice()
        
        # Clean session parameters state cache pipelines
        self.cart.clear()
        self.ent_discount.delete(0, tk.END)
        self.ent_discount.insert(0, "0.00")
        self._refresh_cart_tree()
        self._build_analytics_panel() # Refresh data visualizations engine live updates
        
        messagebox.showinfo("Transaction Finalized", "System successfully logged database records and dispatched dynamic print logs.")

    def _print_receipt_invoice(self):
        receipt_text = f"""
========================================
         BREWMASTER COFFEE SHOP         
========================================
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Operator ID : {self.controller.current_user['username']}
----------------------------------------
Item              Qty     Price    Total
----------------------------------------
"""
        for name, d in self.cart.items():
            tot = d['price'] * d['qty']
            receipt_text += f"{name[:16]:<18} {d['qty']:<7} ${d['price']:<7.2f} ${tot:.2f}\n"
            
        receipt_text += f"""----------------------------------------
Subtotal:                       ${self.computed_subtotal:.2f}
Tax Amount (13%):               ${self.computed_tax:.2f}
Discounts Applied:              ${self.computed_discount:.2f}
========================================
TOTAL CASH PAID:                ${self.computed_total:.2f}
========================================
       THANK YOU FOR YOUR VISIT         
========================================
\n"""
        # Echo print stream context pipeline to stdout log targets terminals
        print(receipt_text)

    # 4. RIGHT PANEL: LIVE BUSINESS BI-ANALYTICS ENGINE
    def _build_analytics_panel(self):
        # Flush existing telemetry UI elements inside container view frame
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        tk.Label(self.right_panel, text="BI BUSINESS TELEMETRY", bg=THEME_BG, fg=THEME_TEXT, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        summary, recent_sales = self.controller.db.fetch_analytics()
        total_revenue = summary[0] if summary[0] else 0.00
        total_tickets = summary[1] if summary[1] else 0
        
        card_rev = tk.Frame(self.right_panel, bg=THEME_SURFACE, padx=15, pady=15, highlightbackground=THEME_BORDER, highlightthickness=1)
        card_rev.pack(fill="x", pady=5)
        tk.Label(card_rev, text="GROSS MATURED REVENUE", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card_rev, text=f"${total_revenue:.2f}", bg=THEME_SURFACE, fg=THEME_ACCENT, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(5, 0))

        card_tkt = tk.Frame(self.right_panel, bg=THEME_SURFACE, padx=15, pady=15, highlightbackground=THEME_BORDER, highlightthickness=1)
        card_tkt.pack(fill="x", pady=10)
        tk.Label(card_tkt, text="TOTAL TRANSACTION TICKETS COMPLETED", bg=THEME_SURFACE, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card_tkt, text=str(total_tickets), bg=THEME_SURFACE, fg=THEME_TEXT, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(5, 0))

        # CUSTOM DATA VISUALIZATION GRAPH CHART ENGINE (PURE RENDER OVER TKINTER CANVAS)
        tk.Label(self.right_panel, text="HISTORICAL TRANSACTION GRAPH (LAST 10 RUNS)", bg=THEME_BG, fg=THEME_TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(15, 5))
        
        canvas_chart = tk.Canvas(self.right_panel, bg=THEME_SURFACE, height=200, bd=0, highlightbackground=THEME_BORDER, highlightthickness=1)
        canvas_chart.pack(fill="x")
        
        if recent_sales:
            max_val = max(x[1] for x in recent_sales)
            if max_val == 0: max_val = 1.00 # Guard against Arithmetic zero-division anomalies
            
            # Rendering engine baseline vector loops
            canvas_width = 340
            canvas_height = 160
            padding_x = 20
            
            # Dynamic vector steps tracking plot counts arrays
            num_points = len(recent_sales)
            step_x = (canvas_width - (padding_x * 2)) / (num_points - 1) if num_points > 1 else (canvas_width - (padding_x * 2))
            
            points = []
            for idx, (_, val) in enumerate(reversed(recent_sales)):
                # Coordinate structural vector projections calculation mappings
                x_coord = padding_x + (idx * step_x)
                normalized_y = (val / max_val) * (canvas_height - 40)
                y_coord = canvas_height - 20 - normalized_y
                points.append((x_coord, y_coord))
                
                # Draw bar vector shapes indicators
                canvas_chart.create_rectangle(x_coord - 6, y_coord, x_coord + 6, canvas_height - 20, fill=THEME_BORDER, outline="")
                canvas_chart.create_rectangle(x_coord - 6, y_coord, x_coord + 6, y_coord + 4, fill=THEME_ACCENT, outline="")
            
            # Connect structural trend line paths vectors overlay pipeline
            if len(points) > 1:
                flat_points = [coord for pt in points for coord in pt]
                canvas_chart.create_line(flat_points, fill=THEME_TEXT_MUTED, width=1, dash=(4, 2))
        else:
            canvas_chart.create_text(170, 100, text="No Historical Dataset Telemetry Found", fill=THEME_TEXT_MUTED, font=("Segoe UI", 10))

# ==========================================
# BOOTSTRAP EXECUTOR PIPELINE ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    app = Application()
    app.mainloop()