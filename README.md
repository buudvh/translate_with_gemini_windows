# Gemini Translator

A desktop application for translating Foreign Language text to Vietnamese using Google's Gemini API. The application features a clean GUI interface and system tray support for Windows.

## Features

- 🌐 Foreign Language to Vietnamese translation using Gemini AI
- 🔍 Word analysis mode for detailed linguistic exploration
- ⌨️ Convenient hotkey support:
  - `Ctrl + C + B`: Quick translate selected text
  - `Ctrl + C` then `Alt + C`: Alternative quick translate method
- 💡 System tray integration for easy access
- 📋 Automatic clipboard integration
- 🖥️ Multi-monitor support
- 🎯 Window appears near cursor position

## Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Required Dependencies

- requests: For API communication
- pillow: For image processing
- pystray: For system tray functionality
- keyboard: For hotkey support
- pyperclip: For clipboard operations
- screeninfo: For multi-monitor support
- pyautogui: For cursor position detection
- PyInstaller: For creating executable

## Configuration

1. Get your Gemini API key from Google
2. On first launch, enter your API key in Settings ⚙️ > Enter API Key
3. The API key will be saved in `config.json` for future use

## Usage

1. Launch the application - it will appear in your system tray
2. You can translate text in two ways:
   - Type or paste text into the "Original Text" box and click "Translate"
   - Use hotkeys to translate selected text from any application
3. Choose between:
   - Translation mode: Standard Foreign Language to Vietnamese translation
   - Word analysis mode: Detailed linguistic analysis of Chinese words/phrases

## Features in Detail

### Translation Mode
- Preserves original context and nuance
- Produces natural, fluent Vietnamese translations
- Maintains proper nouns and terminology consistency
- Optimized for literary and Xianxia/Fantasy style texts

### Word Analysis Mode
- Provides detailed meaning in Vietnamese
- Includes example sentences with translations
- Identifies possible transliterations
- Comprehensive linguistic analysis

### Interface
- Clean, user-friendly design
- Split-pane interface showing original and translated text
- Status indicators for translation progress
- Automatic clipboard management
- System tray integration for minimal footprint

## Building Executable

To create a standalone executable with version info and metadata:

```bash
python -m PyInstaller --noconfirm --onefile --windowed --icon=icon.ico --version-file=file_version_info.txt --add-data "icon.ico;." --add-data "README.md;." --name TranslateGeminiByB app.py
```

Or simply run the build script (Windows):

```powershell
.\build.bat
```

### What this adds to the exe:
- **FileVersion**: 1.0.0.0 (visible in file properties)
- **ProductName**: Gemini Translator
- **ProductVersion**: 1.0.0
- **Copyright**: Copyright © 2025 Hoang Buu. All rights reserved.
- **Description**: Chinese to Vietnamese Translator using Google Gemini API
- **Company**: Hoang Buu

To customize these values, edit `file_version_info.txt` before building.

## Project Structure

```
├── app.py                  # Main application entry point
├── config/
│   └── config_manager.py   # API key management
├── core/
│   └── translator.py       # Translation logic
├── gui/
│   ├── main_window.py     # Main application window
│   └── tray_icon.py       # System tray functionality
└── utils/
    ├── common.py          # Common utilities
    └── hotkey.py          # Hotkey management
```

## License

This project is open-source and available for personal and commercial use.

## Note

This application requires a valid Gemini API key from Google to function. Make sure to keep your API key secure and never share it publicly.