from PIL import Image, ImageDraw
import pystray
import threading
from utils.common import resource_path

def create_tray_icon(app):
    image = Image.open(resource_path("icon.ico"))

    menu = pystray.Menu(
        pystray.MenuItem("Open Gemini Translator", lambda i, x: app.show_window()),
        pystray.MenuItem("Exit", lambda i, x: exit_app(app))
    )

    app.icon = pystray.Icon("GeminiTranslator", image, "Gemini Translator", menu)
    
    app.is_tray_active = True

    threading.Thread(target=app.icon.run, daemon=True).start()

def exit_app(app):
    app.icon.stop()
    app.root.destroy()
