import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Menu
from config.config_manager import load_api_key, save_api_key
from core.translator import translate_with_gemini
from gui.tray_icon import create_tray_icon
from utils.hotkey import setup_hotkey
from screeninfo import get_monitors
import pyautogui
import threading

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
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
        settings_menu.add_command(label="Enter API Key", command=self.enter_api_key)
        menubar.add_cascade(label="⚙ Settings", menu=settings_menu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Use guide", command=self.show_help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
    
    def show_help(self):
        messagebox.showinfo(
            "Hướng dẫn sử dụng",
            "➤ Bấm Ctrl+C+V để dịch nhanh đoạn văn bản đã bôi đen.\n"
            "➤ Bạn cần nhập API key trước khi sử dụng lần đầu.\n"
            "➤ Kết quả dịch sẽ hiển thị bên dưới.\n"
            "➤ Menu này có thể dùng để xem hướng dẫn bất kỳ lúc nào 😎."
        )

    def enter_api_key(self):
        key = simpledialog.askstring("Enter API Key", "Pass your API key here:", show="*", parent=self.root)
        if key:
            self.api_key = key
            save_api_key(key)
            messagebox.showinfo("Success", "API key entered successfully!")

    def create_widgets(self):
        self.root.update()

        total_width = self.root.winfo_width()
        total_height = self.root.winfo_height()

        middle_width = 80
        side_width = (total_width - middle_width) // 2 - 10 -10
        frame_height = total_height - 70

        self.original_frame = tk.LabelFrame(self.root, text="Original Text")
        self.original_frame.place(x=10, y=10, width=side_width, height=frame_height)

        self.original_text = tk.Text(self.original_frame, wrap="word",padx=5, pady=5)
        self.original_text.pack(fill="both", expand=True, padx=5, pady=5)

        middle_x = 10 + side_width + 10
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.place(x=middle_x, y=frame_height//2, width=middle_width, height=40)

        self.translate_btn = ttk.Button(self.middle_frame, text="Translate", command=self.translate)
        self.translate_btn.pack(fill="both", expand=True)

        translated_x = middle_x + middle_width + 10
        translated_width = total_width - translated_x - 10
        self.translated_frame = tk.LabelFrame(self.root, text="Translated Text")
        self.translated_frame.place(x=translated_x, y=10, width=translated_width, height=frame_height)

        self.translated_text = tk.Text(self.translated_frame, wrap="word", padx=5, pady=5)
        self.translated_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.close_btn = ttk.Button(self.root, text="❌ Close", command=self.on_closing)
        self.close_btn.place(x=total_width - 90, y=total_height - 50, width=80, height=30)
    
    def translate(self):
        input_text = self.original_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to translate.")
            return
        
        if not self.api_key:
            messagebox.showwarning("Warning", "Please enter your API key.")
            self.enter_api_key()
            return
        
        self.show_loading_overlay()
        threading.Thread(target=self._do_translate, args=(input_text,), daemon=True).start()

    def _do_translate(self, input_text):
        try:
            result = translate_with_gemini(input_text, self.api_key)
            self.root.after(0, lambda: self._show_result(result))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, self.hide_loading_overlay)

    def _show_result(self, result):
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
        tk.Label(self.loading_overlay, text="⏳ Translating...", font=("Meiryo UI", 12, "bold"), bg='gray90').pack(expand=True)

    def hide_loading_overlay(self):
        if self.loading_overlay:
            self.loading_overlay.destroy()
            self.loading_overlay = None

    def move_window_to_cursor_screen(self):
        try:
            cursor_x, cursor_y = pyautogui.position()
            for monitor in get_monitors():
                if monitor.x <= cursor_x < monitor.x + monitor.width and monitor.y <= cursor_y < monitor.y + monitor.height:
                    win_w = self.root.winfo_width()
                    win_h = self.root.winfo_height()
                    pos_x = monitor.x + (monitor.width - win_w) // 2
                    pos_y = monitor.y + (monitor.height - win_h) // 2
                    self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
                    break
        except Exception as e:
            print("Lỗi khi di chuyển cửa sổ:", e)