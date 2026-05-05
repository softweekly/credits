@echo off
echo 🎬 Starting Credits Generator...
echo.

REM Quick start - checks dependencies and installs if missing
if exist ".venv" (
    echo 🔄 Activating virtual environment...
    call .venv\Scripts\activate.bat
    
    REM Verify virtual environment is active
    echo 🔍 Checking Python path...
    .venv\Scripts\python.exe -c "import sys; print('Using Python:', sys.executable)"
    
    REM Check if moviepy is installed in the venv
    .venv\Scripts\python.exe -c "import moviepy.editor" >nul 2>&1
    if errorlevel 1 (
        echo 📥 Installing missing dependencies in virtual environment...
        .venv\Scripts\pip.exe install moviepy==1.0.3 imageio-ffmpeg
        if errorlevel 1 (
            echo ❌ Failed to install dependencies
            echo Run START_CREDITS_GENERATOR.bat for full setup
            pause
            exit /b 1
        )
        echo ✅ Dependencies installed successfully
    ) else (
        echo ✅ MoviePy found in virtual environment
    )
    
    REM Configure MoviePy for ImageMagick
    echo 🔧 Configuring MoviePy...
    .venv\Scripts\python.exe configure_moviepy.py
    
    echo 🚀 Starting Credits Generator...
    .venv\Scripts\python.exe credits_gui.py
) else (
    echo ❌ Virtual environment not found!
    echo Please run START_CREDITS_GENERATOR.bat first to set up the environment
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ❌ Error starting Credits Generator
    echo Run START_CREDITS_GENERATOR.bat for full setup
    pause
)