# Apply Pillow compatibility fix for newer PIL versions
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
import moviepy.config as cf

# Configure ImageMagick path for Windows
cf.IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# ==========================================
# CONFIGURATION
# ==========================================
OUTPUT_FILE = "movie_credits.mp4"
DURATION = 90  # 1.5 minutes
RESOLUTION = (1920, 1080)
FPS = 30
BG_COLOR = (0, 0, 0) # Black
FONT = 'Arial' # Or any font installed on your system

# ==========================================
# CREDIT CONTENT
# Add your names and roles here!
# ==========================================
CREDITS_LIST = [
    ("header", "DIRECTED BY"),
    ("name", "ALEXANDER SMITH"),
    ("spacer", 40),
    
    ("header", "PRODUCED BY"),
    ("name", "SARAH JENKINS"),
    ("name", "MICHAEL CHEN"),
    ("spacer", 80),

    # Role/Name pairs
    ("pair", "Production Manager", "DAVID BOWIE"),
    ("pair", "Director of Photography", "EMILY WATSON"),
    ("pair", "Art Director", "STEVEN UNIVERSE"),
    ("pair", "Lead Animator", "REBECCA SUGAR"),
    ("pair", "Music Composer", "HANS ZIMMER"),
    ("pair", "Sound Design", "ALICE COOPER"),
    ("pair", "Lead Programmer", "GABE NEWELL"),
    ("pair", "UI Designer", "MARIE KREUTZ"),
    ("pair", "QA Tester", "BILLY WEST"),
    ("pair", "QA Tester", "JOHN DI MAGGIO"),
    ("pair", "Marketing Lead", "JESSICA RABBIT"),
    ("pair", "Social Media", "TOM ANDERSON"),
    ("pair", "Voice Actor", "KEVIN CONROY"),
    ("pair", "Voice Actor", "MARK HAMILL"),
    ("pair", "Voice Actor", "TARA STRONG"),
    ("pair", "Studio Assistant", "SAM RAMI"),
    ("pair", "Script Supervisor", "GRETA GERWIG"),
    ("pair", "Costume Design", "EDITH HEAD"),
    ("pair", "Grip", "BRUCE CAMPBELL"),
    ("pair", "Best Boy", "PETER PARKER"),
    ("pair", "Craft Services", "BENNY HILL"),
    ("pair", "Stunt Coordinator", "JACKIE CHAN"),
    ("pair", "Special Thanks", "THE OPEN SOURCE COMMUNITY"),
    ("pair", "Special Thanks", "MOM AND DAD"),
    
    ("spacer", 100),
    ("header", "FILMED ON LOCATION AT"),
    ("name", "VANCOUVER, BC"),
    ("spacer", 100),
    ("header", "COPYRIGHT 2023"),
]

def create_credits():
    clips = []
    current_h = 0
    
    # Calculate starting position (start off-screen at the bottom)
    screen_w, screen_h = RESOLUTION

    for item_type, *content in CREDITS_LIST:
        if item_type == "header":
            txt = TextClip(content[0], fontsize=60, color='white', font=FONT, kerning=2)
            txt = txt.set_position(('center', current_h))
            clips.append(txt)
            current_h += 80
            
        elif item_type == "name":
            txt = TextClip(content[0], fontsize=42, color='white', font=FONT)
            txt = txt.set_position(('center', current_h))
            clips.append(txt)
            current_h += 65

        elif item_type == "pair":
            role, name = content
            # Role (Left aligned)
            left_txt = TextClip(role, fontsize=36, color='white', font=FONT)
            left_txt = left_txt.set_position((screen_w/4, current_h))
            
            # Name (Right aligned) 
            right_txt = TextClip(name, fontsize=36, color='white', font=FONT)
            right_txt = right_txt.set_position((screen_w/2 + 50, current_h))
            
            clips.append(left_txt)
            clips.append(right_txt)
            current_h += 70

        elif item_type == "spacer":
            current_h += content[0]

    # Combine all text into one big clip
    full_credits_panel = CompositeVideoClip(clips, size=(screen_w, current_h))
    
    # Calculate scroll movement
    # We want it to start with the top just below the screen and end with the bottom just above the screen
    total_travel = current_h + screen_h
    
    # Define the scroll animation
    # t is time in seconds
    def scroll(t):
        y_pos = screen_h - (t / DURATION) * total_travel
        return ('center', y_pos)

    # Apply animation
    scrolling_credits = full_credits_panel.set_position(scroll).set_duration(DURATION)
    
    # Create final video with black background
    bg = ColorClip(size=RESOLUTION, color=BG_COLOR).set_duration(DURATION)
    final_video = CompositeVideoClip([bg, scrolling_credits])
    
    # Write to file
    final_video.write_videofile(OUTPUT_FILE, fps=FPS, codec="libx264")

if __name__ == "__main__":
    create_credits()