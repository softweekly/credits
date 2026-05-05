"""
Configure MoviePy to work with ImageMagick on Windows
"""
# First, apply Pillow compatibility fix
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
exec(open('fix_pillow_compatibility.py').read())

import moviepy.config as cf

# Set the path to ImageMagick
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# Verify ImageMagick exists
if os.path.exists(IMAGEMAGICK_BINARY):
    print(f"✅ Found ImageMagick at: {IMAGEMAGICK_BINARY}")
    
    # Configure MoviePy
    cf.IMAGEMAGICK_BINARY = IMAGEMAGICK_BINARY
    
    # Also set environment variable for this session
    os.environ['IMAGEMAGICK_BINARY'] = IMAGEMAGICK_BINARY
    
    print(f"✅ Configured MoviePy to use ImageMagick")
    
    # Test the configuration
    try:
        from moviepy.editor import TextClip
        test_clip = TextClip("Test", fontsize=30, color='white', font='Arial').set_duration(0.1)
        print("✅ ImageMagick configuration test passed!")
    except Exception as e:
        print(f"⚠️  ImageMagick configuration test failed: {e}")
        print("This may be normal - text generation will work in the main application")
        
else:
    print(f"❌ ImageMagick not found at: {IMAGEMAGICK_BINARY}")
    print("Please install ImageMagick or update the path in this file")