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
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, ImageClip
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
        
        # Background image section
        bg_image_frame = ttk.LabelFrame(self.appearance_frame, text="Background Image")
        bg_image_frame.pack(fill=tk.X, padx=10, pady=10)
        
        bg_select_frame = ttk.Frame(bg_image_frame)
        bg_select_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(bg_select_frame, text="Select Image", command=self.choose_bg_image).pack(side=tk.LEFT)
        ttk.Button(bg_select_frame, text="Clear Image", command=self.clear_bg_image).pack(side=tk.LEFT, padx=5)
        
        self.bg_image_label = ttk.Label(bg_image_frame, text="No image selected")
        self.bg_image_label.pack(padx=10, pady=5)
        
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
    
    def choose_bg_image(self):
        filename = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if filename:
            self.settings["bg_image"] = filename
            self.bg_image_label.config(text=os.path.basename(filename))
    
    def clear_bg_image(self):
        self.settings["bg_image"] = ""
        self.bg_image_label.config(text="No image selected")
    
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
        
        # Calculate scroll animation
        total_travel = current_h + screen_h
        
        def scroll(t):
            y_pos = screen_h - (t / self.settings["duration"]) * total_travel
            return ('center', y_pos)
        
        scrolling_credits = full_credits_panel.set_position(scroll).set_duration(self.settings["duration"])
        
        # Create background
        if self.settings["bg_image"] and os.path.exists(self.settings["bg_image"]):
            bg = ImageClip(self.settings["bg_image"]).resize((screen_w, screen_h)).set_duration(self.settings["duration"])
        else:
            bg = ColorClip(size=(screen_w, screen_h), color=bg_color).set_duration(self.settings["duration"])
        
        # Combine and write
        final_video = CompositeVideoClip([bg, scrolling_credits])
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
                
                if self.settings["bg_image"]:
                    self.bg_image_label.config(text=os.path.basename(self.settings["bg_image"]))
                else:
                    self.bg_image_label.config(text="No image selected")
                
                messagebox.showinfo("Success", "Project loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project: {str(e)}")

def main():
    root = tk.Tk()
    app = CreditsGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()