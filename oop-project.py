import tkinter as tk
from views.dashboard import DashboardView
from views.settings import SettingsView

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enterprise Project v1.0")
        self.geometry("1024x768")

        # Central container for all views
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        
        # Registering all views
        for F in (DashboardView, SettingsView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DashboardView")

    def show_frame(self, page_name):
        """Switches the visible window/view"""
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.mainloop()