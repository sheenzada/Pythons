# # import os
# # import asyncio
# # import threading
# # import sqlite3
# # from datetime import datetime
# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# # from uvicorn import Config, Server
# # from kivy.app import App
# # from kivy.uix.boxlayout import BoxLayout
# # from kivy.uix.scrollview import ScrollView
# # from kivy.uix.label import Label
# # from kivy.uix.textinput import TextInput
# # from kivy.uix.button import Button
# # from kivy.clock import Clock
# # from kivy.core.window import Window

# # # ==========================================
# # # 1. BACKEND & DATABASE (FastAPI + SQLite)
# # # ==========================================
# # app = FastAPI()
# # DB_PATH = "chat.db"

# # def init_db():
# #     conn = sqlite3.connect(DB_PATH)
# #     curr = conn.cursor()
# #     curr.execute('''CREATE TABLE IF NOT EXISTS messages 
# #                     (id INTEGER PRIMARY KEY, sender TEXT, content TEXT, timestamp TEXT)''')
# #     conn.commit()
# #     conn.close()

# # class ConnectionManager:
# #     def __init__(self):
# #         self.active_connections: list[WebSocket] = []

# #     async def connect(self, websocket: WebSocket):
# #         await websocket.accept()
# #         self.active_connections.append(websocket)

# #     def disconnect(self, websocket: WebSocket):
# #         self.active_connections.remove(websocket)

# #     async def broadcast(self, message: str):
# #         for connection in self.active_connections:
# #             await connection.send_text(message)

# # manager = ConnectionManager()

# # @app.websocket("/ws")
# # async def websocket_endpoint(websocket: WebSocket):
# #     await manager.connect(websocket)
# #     try:
# #         while True:
# #             data = await websocket.receive_text()
# #             # Save to DB
# #             conn = sqlite3.connect(DB_PATH)
# #             conn.execute("INSERT INTO messages (sender, content, timestamp) VALUES (?, ?, ?)",
# #                          ("User", data, datetime.now().strftime("%H:%M")))
# #             conn.commit()
# #             conn.close()
# #             await manager.broadcast(data)
# #     except WebSocketDisconnect:
# #         manager.disconnect(websocket)

# # def run_server():
# #     init_db()
# #     config = Config(app=app, host="127.0.0.1", port=8000, log_level="info")
# #     server = Server(config)
# #     server.run()

# # # ==========================================
# # # 2. FRONTEND (Kivy UI)
# # # ==========================================


# # class WhatsAppFull(App):
# #     def build(self):
# #         Window.size = (380, 600)
# #         self.root_layout = BoxLayout(orientation='vertical', spacing=0)
        
# #         # Header
# #         header = Label(text="WhatsApp Python Pro", size_hint_y=0.1, color=(1,1,1,1))
# #         self.root_layout.add_widget(header)

# #         # Chat Area
# #         self.scroll = ScrollView(size_hint_y=0.8)
# #         self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
# #         self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
# #         self.scroll.add_widget(self.chat_box)
# #         self.root_layout.add_widget(self.scroll)

# #         # Input Area
# #         input_box = BoxLayout(size_hint_y=0.1, padding=5)
# #         self.msg_input = TextInput(hint_text="Type message...", multiline=False)
# #         send_btn = Button(text=">>", size_hint_x=0.2, on_press=self.send_msg)
# #         input_box.add_widget(self.msg_input)
# #         input_box.add_widget(send_btn)
# #         self.root_layout.add_widget(input_box)

# #         # Load History and Start WebSocket Thread
# #         self.load_history()
# #         threading.Thread(target=self.connect_to_ws, daemon=True).start()
        
# #         return self.root_layout

# #     def load_history(self):
# #         conn = sqlite3.connect(DB_PATH)
# #         rows = conn.execute("SELECT sender, content, timestamp FROM messages ORDER BY id ASC").fetchall()
# #         for r in rows:
# #             self.add_message_to_ui(f"[{r[2]}] {r[0]}: {r[1]}")
# #         conn.close()

# #     def add_message_to_ui(self, text):
# #         lbl = Label(text=text, size_hint_y=None, height=40, color=(0.8, 0.8, 0.8, 1), halign="left")
# #         lbl.bind(size=lbl.setter('text_size'))
# #         self.chat_box.add_widget(lbl)

# #     def send_msg(self, instance):
# #         import websocket # pip install websocket-client
# #         msg = self.msg_input.text
# #         if msg:
# #             ws = websocket.create_connection("ws://127.0.0.1:8000/ws")
# #             ws.send(msg)
# #             ws.close()
# #             self.msg_input.text = ""

# #     def connect_to_ws(self):
# #         import websocket
# #         ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws",
# #                                     on_message=lambda ws, msg: Clock.schedule_once(lambda dt: self.add_message_to_ui(f"New: {msg}")))
# #         ws.run_forever()

# # # ==========================================
# # # 3. EXECUTION
# # # ==========================================
# # if __name__ == "__main__":
# #     # Start Backend in a separate thread
# #     threading.Thread(target=run_server, daemon=True).start()
    
# #     # Wait for server to boot, then start Frontend
# #     WhatsAppFull().run()


# import sys
# import time
# import sqlite3
# import threading
# import multiprocessing
# from datetime import datetime

# # --- THIRD PARTY IMPORTS ---
# # pip install fastapi uvicorn kivy websocket-client
# try:
#     from fastapi import FastAPI, WebSocket, WebSocketDisconnect
#     import uvicorn
#     from kivy.app import App
#     from kivy.uix.boxlayout import BoxLayout
#     from kivy.uix.scrollview import ScrollView
#     from kivy.uix.label import Label
#     from kivy.uix.textinput import TextInput
#     from kivy.uix.button import Button
#     from kivy.clock import Clock
#     from kivy.core.window import Window
#     import websocket 
# except ImportError as e:
#     print(f"Missing Library: {e}. Please run: pip install fastapi uvicorn kivy websocket-client")
#     sys.exit()

# # ==========================================
# # 1. DATABASE LAYER
# # ==========================================
# DB_PATH = "whatsapp_pro.db"

# def init_db():
#     with sqlite3.connect(DB_PATH) as conn:
#         conn.execute('''CREATE TABLE IF NOT EXISTS chat_logs 
#                         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                          sender TEXT, message TEXT, time TEXT)''')

# # ==========================================
# # 2. BACKEND (FastAPI) - Runs in Background
# # ==========================================
# backend_app = FastAPI()

# class ChatManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, ws: WebSocket):
#         await ws.accept()
#         self.active_connections.append(ws)

#     def disconnect(self, ws: WebSocket):
#         self.active_connections.remove(ws)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

# manager = ChatManager()

# @backend_app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Save to Database
#             with sqlite3.connect(DB_PATH) as conn:
#                 conn.execute("INSERT INTO chat_logs (sender, message, time) VALUES (?, ?, ?)",
#                              ("User", data, datetime.now().strftime("%H:%M")))
#             await manager.broadcast(data)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# def start_server():
#     init_db()
#     uvicorn.run(backend_app, host="127.0.0.1", port=8001, log_level="error")

# # ==========================================
# # 3. FRONTEND (Kivy UI)
# # ==========================================
# class ProChatUI(App):
#     def build(self):
#         Window.size = (400, 700)
#         Window.clearcolor = (0.05, 0.07, 0.09, 1) # Dark theme
        
#         self.layout = BoxLayout(orientation='vertical')
        
#         # Navbar
#         nav = Label(text="CHATS", size_hint_y=0.08, bold=True, color=(0.07, 0.82, 0.4, 1))
#         self.layout.add_widget(nav)

#         # Message Area
#         self.scroll = ScrollView(size_hint_y=0.82)
#         self.msg_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=20)
#         self.msg_list.bind(minimum_height=self.msg_list.setter('height'))
#         self.scroll.add_widget(self.msg_list)
#         self.layout.add_widget(self.scroll)

#         # Footer Input
#         footer = BoxLayout(size_hint_y=0.1, padding=10, spacing=10)
#         self.input = TextInput(hint_text="Type a message...", multiline=False, background_color=(0.1, 0.15, 0.2, 1), foreground_color=(1,1,1,1))
#         self.input.bind(on_text_validate=self.send_action)
        
#         send_btn = Button(text="SEND", size_hint_x=0.2, background_color=(0.07, 0.82, 0.4, 1))
#         send_btn.bind(on_press=self.send_action)
        
#         footer.add_widget(self.input)
#         footer.add_widget(send_btn)
#         self.layout.add_widget(footer)

#         # Start Listening thread
#         threading.Thread(target=self.listen_to_server, daemon=True).start()
#         return self.layout

#     def add_bubble(self, text, is_new=True):
#         bubble = Label(text=text, size_hint_y=None, height=45, color=(1,1,1,1), halign="left")
#         bubble.bind(size=bubble.setter('text_size'))
#         self.msg_list.add_widget(bubble)
#         if is_new:
#             self.scroll.scroll_y = 0

#     def send_action(self, *args):
#         val = self.input.text
#         if val:
#             try:
#                 ws = websocket.create_connection("ws://127.0.0.1:8001/ws")
#                 ws.send(val)
#                 ws.close()
#                 self.input.text = ""
#             except Exception as e:
#                 self.add_bubble(f"Error: Server not ready. {e}")

#     def listen_to_server(self):
#         # Give server a second to start
#         time.sleep(2)
#         def on_message(ws, msg):
#             Clock.schedule_once(lambda dt: self.add_bubble(f"> {msg}"))

#         ws_app = websocket.WebSocketApp("ws://127.0.0.1:8001/ws", on_message=on_message)
#         ws_app.run_forever()

# # ==========================================
# # 4. MAIN ENTRY POINT
# # ==========================================
# if __name__ == "__main__":
#     # Start the FastAPI server in a separate process to avoid GIL locking
#     server_proc = multiprocessing.Process(target=start_server, daemon=True)
#     server_proc.start()
    
#     # Start the Kivy Frontend
#     ProChatUI().run()


import sys
import time
import sqlite3
import threading
import multiprocessing
from datetime import datetime

# 1. ATTEMPT IMPORTS
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    import uvicorn
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.clock import Clock
    from kivy.core.window import Window
    import websocket # From 'websocket-client'
except ImportError as e:
    print(f"ERROR: {e}. Run: pip install fastapi uvicorn kivy websocket-client")
    sys.exit()

# 2. DATABASE SETUP
DB_NAME = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS logs (sender TEXT, msg TEXT, time TEXT)")

# 3. BACKEND SERVER (FastAPI)
server_app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@server_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO logs VALUES (?, ?, ?)", ("User", data, datetime.now().strftime("%H:%M")))
            await manager.broadcast(data)
    except Exception:
        pass

def run_backend():
    init_db()
    uvicorn.run(server_app, host="127.0.0.1", port=8002, log_level="error")

# 4. FRONTEND APP (Kivy)
class WhatsAppClone(App):
    def build(self):
        Window.size = (350, 600)
        self.root = BoxLayout(orientation='vertical')
        
        # Chat Display
        self.scroll = ScrollView()
        self.chat_log = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.chat_log.bind(minimum_height=self.chat_log.setter('height'))
        self.scroll.add_widget(self.chat_log)
        self.root.add_widget(self.scroll)

        # Input Area
        input_area = BoxLayout(size_hint_y=0.1)
        self.txt = TextInput(hint_text="Type...", multiline=False)
        btn = Button(text="Send", size_hint_x=0.3, on_press=self.send_msg)
        input_area.add_widget(self.txt)
        input_area.add_widget(btn)
        self.root.add_widget(input_area)

        threading.Thread(target=self.receive_loop, daemon=True).start()
        return self.root

    def send_msg(self, *args):
        if self.txt.text:
            try:
                ws = websocket.create_connection("ws://127.0.0.1:8002/ws")
                ws.send(self.txt.text)
                ws.close()
                self.txt.text = ""
            except: self.add_msg("Server Error")

    def add_msg(self, text):
        self.chat_log.add_widget(Label(text=text, size_hint_y=None, height=30, color=(0,1,0,1)))

    def receive_loop(self):
        time.sleep(2) # Wait for server
        def on_msg(ws, msg):
            Clock.schedule_once(lambda dt: self.add_msg(f"Recv: {msg}"))
        ws_app = websocket.WebSocketApp("ws://127.0.0.1:8002/ws", on_message=on_msg)
        ws_app.run_forever()

# 5. EXECUTION
if __name__ == "__main__":
    # Start server in a separate process
    p = multiprocessing.Process(target=run_backend, daemon=True)
    p.start()
    
    # Start Kivy
    WhatsAppClone().run()