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

## 🚀 Quick Start (Windows)

### Option 1: One-Click Setup
1. **Download** this folder to your computer
2. **Double-click** `START_CREDITS_GENERATOR.bat` 
3. **Done!** The installer will set everything up automatically

### Option 2: Manual Installation

#### Prerequisites
- **Windows 10/11**
- **Python 3.7 or higher** ([Download Python](https://www.python.org/downloads/))
- **ImageMagick** ([Download ImageMagick](https://imagemagick.org/script/download.php#windows))

#### Step-by-Step Installation

1. **Install Python** (if not already installed)
   ```
   Download from: https://www.python.org/downloads/
   ✅ Check "Add Python to PATH" during installation
   ```

2. **Install ImageMagick**
   ```
   Download from: https://imagemagick.org/script/download.php#windows
   Choose: ImageMagick-7.x.x-Q16-HDRI-x64-dll.exe
   ✅ Install to default location: C:\Program Files\ImageMagick-...
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Credits Generator**
   ```bash
   python credits_gui.py
   ```

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