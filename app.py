from tkinter import Tk
from gui.main_window import TranslatorApp

if __name__ == "__main__":
    root = Tk()
    app = TranslatorApp(root)
    root.geometry("500x600")
    root.mainloop()
