"""
Compatibility fix for MoviePy with newer Pillow versions
This patches the PIL.Image.ANTIALIAS issue
"""
import PIL.Image

# Fix for Pillow 10+ compatibility
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
    print("✅ Applied Pillow compatibility fix (ANTIALIAS -> LANCZOS)")
else:
    print("✅ Pillow compatibility already OK")

# Also fix other deprecated attributes if they don't exist
if not hasattr(PIL.Image, 'BICUBIC'):
    PIL.Image.BICUBIC = PIL.Image.Resampling.BICUBIC

if not hasattr(PIL.Image, 'BILINEAR'):
    PIL.Image.BILINEAR = PIL.Image.Resampling.BILINEAR

if not hasattr(PIL.Image, 'NEAREST'):
    PIL.Image.NEAREST = PIL.Image.Resampling.NEAREST