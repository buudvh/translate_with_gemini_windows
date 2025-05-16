import keyboard
import pyperclip
import time
import threading
from tkinter import messagebox
import tkinter as tk
from screeninfo import get_monitors
from core.translator import translate_with_gemini

def setup_hotkey(app):
    def hotkey_handler():
        threading.Thread(target=listen_hotkey, args=(app,)).start()

    keyboard.add_hotkey("ctrl+c+b", hotkey_handler)

def listen_hotkey(app):
        while True:
            keyboard.wait("ctrl+c+b")
            time.sleep(0.1)  # Chờ clipboard cập nhật
            try:
                selected_text = pyperclip.paste()
                if selected_text.strip():
                    app.move_window_to_cursor_screen()
                    app.show_window()
                    app.original_text.delete("1.0", tk.END)
                    app.original_text.insert(tk.END, selected_text)
                    app.show_loading_overlay()
                    if not app.api_key:
                        app.hide_loading_overlay()
                        messagebox.showwarning("Warning", "Please enter your API key.")
                        app.root.after(0, app.enter_api_key)
                        return
                    result = translate_with_gemini(selected_text, app.api_key)
                    app.hide_loading_overlay()
                    app.translated_text.delete("1.0", tk.END)
                    app.translated_text.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:", e)
