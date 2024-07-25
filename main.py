import tkinter, sys, os
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import argparse
from pathlib import Path

class App(tkinter.Tk):
    def __init__(self, fp = None):
        super().__init__()

        self.title("MC3DS BJSON Editor")
        self.geometry('640x400')
        self.columnconfigure(0, weight=4)
        self.rowconfigure(0, weight=1)

        if getattr(sys, 'frozen', False):
            self.running = "exe"
            self.app_path = sys._MEIPASS
            self.runningDir = os.path.dirname(sys.executable)
        elif __file__:
            self.running = "src"
            self.app_path = os.path.dirname(__file__)
            self.runningDir = os.path.dirname(__file__)

        os_name = os.name
        if os_name == "nt":
            self.iconbitmap(default=os.path.join(self.app_path, "icon.ico"))
        elif os_name == "posix":
            self.wm_iconbitmap()
            self.iconphoto(False, tkinter.PhotoImage(os.path.join(self.app_path, "icon.ico")))
        
        # -------------------------------
        menubar = tkinter.Menu(self)
        self.config(menu=menubar)

        file_menu = tkinter.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Open", command=self.openFile)
        file_menu.add_command(label="Save as", command=self.saveChanges)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.closeApp)

        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        # -------------------------------

        self.tree = ttk.Treeview(self, show='tree', selectmode="browse")
        self.tree.bind('<<TreeviewSelect>>', self.itemSelected)
        self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.filePath = fp
        self.saved = True

        if fp != None:
            inputPath = Path(fp)
            self.title(f"MC3DS BJSON Editor - {inputPath.name}")
            pass

    def itemSelected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            print(record)

    def clearTreeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
    def saveChanges(self):
        pass

    def openFile(self):
        if self.askForChanges():
            inputFp = tkinter.filedialog.askopenfilename(filetypes=[("BLANG Files", ".blang")])
            inputPath = Path(inputFp)
            if inputFp != "":
                self.clearTreeview()
                self.tree.grid_remove()
                self.title(f"MC3DS BJSON Editor - {inputPath.name}")
                self.filePath = inputFp
                self.saved = True
    
    def closeApp(self, val=None):
        if self.saved:
            sys.exit()
        else:
            print("Not saved")
            op = tkinter.messagebox.askyesnocancel(title="Unsaved changes", message="There are unsaved changes. Would you like to save them before exit?")
            if op == True:
                self.saveChanges()
                sys.exit()
            elif op == False:
                sys.exit()
            else:
                pass
    
    def askForChanges(self):
        if self.saved:
            return True
        else:
            print("Not saved")
            op = tkinter.messagebox.askyesnocancel(title="Unsaved changes", message="There are unsaved changes. Would you like to save them?")
            if op == True:
                self.saveChanges()
                return True
            elif op == False:
                return True
            else:
                return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A MC3DS BJSON Editor')
    parser.add_argument('path', nargs='?', type=str, help='File path to open')
    args = parser.parse_args()

    if args.path != None:
        if os.path.exists(args.path):
            app = App(args.path)
    else:
        app = App()

    app.bind('<Alt-F4>', app.closeApp)
    app.protocol("WM_DELETE_WINDOW", app.closeApp)

    app.mainloop()