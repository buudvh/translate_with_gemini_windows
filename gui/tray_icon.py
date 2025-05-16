from PIL import Image, ImageDraw
import pystray
import threading

def create_tray_icon(app):
    image = Image.new('RGB', (64, 64), (0, 120, 215))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill=(255, 255, 255))

    menu = pystray.Menu(
        pystray.MenuItem("Mở Gemini Translator", lambda i, x: app.show_window()),
        pystray.MenuItem("Thoát", lambda i, x: exit_app(app))
    )

    app.icon = pystray.Icon("GeminiTranslator", image, "Gemini Translator", menu)
    
    app.is_tray_active = True

    threading.Thread(target=app.icon.run, daemon=True).start()

def exit_app(app):
    app.icon.stop()
    app.root.destroy()
