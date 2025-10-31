import keyboard
import pyperclip
import time
import threading
from tkinter import messagebox
import tkinter as tk
from screeninfo import get_monitors
from core.translator import translate_with_gemini
import subprocess

def setup_hotkey(app):
    # type 1: Ctrl+C+B
    keyboard.add_hotkey("ctrl+c+b", lambda: threading.Thread(target=handle_clipboard, args=(app,), daemon=True).start())

    # type 2: Ctrl+C then Alt+C
    def sequence_listener():
        threading.Thread(target=wait_alt_c_then_handle, args=(app,), daemon=True).start()

    keyboard.add_hotkey("ctrl+c", sequence_listener)

def wait_alt_c_then_handle(app):
    time.sleep(0.1)  # wait for clipboard to be updated
    selected_text = pyperclip.paste()
    if not selected_text.strip():
        return
    try:
        keyboard.wait("alt+c")  # wait for alt+c
        handle_clipboard(app, selected_text)
    except:
        pass  # user may not press alt+c, so we just ignore the error

def handle_clipboard(app, preloaded_text=None):
    try:
        selected_text = preloaded_text or pyperclip.paste()
        if not selected_text.strip():
            return

        app.move_window_to_cursor_screen()
        app.show_window()
        app.original_text.delete("1.0", tk.END)
        app.original_text.insert(tk.END, selected_text)
        app.translated_text.delete("1.0", tk.END)
        app.translated_text.insert(tk.END, "")
        app.show_loading_overlay()

        if not app.api_key:
            app.hide_loading_overlay()
            messagebox.showwarning("Warning", "Please enter your API key.")
            app.root.after(0, app.enter_api_key)
            return

        result = translate_with_gemini(selected_text, app.api_key)
        app.copy_to_clipboard(result)
        app.hide_loading_overlay()
        app.translated_text.delete("1.0", tk.END)
        app.translated_text.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
