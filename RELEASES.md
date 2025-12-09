# Release Notes

## Version 1.0.4.0 (December 9, 2025)

### 🐛 Bug Fixes
- **AI Model Fix**: Ensured Gemini 2.5 Flash model is properly configured and validated
  - Model endpoint: `gemini-2.5-flash:generateContent`
  - This resolves runtime issues with older model versions
- **Error Handling**: Fixed f-string quote escaping issue in HTTP error handling
  - Properly handles malformed or unexpected API responses
  - Added defensive access to nested API response structures

### 🔧 Improvements
- Enhanced error message parsing from API responses
- Improved robustness when API response structure is unexpected
- Better fallback handling when required fields are missing

### 📝 What Changed
- ✅ Updated `core/translator.py` — Fixed error handling and ensured Gemini 2.5 compatibility

---

## Version 1.0.3.0 (December 9, 2025)

### ✨ New Features
- **Version metadata embedding**: Executable now includes proper file version, product name, product version, and copyright information
  - FileVersion: 1.0.3.0
  - ProductName: Gemini Translator
  - ProductVersion: 1.0.3.0
  - Copyright: © 2025 Hoang Buu. All rights reserved.
  - These values are visible in Windows file properties (Right-click exe > Properties > Details)

### 🔧 Improvements
- Added `file_version_info.txt` configuration file for PyInstaller version metadata
- Created `build.bat` batch script for simplified Windows builds with automatic version info inclusion
- Updated build documentation with new PyInstaller command using `--version-file` parameter
- Enhanced README with details about customizing version information before builds

### 📋 How to Build
Simply run the new build script:
```powershell
.\build.bat
```

Or manually use PyInstaller with the version file:
```bash
python -m PyInstaller --noconfirm --onefile --windowed --icon=icon.ico --version-file=file_version_info.txt --add-data "icon.ico;." --add-data "README.md;." --name TranslateGeminiByB app.py
```

### 📝 Files Changed
- ✅ Added `file_version_info.txt` — Version metadata configuration
- ✅ Added `build.bat` — Automated Windows build script
- ✅ Updated `README.md` — Build instructions with version info details

### 🎯 Next Steps for Users
To customize the version information for your builds:
1. Edit `file_version_info.txt`
2. Modify the following fields as needed:
   - `filevers=(1, 0, 3, 0)` — File version (major, minor, build, revision)
   - `prodvers=(1, 0, 3, 0)` — Product version
   - `FileVersion` string — Display version in properties
   - `ProductVersion` string — Display product version
   - `LegalCopyright` — Copyright notice
   - `CompanyName` — Company/author name
3. Rebuild using `.\build.bat` or the manual PyInstaller command

---

## Version 1.0.0 (Initial Release)

### Features
- Chinese to Vietnamese translation using Google's Gemini AI
- Word analysis mode for detailed linguistic exploration
- Global hotkey support (Ctrl+C+B and Ctrl+C then Alt+C)
- System tray integration
- Automatic clipboard handling
- Multi-monitor support with window repositioning
- API key management via GUI
- PyInstaller-compatible packaging

### Supported OS
- Windows 10/11
