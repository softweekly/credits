@echo off
echo.
echo ================================================================
echo          🎬 CREDITS GENERATOR - QUICK START INSTALLER 🎬
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.7+ 
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Restart this script after installation
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

REM Check if ImageMagick is installed
if exist "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe" (
    echo ✅ ImageMagick found
) else (
    if exist "C:\Program Files\ImageMagick*\magick.exe" (
        echo ✅ ImageMagick found (different version)
    ) else (
        echo ⚠️  ImageMagick not found at default location
        echo.
        echo This is required for text rendering. Please install:
        echo 1. Go to: https://imagemagick.org/script/download.php#windows
        echo 2. Download: ImageMagick-7.x.x-Q16-HDRI-x64-dll.exe
        echo 3. Install to default location
        echo 4. Restart this script after installation
        echo.
        echo Continue anyway? (The GUI will start but video generation may fail)
        set /p choice="Press Y to continue, or any key to exit: "
        if /i not "%choice%"=="y" exit /b 1
    )
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo.
echo 🔍 Checking dependencies...
python -c "import moviepy; print('MoviePy:', moviepy.__version__)" 2>nul
if errorlevel 1 (
    echo 📥 Installing Python dependencies...
    pip install --upgrade pip
    pip install moviepy[optional] imageio-ffmpeg
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        echo.
        echo Trying alternative installation...
        pip install moviepy imageio-ffmpeg
    )
) else (
    echo ✅ Dependencies already installed
)

REM Verify installation
echo.
echo 🧪 Testing installation...
python -c "
import moviepy
import tkinter
print('✅ All modules imported successfully!')
print('🎬 Ready to generate credits!')
" 2>nul

if errorlevel 1 (
    echo ❌ Some modules failed to import
    echo Attempting to fix...
    pip install --force-reinstall moviepy[optional]
)

echo.
echo ================================================================
echo                    🚀 LAUNCHING CREDITS GENERATOR
echo ================================================================
echo.
echo Usage Tips:
echo • Use the "Credits Editor" tab to add/edit your credits
echo • Try the "Appearance" tab to change colors and backgrounds  
echo • Check "Settings" tab for video options
echo • Click "Preview Text" before generating to see layout
echo.

REM Launch the GUI
python credits_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Failed to start Credits Generator
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python and ImageMagick are properly installed
    echo 2. Check that all dependencies installed correctly
    echo 3. Try running: python credits_gui.py manually
    echo.
    pause
) else (
    echo.
    echo 👋 Credits Generator closed successfully!
)

echo.
echo Press any key to exit...
pause >nul