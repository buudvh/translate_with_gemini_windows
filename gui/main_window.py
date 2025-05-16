import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Menu
from config.config_manager import load_api_key, save_api_key
from core.translator import translate_with_gemini
from gui.tray_icon import create_tray_icon
from utils.hotkey import setup_hotkey
from screeninfo import get_monitors
import pyautogui

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Translator")
        self.api_key = load_api_key()

        self.default_font = ("Meiryo UI", 11)
        self.root.option_add("*Font", self.default_font)

        self.create_menu()
        self.create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.icon = None
        self.is_tray_active = False

        self.loading_overlay = None

        setup_hotkey(self)

    def on_closing(self):
        self.hide_window()
        if not self.is_tray_active:
            create_tray_icon(self)

    def hide_window(self):
        self.root.withdraw()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Nhập API Key", command=self.enter_api_key)
        menubar.add_cascade(label="⚙ Cài đặt", menu=settings_menu)

    def enter_api_key(self):
        key = simpledialog.askstring("Nhập API Key", "Dán API Key của Gemini vào đây:", show="*")
        if key:
            self.api_key = key
            save_api_key(key)
            messagebox.showinfo("Thành công", "Đã lưu API Key!")

    def create_widgets(self):
        # Original Text
        original_frame = ttk.LabelFrame(self.root, text="Original Text")
        original_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.original_text = tk.Text(original_frame, height=6, wrap=tk.WORD)
        self.original_text.pack(fill="both", expand=True, padx=5, pady=5)

        translate_btn = ttk.Button(self.root, text="Translate", command=self.translate)
        translate_btn.pack(pady=5)

        # Translated Text
        translated_frame = ttk.LabelFrame(self.root, text="Translated Text")
        translated_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.translated_text = tk.Text(translated_frame, height=6, wrap=tk.WORD)
        self.translated_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Close Button
        close_btn = ttk.Button(self.root, text="Close", command=self.on_closing)
        close_btn.pack(pady=10)
    
    def translate(self):
        input_text = self.original_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần dịch.")
            return
        
        if not self.api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập API Key trước khi dịch.")
            return
        
        self.show_loading_overlay()
        result = translate_with_gemini(input_text, self.api_key)
        self.hide_loading_overlay()
        self.translated_text.delete("1.0", tk.END)
        self.translated_text.insert(tk.END, result)

    def show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(0, lambda: self.root.attributes('-topmost', False))
        self.root.after(0, self.root.focus_force)

    def show_loading_overlay(self):
        if self.loading_overlay:
            return
        self.loading_overlay = tk.Toplevel(self.root)
        self.loading_overlay.overrideredirect(True)
        self.loading_overlay.attributes("-topmost", True)
        self.loading_overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_rootx()}+{self.root.winfo_rooty()}")
        self.loading_overlay.configure(bg='gray90')
        tk.Label(self.loading_overlay, text="⏳ Đang dịch...", font=("Meiryo UI", 12, "bold"), bg='gray90').pack(expand=True)

    def hide_loading_overlay(self):
        if self.loading_overlay:
            self.loading_overlay.destroy()
            self.loading_overlay = None

    def move_window_to_cursor_screen(self):
        try:
            cursor_x, cursor_y = pyautogui.position()
            for monitor in get_monitors():
                if monitor.x <= cursor_x < monitor.x + monitor.width and monitor.y <= cursor_y < monitor.y + monitor.height:
                    win_w, win_h = 500, 600  # kích thước cửa sổ
                    pos_x = monitor.x + (monitor.width - win_w) // 2
                    pos_y = monitor.y + (monitor.height - win_h) // 2
                    self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
                    break
        except Exception as e:
            print("Lỗi khi di chuyển cửa sổ:", e)