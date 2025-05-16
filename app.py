from tkinter import Tk
from gui.main_window import TranslatorApp
from utils.common import resource_path

if __name__ == "__main__":
    root = Tk()
    root.iconbitmap(resource_path("icon.ico"))
    root.geometry("1000x600")
    app = TranslatorApp(root)
    root.mainloop()
