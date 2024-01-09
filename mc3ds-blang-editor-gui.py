import os
import sys
import customtkinter
from PIL import ImageTk

from modules import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --------------------------------------------

        self.title("MC3DS Blang Editor")
        if getattr(sys, 'frozen', False):
            self.app_path = sys._MEIPASS
            self.runningDir = os.path.dirname(sys.executable)
            self.outputFolder = os.path.join(self.runningDir, "MC3DS")
        elif __file__:
            self.app_path = os.path.dirname(__file__)
            self.runningDir = os.path.dirname(__file__)
            self.outputFolder = os.path.join(self.runningDir, "MC3DS")

        self.title("MC3DS Texture Maker")
        os_name = os.name
        if os_name == "nt":
            self.iconbitmap(default=os.path.join(self.app_path, "icon.ico"))
        elif os_name == "posix":
            iconpath = ImageTk.PhotoImage(file=os.path.join(self.app_path, "icon.png"))
            self.wm_iconbitmap()
            self.iconphoto(False, iconpath)

        self.geometry("580x420")
        self.minsize(580, 420)
        self.resizable(True, True)

def closeApp(val=None):
    sys.exit()

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

app = App()

app.bind('<Alt-F4>', closeApp)
app.protocol("WM_DELETE_WINDOW", closeApp)

app.mainloop()