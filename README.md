# 🎬 Credits Generator

Create professional movie-style scrolling credits videos with an easy-to-use graphical interface!

![Credits Generator Preview](https://img.shields.io/badge/Platform-Windows-blue) ![Python](https://img.shields.io/badge/Python-3.7+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎯 Easy GUI Interface** - No coding required!
- **🎨 Custom Colors** - Text and background color pickers
- **🖼️ Background Images** - Upload your own background images
- **📝 Flexible Credits** - Headers, names, role/name pairs, and custom spacing
- **⚙️ Multiple Formats** - Support for 1080p, 720p, 4K resolutions
- **💾 Save Projects** - Save and load your credit configurations
- **📺 Live Preview** - See your credits before generating the video

## 🚀 Installation Guide

### Option 1: Automated Setup (Recommended for Beginners)
1. **Download the repository:**
   - Click the green "Code" button on GitHub
   - Select "Download ZIP"
   - Extract to your desired location (e.g., `C:\Credits\`)

2. **Run the automated installer:**
   - **Double-click** `START_CREDITS_GENERATOR.bat`
   - The script will automatically:
     - Check if Python is installed
     - Create a virtual environment
     - Install all required dependencies
     - Launch the Credits Generator

3. **That's it!** 🎉 The application should open automatically.

### Option 2: Manual Installation (Advanced Users)

#### Prerequisites
- **Windows 10/11**
- **Python 3.7 or higher** ([Download Python](https://www.python.org/downloads/))
- **ImageMagick** ([Download ImageMagick](https://imagemagick.org/script/download.php#windows))

#### Detailed Step-by-Step Installation

**Step 1: Install Python**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x version
3. **IMPORTANT:** During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users" (optional)
4. Verify installation: Open Command Prompt and type `python --version`

**Step 2: Install ImageMagick**
1. Go to [ImageMagick Downloads](https://imagemagick.org/script/download.php#windows)
2. Download: `ImageMagick-7.x.x-Q16-HDRI-x64-dll.exe`
3. Install to default location: `C:\Program Files\ImageMagick-...`
4. ✅ Make sure "Install development headers" is checked

**Step 3: Set Up Virtual Environment (Recommended)**
1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```cmd
   cd C:\path\to\credits-generator
   ```
3. Create virtual environment:
   ```cmd
   python -m venv .venv
   ```
4. Activate virtual environment:
   ```cmd
   # For Command Prompt:
   .venv\Scripts\activate.bat
   
   # For PowerShell:
   .venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

**Step 4: Launch the Application**
```cmd
python credits_gui.py
```

## 🔧 Troubleshooting

### Python Installation Issues
- **"python is not recognized"**: Python is not in PATH. Reinstall Python with "Add to PATH" checked
- **Permission errors**: Run Command Prompt as Administrator
- **Old Python version**: This app requires Python 3.7+. Update your Python installation

### ImageMagick Issues
- **"ImageMagick not found"**: Make sure ImageMagick is installed and in your system PATH
- **Policy errors**: Some ImageMagick installations have restrictive policies. You may need to edit the policy.xml file

### Virtual Environment Issues
- **PowerShell execution policy**: Run this command first:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
- **Virtual environment not activating**: Make sure you're in the correct directory

### Dependency Installation Issues
- **pip install fails**: Try upgrading pip first:
  ```cmd
  python -m pip install --upgrade pip
  ```
- **Specific package fails**: Some packages may need Microsoft Visual C++ Build Tools

## 🚀 Quick Start After Installation

### First Time Setup
1. **Launch the application** using one of these methods:
   - Double-click `QUICK_START.bat` (if you used automated setup)
   - Or run `python credits_gui.py` in your activated virtual environment

2. **Create your first credits video:**
   - Go to the **Credits Editor** tab
   - Add a header: Select "Header", type "DIRECTED BY", click "Add Entry"
   - Add a name: Select "Name", type "YOUR NAME", click "Add Entry"
   - Go to **Settings** tab and choose your preferences
   - Click **"Generate Video"** to create your credits!

### Understanding the Files

| File | Purpose |
|------|---------|
| `START_CREDITS_GENERATOR.bat` | Full setup script - installs everything and runs the app |
| `QUICK_START.bat` | Quick launcher for after initial setup |
| `credits_gui.py` | Main application file |
| `requirements.txt` | List of Python packages needed |
| `.gitignore` | Excludes video files and virtual environment from git |

### What Gets Installed

When you run the setup, these Python packages are installed:
- **MoviePy 1.0.3** - Video editing and generation
- **ImageIO-FFmpeg** - Video codec support  
- **Pillow** - Image processing (automatically installed with MoviePy)
- **NumPy** - Numerical operations (automatically installed with MoviePy)

The virtual environment (`.venv` folder) keeps these packages separate from your system Python installation.

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space (more for video output)
- **Python**: 3.7 or higher

### For Best Performance
- **RAM**: 8GB+ for larger videos (4K, long duration)
- **CPU**: Multi-core processor for faster video generation
- **Storage**: SSD for faster video processing

## ❓ Frequently Asked Questions

### Q: Do I need to install anything else?
A: No! The automated setup installs everything you need. Just make sure you have Python installed first.

### Q: Can I use this on Mac or Linux?
A: The app itself can work on Mac/Linux, but the `.bat` files are Windows-only. You'd need to manually set up the virtual environment and run the Python files directly.

### Q: Where are my generated videos saved?
A: By default, videos are saved in the same folder as the application. You can change this in the Settings tab.

### Q: How long does video generation take?
A: Depends on video length and resolution:
- 720p, 60 seconds: ~30 seconds
- 1080p, 90 seconds: ~1-2 minutes  
- 4K, 120 seconds: ~5+ minutes

### Q: Can I add background music?
A: Not currently built-in, but you can add music to the generated video using any video editor.

### Q: The app won't start - what should I do?
A: Try these steps:
1. Make sure Python is installed and in PATH
2. Run as Administrator
3. Check the troubleshooting section above
4. Create an issue on GitHub with error details

## 📖 How to Use

### 1. **Credits Editor Tab**
- **View all credits** in the interactive table
- **Add entries:** Select type (header/name/pair/spacer), fill fields, click "Add Entry"
- **Edit entries:** Click an entry to select it, modify fields, click "Update Selected"
- **Reorder:** Use "Move Up" and "Move Down" buttons
- **Delete:** Select entry and click "Delete Selected"

### 2. **Appearance Tab**
- **Text Color:** Click color button to choose text color
- **Background Color:** Click color button to choose background color  
- **Background Image:** Click "Select Image" to upload custom backgrounds
- **Clear Image:** Remove background image to use solid color

### 3. **Settings Tab**
- **Duration:** Video length in seconds (default: 90)
- **Resolution:** Choose from 720p, 1080p, 4K options
- **FPS:** Frame rate (default: 30)
- **Font:** Select font family
- **Output File:** Choose output filename

### 4. **Generate Video**
- **Preview Text:** See credits layout before generating
- **Generate Video:** Create the final MP4 (with progress bar)
- **Save/Load Project:** Save configurations for future use

## 🎬 Credit Types Explained

| Type | Description | Example |
|------|-------------|---------|
| **Header** | Section titles in large text | "DIRECTED BY" |
| **Name** | Individual names under headers | "STEVEN SPIELBERG" | 
| **Pair** | Role and name side-by-side | "Music Composer" → "HANS ZIMMER" |
| **Spacer** | Add vertical spacing | 40 pixels of space |

## 🎯 Tips for Great Credits

- **Start with headers** like "DIRECTED BY", "PRODUCED BY"
- **Use consistent naming** - ALL CAPS for names looks professional  
- **Add spacers** between sections for clean separation
- **Choose readable colors** - White text on dark backgrounds work well
- **Test duration** - Make sure credits aren't too fast or slow
- **Save your projects** - Reuse templates for multiple videos

## 📁 Project Files

```
Credits/
├── credits_gui.py          # Main GUI application
├── Credits.py              # Original command-line version  
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── START_CREDITS_GENERATOR.bat  # Quick start script
└── movie_credits.mp4      # Generated video output
```

## 🔧 Troubleshooting

### "ImageMagick not found" Error
1. **Download ImageMagick** from the official website
2. **Install to default location** (C:\Program Files\ImageMagick-...)
3. **Restart** the Credits Generator

### "Module not found" Error  
```bash
pip install moviepy imageio-ffmpeg
```

### Video Generation is Slow
- Try **lower resolution** (720p instead of 1080p)
- **Reduce duration** for faster testing
- **Fewer credits** = faster generation

### GUI Won't Start
```bash
pip install tkinter
```

## 🛠️ Advanced Usage

### Custom Fonts
Add fonts to your system, then select them in the Settings tab.

### Batch Generation
Save different project files (.json) and load them to generate multiple credit styles.

### Integration
Use the generated MP4 files in video editors like:
- **Adobe Premiere Pro**
- **DaVinci Resolve** 
- **Final Cut Pro**
- **iMovie**

## 📄 License

This project is licensed under the MIT License - feel free to use it for personal and commercial projects!

## 🤝 Contributing

Found a bug or have a feature request? Feel free to create an issue or submit a pull request!

---

**Happy Credit Creating!** 🎬✨

Created with ❤️ using Python, MoviePy, and Tkinter