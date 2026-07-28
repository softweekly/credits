#!/usr/bin/env python3
"""
Credits Generator GUI - Easy-to-use interface for creating movie credits
"""
# Apply Pillow compatibility fix for newer PIL versions
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import json
import os
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, ImageClip, VideoFileClip, AudioFileClip
import moviepy.config as cf

# Configure ImageMagick path for Windows
cf.IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

class CreditsGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Credits Generator - Professional Video Credits Made Easy")
        self.root.geometry("1000x700")
        
        # Default settings
        self.settings = {
            "duration": 90,
            "resolution": "1920x1080", 
            "fps": 30,
            "font": "Arial",
            "text_color": "#FFFFFF",
            "bg_color": "#000000",
            "bg_image": "",
            "audio_file": "",
            "use_video_audio": True,
            "output_file": "movie_credits.mp4"
        }
        
        # Credits data
        self.credits_data = [
            {"type": "header", "content": "DIRECTED BY"},
            {"type": "name", "content": "ALEXANDER SMITH"},
            {"type": "spacer", "content": "40"},
            {"type": "header", "content": "PRODUCED BY"},
            {"type": "name", "content": "SARAH JENKINS"},
            {"type": "name", "content": "MICHAEL CHEN"},
            {"type": "spacer", "content": "80"},
            {"type": "pair", "role": "Production Manager", "name": "DAVID BOWIE"},
            {"type": "pair", "role": "Director of Photography", "name": "EMILY WATSON"},
            {"type": "pair", "role": "Art Director", "name": "STEVEN UNIVERSE"},
            {"type": "pair", "role": "Lead Animator", "name": "REBECCA SUGAR"},
            {"type": "pair", "role": "Music Composer", "name": "HANS ZIMMER"},
            {"type": "pair", "role": "Sound Design", "name": "ALICE COOPER"},
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Credits Editor
        self.credits_frame = ttk.Frame(notebook)
        notebook.add(self.credits_frame, text="Credits Editor")
        self.setup_credits_tab()
        
        # Tab 2: Appearance
        self.appearance_frame = ttk.Frame(notebook)
        notebook.add(self.appearance_frame, text="Appearance")
        self.setup_appearance_tab()
        
        # Tab 3: Settings
        self.settings_frame = ttk.Frame(notebook)
        notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
        # Bottom frame for actions
        self.action_frame = ttk.Frame(self.root)
        self.action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(self.action_frame, text="Preview Text", command=self.preview_credits).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.action_frame, text="Generate Video", command=self.generate_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.action_frame, text="Save Project", command=self.save_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.action_frame, text="Load Project", command=self.load_project).pack(side=tk.LEFT, padx=5)
        
    def setup_credits_tab(self):
        # Left panel - Credits list
        left_frame = ttk.Frame(self.credits_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Credits List", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        # Credits treeview
        columns = ("Type", "Role/Content", "Name")
        self.credits_tree = ttk.Treeview(left_frame, columns=columns, show="tree headings", height=15)
        
        self.credits_tree.heading("#0", text="#")
        self.credits_tree.heading("Type", text="Type")  
        self.credits_tree.heading("Role/Content", text="Role/Content")
        self.credits_tree.heading("Name", text="Name")
        
        self.credits_tree.column("#0", width=30)
        self.credits_tree.column("Type", width=80)
        self.credits_tree.column("Role/Content", width=200)
        self.credits_tree.column("Name", width=200)
        
        self.credits_tree.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Edit controls
        right_frame = ttk.Frame(self.credits_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Edit Entry", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Entry type
        ttk.Label(right_frame, text="Type:").pack(anchor=tk.W)
        self.entry_type = ttk.Combobox(right_frame, values=["header", "name", "pair", "spacer"], width=25)
        self.entry_type.pack(pady=(0, 10))
        self.entry_type.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Content/Role field  
        self.content_label = ttk.Label(right_frame, text="Content:")
        self.content_label.pack(anchor=tk.W)
        self.content_entry = ttk.Entry(right_frame, width=25)
        self.content_entry.pack(pady=(0, 10))
        
        # Name field (for pairs)
        self.name_label = ttk.Label(right_frame, text="Name:")
        self.name_entry = ttk.Entry(right_frame, width=25)
        
        # Buttons
        ttk.Button(right_frame, text="Add Entry", command=self.add_entry).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Update Selected", command=self.update_entry).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Delete Selected", command=self.delete_entry).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Move Up", command=self.move_up).pack(fill=tk.X, pady=2)
        ttk.Button(right_frame, text="Move Down", command=self.move_down).pack(fill=tk.X, pady=2)
        
        # Populate initial data
        self.refresh_credits_list()
        self.credits_tree.bind("<<TreeviewSelect>>", self.on_select_credit)
        
    def setup_appearance_tab(self):
        # Colors section
        colors_frame = ttk.LabelFrame(self.appearance_frame, text="Colors")
        colors_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Text color
        text_color_frame = ttk.Frame(colors_frame)
        text_color_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(text_color_frame, text="Text Color:").pack(side=tk.LEFT)
        self.text_color_btn = tk.Button(text_color_frame, text="      ", bg=self.settings["text_color"], 
                                       command=lambda: self.choose_color("text_color"))
        self.text_color_btn.pack(side=tk.LEFT, padx=10)
        self.text_color_label = ttk.Label(text_color_frame, text=self.settings["text_color"])
        self.text_color_label.pack(side=tk.LEFT, padx=5)
        
        # Background color
        bg_color_frame = ttk.Frame(colors_frame)
        bg_color_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(bg_color_frame, text="Background Color:").pack(side=tk.LEFT)
        self.bg_color_btn = tk.Button(bg_color_frame, text="      ", bg=self.settings["bg_color"],
                                     command=lambda: self.choose_color("bg_color"))
        self.bg_color_btn.pack(side=tk.LEFT, padx=10)
        self.bg_color_label = ttk.Label(bg_color_frame, text=self.settings["bg_color"])
        self.bg_color_label.pack(side=tk.LEFT, padx=5)
        
        # Background media section
        bg_media_frame = ttk.LabelFrame(self.appearance_frame, text="Background Media")
        bg_media_frame.pack(fill=tk.X, padx=10, pady=10)
        
        bg_select_frame = ttk.Frame(bg_media_frame)
        bg_select_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(bg_select_frame, text="Select Image/Video", command=self.choose_bg_media).pack(side=tk.LEFT)
        ttk.Button(bg_select_frame, text="Clear Background", command=self.clear_bg_media).pack(side=tk.LEFT, padx=5)
        
        self.bg_media_label = ttk.Label(bg_media_frame, text="No background selected")
        self.bg_media_label.pack(padx=10, pady=5)
        
        self.bg_media_info = ttk.Label(bg_media_frame, text="", font=("Arial", 9), foreground="gray")
        self.bg_media_info.pack(padx=10, pady=2)
        
        # Audio section
        audio_frame = ttk.LabelFrame(self.appearance_frame, text="Audio")
        audio_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Audio source info
        self.audio_source_label = ttk.Label(audio_frame, text="Audio: Will use background silence", font=("Arial", 10, "bold"))
        self.audio_source_label.pack(padx=10, pady=5)
        
        # Audio file selection
        audio_select_frame = ttk.Frame(audio_frame)
        audio_select_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(audio_select_frame, text="Add Audio File", command=self.choose_audio_file).pack(side=tk.LEFT)
        ttk.Button(audio_select_frame, text="Clear Audio", command=self.clear_audio_file).pack(side=tk.LEFT, padx=5)
        
        self.audio_file_label = ttk.Label(audio_frame, text="No audio file selected")
        self.audio_file_label.pack(padx=10, pady=2)
        
        # Audio options
        self.use_video_audio_var = tk.BooleanVar(value=True)
        self.video_audio_check = ttk.Checkbutton(audio_frame, text="Use video audio (if background is video)", 
                                                variable=self.use_video_audio_var, command=self.update_audio_status)
        self.video_audio_check.pack(padx=10, pady=5)
        
    def setup_settings_tab(self):
        # Video settings
        video_frame = ttk.LabelFrame(self.settings_frame, text="Video Settings")
        video_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Duration
        dur_frame = ttk.Frame(video_frame)
        dur_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(dur_frame, text="Duration (seconds):").pack(side=tk.LEFT)
        self.duration_var = tk.StringVar(value=str(self.settings["duration"]))
        ttk.Entry(dur_frame, textvariable=self.duration_var, width=10).pack(side=tk.LEFT, padx=10)
        
        # Resolution
        res_frame = ttk.Frame(video_frame)
        res_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(res_frame, text="Resolution:").pack(side=tk.LEFT)
        self.resolution_var = tk.StringVar(value=self.settings["resolution"])
        resolution_combo = ttk.Combobox(res_frame, textvariable=self.resolution_var, 
                                       values=["1920x1080", "1280x720", "3840x2160", "1024x576"])
        resolution_combo.pack(side=tk.LEFT, padx=10)
        
        # FPS
        fps_frame = ttk.Frame(video_frame)
        fps_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(fps_frame, text="FPS:").pack(side=tk.LEFT)
        self.fps_var = tk.StringVar(value=str(self.settings["fps"]))
        ttk.Entry(fps_frame, textvariable=self.fps_var, width=10).pack(side=tk.LEFT, padx=10)
        
        # Font
        font_frame = ttk.Frame(video_frame)
        font_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(font_frame, text="Font:").pack(side=tk.LEFT)
        self.font_var = tk.StringVar(value=self.settings["font"])
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_var,
                                 values=["Arial", "Times New Roman", "Helvetica", "Courier New"])
        font_combo.pack(side=tk.LEFT, padx=10)
        
        # Output file
        output_frame = ttk.Frame(video_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value=self.settings["output_file"])
        ttk.Entry(output_frame, textvariable=self.output_var, width=30).pack(side=tk.LEFT, padx=10)
        
    def on_type_change(self, event=None):
        entry_type = self.entry_type.get()
        if entry_type == "pair":
            self.name_label.pack(anchor=tk.W)
            self.name_entry.pack(pady=(0, 10))
            self.content_label.config(text="Role:")
        else:
            self.name_label.pack_forget()
            self.name_entry.pack_forget()
            if entry_type == "spacer":
                self.content_label.config(text="Spacing (px):")
            else:
                self.content_label.config(text="Content:")
    
    def refresh_credits_list(self):
        # Clear existing items
        for item in self.credits_tree.get_children():
            self.credits_tree.delete(item)
            
        # Add credits data
        for i, credit in enumerate(self.credits_data):
            if credit["type"] == "pair":
                self.credits_tree.insert("", "end", text=str(i+1), 
                                       values=(credit["type"], credit["role"], credit["name"]))
            else:
                content = credit["content"]
                self.credits_tree.insert("", "end", text=str(i+1),
                                       values=(credit["type"], content, ""))
    
    def on_select_credit(self, event=None):
        selection = self.credits_tree.selection()
        if selection:
            item = selection[0]
            index = int(self.credits_tree.item(item, "text")) - 1
            if 0 <= index < len(self.credits_data):
                credit = self.credits_data[index]
                self.entry_type.set(credit["type"])
                self.on_type_change()
                
                if credit["type"] == "pair":
                    self.content_entry.delete(0, tk.END)
                    self.content_entry.insert(0, credit["role"])
                    self.name_entry.delete(0, tk.END)
                    self.name_entry.insert(0, credit["name"])
                else:
                    self.content_entry.delete(0, tk.END) 
                    self.content_entry.insert(0, credit["content"])
    
    def add_entry(self):
        entry_type = self.entry_type.get()
        content = self.content_entry.get()
        
        if not entry_type or not content:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        new_entry = {"type": entry_type, "content": content}
        
        if entry_type == "pair":
            name = self.name_entry.get()
            if not name:
                messagebox.showerror("Error", "Please enter a name for the pair entry")
                return
            new_entry = {"type": entry_type, "role": content, "name": name}
            
        self.credits_data.append(new_entry)
        self.refresh_credits_list()
        
        # Clear fields
        self.content_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
    
    def update_entry(self):
        selection = self.credits_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an entry to update")
            return
            
        item = selection[0]
        index = int(self.credits_tree.item(item, "text")) - 1
        
        entry_type = self.entry_type.get()
        content = self.content_entry.get()
        
        if not entry_type or not content:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
            
        updated_entry = {"type": entry_type, "content": content}
        
        if entry_type == "pair":
            name = self.name_entry.get()
            if not name:
                messagebox.showerror("Error", "Please enter a name for the pair entry")
                return
            updated_entry = {"type": entry_type, "role": content, "name": name}
            
        self.credits_data[index] = updated_entry
        self.refresh_credits_list()
    
    def delete_entry(self):
        selection = self.credits_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select an entry to delete")
            return
            
        item = selection[0]
        index = int(self.credits_tree.item(item, "text")) - 1
        
        del self.credits_data[index]
        self.refresh_credits_list()
    
    def move_up(self):
        selection = self.credits_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        index = int(self.credits_tree.item(item, "text")) - 1
        
        if index > 0:
            self.credits_data[index], self.credits_data[index-1] = self.credits_data[index-1], self.credits_data[index]
            self.refresh_credits_list()
    
    def move_down(self):
        selection = self.credits_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        index = int(self.credits_tree.item(item, "text")) - 1
        
        if index < len(self.credits_data) - 1:
            self.credits_data[index], self.credits_data[index+1] = self.credits_data[index+1], self.credits_data[index]
            self.refresh_credits_list()
    
    def choose_color(self, color_type):
        current_color = self.settings[color_type]
        color = colorchooser.askcolor(color=current_color)[1]
        if color:
            self.settings[color_type] = color
            if color_type == "text_color":
                self.text_color_btn.config(bg=color)
                self.text_color_label.config(text=color)
            else:
                self.bg_color_btn.config(bg=color)
                self.bg_color_label.config(text=color)
    
    def choose_bg_media(self):
        filename = filedialog.askopenfilename(
            title="Select Background Image or Video",
            filetypes=[
                ("All supported", "*.png *.jpg *.jpeg *.gif *.bmp *.mp4 *.mov *.avi *.mkv *.wmv"),
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Video files", "*.mp4 *.mov *.avi *.mkv *.wmv")
            ]
        )
        if filename:
            self.settings["bg_image"] = filename
            file_name = os.path.basename(filename)
            self.bg_media_label.config(text=file_name)
            
            # Check if it's a video file
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']
            is_video = any(filename.lower().endswith(ext) for ext in video_extensions)
            
            if is_video:
                self.bg_media_info.config(text="Video file - audio will be used automatically")
            else:
                self.bg_media_info.config(text="Image file - add separate audio if needed")
            
            self.update_audio_status()
    
    def clear_bg_media(self):
        self.settings["bg_image"] = ""
        self.bg_media_label.config(text="No background selected")
        self.bg_media_info.config(text="")
        self.update_audio_status()
    
    def choose_audio_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.aac *.ogg *.flac *.m4a"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.settings["audio_file"] = filename
            self.audio_file_label.config(text=os.path.basename(filename))
            self.update_audio_status()
    
    def clear_audio_file(self):
        self.settings["audio_file"] = ""
        self.audio_file_label.config(text="No audio file selected")
        self.update_audio_status()
    
    def update_audio_status(self):
        bg_file = self.settings["bg_image"]
        audio_file = self.settings["audio_file"]
        use_video_audio = self.use_video_audio_var.get()
        
        # Check if background is video
        is_bg_video = False
        if bg_file:
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']
            is_bg_video = any(bg_file.lower().endswith(ext) for ext in video_extensions)
        
        # Determine audio source
        if audio_file:
            self.audio_source_label.config(text="Audio: Custom audio file", foreground="blue")
        elif is_bg_video and use_video_audio:
            self.audio_source_label.config(text="Audio: From background video", foreground="green")
        elif is_bg_video and not use_video_audio:
            self.audio_source_label.config(text="Audio: Silent (video audio disabled)", foreground="orange")
        else:
            self.audio_source_label.config(text="Audio: Silent (no audio source)", foreground="gray")
        
        # Update settings
        self.settings["use_video_audio"] = use_video_audio
    
    def preview_credits(self):
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Credits Preview")
        preview_window.geometry("600x400")
        
        text_area = tk.Text(preview_window, wrap=tk.WORD, font=("Courier", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generate preview text
        preview_text = "CREDITS PREVIEW\n" + "="*50 + "\n\n"
        
        for credit in self.credits_data:
            if credit["type"] == "header":
                preview_text += f"    {credit['content']}\n"
                preview_text += f"    {'-' * len(credit['content'])}\n"
            elif credit["type"] == "name":
                preview_text += f"        {credit['content']}\n"
            elif credit["type"] == "pair":
                preview_text += f"    {credit['role']:<25} {credit['name']}\n"
            elif credit["type"] == "spacer":
                preview_text += "\n"
                
        text_area.insert(tk.END, preview_text)
        text_area.config(state=tk.DISABLED)
    
    def update_settings_from_ui(self):
        self.settings["duration"] = int(self.duration_var.get())
        self.settings["resolution"] = self.resolution_var.get()
        self.settings["fps"] = int(self.fps_var.get())
        self.settings["font"] = self.font_var.get()
        self.settings["output_file"] = self.output_var.get()
    
    def generate_video(self):
        try:
            self.update_settings_from_ui()
            
            # Show progress dialog
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Generating Video...")
            progress_window.geometry("400x150")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            ttk.Label(progress_window, text="Generating video, please wait...", 
                     font=("Arial", 12)).pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=20, fill=tk.X)
            progress_bar.start()
            
            status_label = ttk.Label(progress_window, text="Processing...")
            status_label.pack(pady=10)
            
            # Generate video in background
            self.root.after(100, lambda: self._generate_video_background(progress_window, progress_bar))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
    
    def _generate_video_background(self, progress_window, progress_bar):
        try:
            # Convert credits data to format expected by generation function
            credits_list = []
            for credit in self.credits_data:
                if credit["type"] == "pair":
                    credits_list.append(("pair", credit["role"], credit["name"]))
                elif credit["type"] == "spacer":
                    credits_list.append(("spacer", int(credit["content"])))
                else:
                    credits_list.append((credit["type"], credit["content"]))
            
            # Generate video
            self._create_video(credits_list)
            
            # Close progress window
            progress_bar.stop()
            progress_window.destroy()
            
            messagebox.showinfo("Success", f"Video generated successfully as {self.settings['output_file']}")
            
        except Exception as e:
            progress_bar.stop()
            progress_window.destroy()
            messagebox.showerror("Error", f"Failed to generate video: {str(e)}")
    
    def _create_video(self, credits_list):
        clips = []
        current_h = 0
        
        # Parse resolution
        res_parts = self.settings["resolution"].split("x")
        screen_w, screen_h = int(res_parts[0]), int(res_parts[1])
        
        # Use hex colors directly (TextClip expects hex strings or color names)
        text_color = self.settings["text_color"]  # Keep as hex string
        bg_color = tuple(int(self.settings["bg_color"][i:i+2], 16) for i in (1, 3, 5))  # RGB for ColorClip
        
        for item in credits_list:
            item_type = item[0]
            
            if item_type == "header":
                txt = TextClip(item[1], fontsize=60, color=text_color, font=self.settings["font"], kerning=2)
                txt = txt.set_position(('center', current_h))
                clips.append(txt)
                current_h += 80
                
            elif item_type == "name":
                txt = TextClip(item[1], fontsize=42, color=text_color, font=self.settings["font"])
                txt = txt.set_position(('center', current_h))
                clips.append(txt)
                current_h += 65
                
            elif item_type == "pair":
                role, name = item[1], item[2]
                # Role
                left_txt = TextClip(role, fontsize=36, color=text_color, font=self.settings["font"])
                left_txt = left_txt.set_position((screen_w/4, current_h))
                
                # Name
                right_txt = TextClip(name, fontsize=36, color=text_color, font=self.settings["font"])
                right_txt = right_txt.set_position((screen_w/2 + 50, current_h))
                
                clips.append(left_txt)
                clips.append(right_txt)
                current_h += 70
                
            elif item_type == "spacer":
                current_h += item[1]
        
        # Create composite of all text
        full_credits_panel = CompositeVideoClip(clips, size=(screen_w, current_h))
        
        # Pre-render the credits panel to a single image to avoid re-rendering
        # each TextClip on every frame (this was causing 60x slowdown).
        # We also extract the alpha mask so the text background stays transparent.
        panel_frame = full_credits_panel.get_frame(0)
        mask_frame = full_credits_panel.mask.get_frame(0)
        full_credits_panel = ImageClip(panel_frame).set_mask(ImageClip(mask_frame, ismask=True))
        
        # Calculate scroll animation
        total_travel = current_h + screen_h
        
        def scroll(t):
            y_pos = screen_h - (t / self.settings["duration"]) * total_travel
            return ('center', y_pos)
        
        scrolling_credits = full_credits_panel.set_position(scroll).set_duration(self.settings["duration"])
        
        # Create background and handle audio
        audio_clip = None
        bg_file = self.settings["bg_image"]
        
        if bg_file and os.path.exists(bg_file):
            # Check if background is video or image
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']
            is_video = any(bg_file.lower().endswith(ext) for ext in video_extensions)
            
            if is_video:
                # Background is video - trim to video duration
                raw_bg = VideoFileClip(bg_file)
                video_duration = self.settings["duration"]
                trim_end = min(raw_bg.duration, video_duration)
                bg_video = raw_bg.subclip(0, trim_end).resize((screen_w, screen_h)).set_duration(trim_end)
                bg = bg_video.without_audio()  # We'll handle audio separately
                
                # Get audio from video if enabled
                if self.settings["use_video_audio"] and bg_video.audio is not None:
                    raw_audio = bg_video.audio
                    trim_end = min(raw_audio.duration, self.settings["duration"])
                    audio_clip = raw_audio.subclip(0, trim_end)
            else:
                # Background is image
                bg = ImageClip(bg_file).resize((screen_w, screen_h)).set_duration(self.settings["duration"])
        else:
            # No background file - use solid color
            bg = ColorClip(size=(screen_w, screen_h), color=bg_color).set_duration(self.settings["duration"])
        
        # Override with custom audio file if provided
        if self.settings["audio_file"] and os.path.exists(self.settings["audio_file"]):
            raw_audio = AudioFileClip(self.settings["audio_file"])
            video_duration = self.settings["duration"]
            trim_end = min(raw_audio.duration, video_duration)
            audio_clip = raw_audio.subclip(0, trim_end)
        
        # Combine video
        final_video = CompositeVideoClip([bg, scrolling_credits])
        
        # Add audio if available
        if audio_clip is not None:
            final_video = final_video.set_audio(audio_clip)
        
        # Write to file
        final_video.write_videofile(self.settings["output_file"], fps=self.settings["fps"], codec="libx264")
    
    def save_project(self):
        filename = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            project_data = {
                "settings": self.settings,
                "credits_data": self.credits_data
            }
            with open(filename, 'w') as f:
                json.dump(project_data, f, indent=2)
            messagebox.showinfo("Success", "Project saved successfully!")
    
    def load_project(self):
        filename = filedialog.askopenfilename(
            title="Load Project",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    project_data = json.load(f)
                    
                self.settings = project_data.get("settings", self.settings)
                self.credits_data = project_data.get("credits_data", self.credits_data)
                
                # Update UI
                self.refresh_credits_list()
                self.duration_var.set(str(self.settings["duration"]))
                self.resolution_var.set(self.settings["resolution"])
                self.fps_var.set(str(self.settings["fps"]))
                self.font_var.set(self.settings["font"])
                self.output_var.set(self.settings["output_file"])
                
                # Update color buttons
                self.text_color_btn.config(bg=self.settings["text_color"])
                self.text_color_label.config(text=self.settings["text_color"])
                self.bg_color_btn.config(bg=self.settings["bg_color"])
                self.bg_color_label.config(text=self.settings["bg_color"])
                
                # Update background media
                if self.settings["bg_image"]:
                    self.bg_media_label.config(text=os.path.basename(self.settings["bg_image"]))
                    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']
                    is_video = any(self.settings["bg_image"].lower().endswith(ext) for ext in video_extensions)
                    if is_video:
                        self.bg_media_info.config(text="Video file - audio will be used automatically")
                    else:
                        self.bg_media_info.config(text="Image file - add separate audio if needed")
                else:
                    self.bg_media_label.config(text="No background selected")
                    self.bg_media_info.config(text="")
                
                # Update audio settings
                if self.settings.get("audio_file"):
                    self.audio_file_label.config(text=os.path.basename(self.settings["audio_file"]))
                else:
                    self.audio_file_label.config(text="No audio file selected")
                
                if "use_video_audio" in self.settings:
                    self.use_video_audio_var.set(self.settings["use_video_audio"])
                
                self.update_audio_status()
                
                messagebox.showinfo("Success", "Project loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project: {str(e)}")

def main():
    root = tk.Tk()
    app = CreditsGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()