#!/usr/bin/env python3
"""
Preview version of the credits script that shows the text output
"""

# ==========================================
# CREDIT CONTENT
# (Same as the original script)
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

def preview_credits():
    """Print a text preview of what the credits will look like"""
    print("=" * 60)
    print("CREDITS PREVIEW")
    print("=" * 60)
    print()
    
    for item_type, *content in CREDITS_LIST:
        if item_type == "header":
            print()
            print(f"    {content[0]}")
            print("    " + "─" * len(content[0]))
            
        elif item_type == "name":
            print(f"        {content[0]}")

        elif item_type == "pair":
            role, name = content
            print(f"    {role:<25} {name}")

        elif item_type == "spacer":
            print()  # Add extra spacing

    print()
    print("=" * 60)
    print(f"Total credits entries: {len([x for x in CREDITS_LIST if x[0] in ['header', 'name', 'pair']])}")
    print("=" * 60)

if __name__ == "__main__":
    preview_credits()