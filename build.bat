@echo off
REM Build script for Megallm Translator with version info
REM Usage: .\build.bat

setlocal enabledelayedexpansion

echo Building Megallm Translator executable...
echo.

if not exist "file_version_info.txt" (
    echo Error: file_version_info.txt not found!
    echo Make sure you're running this script from the project root directory.
    exit /b 1
)

echo Running PyInstaller...
python -m PyInstaller --noconfirm --onefile --windowed ^
  --icon=icon.ico ^
  --version-file=file_version_info.txt ^
  --add-data "icon.ico;." ^
  --add-data "README.md;." ^
  --name TranslateMegallmByB ^
  app.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo Build completed successfully!
    echo Your executable is in: dist\TranslateMegallmByB.exe
    echo.
    echo You can verify the version info by:
    echo  - Right-click the exe and select "Properties"
    echo  - Check the "Details" tab
) else (
    echo Build failed!
    exit /b 1
)

endlocal
