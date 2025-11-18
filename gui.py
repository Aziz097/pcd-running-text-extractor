import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkFont

class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLN UPT Tanjung Karang - Video Processing Control")
        self.root.geometry("1200x800")
        
        # Color scheme
        self.bg_color = "#f5f5f5"
        self.primary_blue = "#2962ff"
        self.card_bg = "#ffffff"
        self.text_dark = "#333333"
        self.text_light = "#666666"
        self.success_green = "#4caf50"
        
        self.root.configure(bg=self.bg_color)
        
        # Create main container
        self.create_header()
        self.create_main_content()
        
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.primary_blue, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo and title container
        title_container = tk.Frame(header_frame, bg=self.primary_blue)
        title_container.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Lightning bolt icon (simulated with text)
        icon_label = tk.Label(title_container, text="⚡", 
                             font=("Poppins", 24, "bold"),
                             fg="white", bg=self.primary_blue)
        icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Title text
        title_frame = tk.Frame(title_container, bg=self.primary_blue)
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, text="PLN UPT Tanjung Karang",
                               font=("Poppins", 14, "bold"),
                               fg="white", bg=self.primary_blue)
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(title_frame, text="Video Extraction Tool",
                                 font=("Poppins", 10),
                                 fg="#e0e0e0", bg=self.primary_blue)
        subtitle_label.pack(anchor="w")
        
        # Right side - Officer info
        officer_frame = tk.Frame(header_frame, bg=self.primary_blue)
        officer_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        officer_label = tk.Label(officer_frame, text="Officer Komunikasi",
                                font=("Poppins", 12),
                                fg="white", bg=self.primary_blue)
        officer_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # User avatar circle
        avatar_frame = tk.Frame(officer_frame, bg="white", width=35, height=35)
        avatar_frame.pack(side=tk.LEFT)
        avatar_frame.pack_propagate(False)
        
        avatar_label = tk.Label(avatar_frame, text="👤", font=("Poppins", 16))
        avatar_label.pack(expand=True)
        
    def create_main_content(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title section
        title_label = tk.Label(main_container, 
                              text="📹 Video Processing Control",
                              font=("Poppins", 20, "bold"),
                              fg=self.text_dark, bg=self.bg_color)
        title_label.pack(anchor="w", pady=(0, 0))
        
        subtitle_label = tk.Label(main_container,
                                 text="Extract video clips from TV broadcast recordings",
                                 font=("Poppins", 12),
                                 fg=self.text_light, bg=self.bg_color)
        subtitle_label.pack(anchor="w", pady=(0, 0))
        
        # Create two columns
        columns_frame = tk.Frame(main_container, bg=self.bg_color)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column
        left_column = tk.Frame(columns_frame, bg=self.bg_color)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Right column
        right_column = tk.Frame(columns_frame, bg=self.bg_color)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Video Processing Control Card (Left)
        self.create_video_control_card(left_column)
        
        # Status and Results Cards (Right)
        self.create_status_card(right_column)
        self.create_results_card(right_column)
        self.create_quick_actions_card(right_column)
        
    def create_video_control_card(self, parent):
        # Card frame
        card = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=1)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Add shadow effect with border
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Card content with padding
        content = tk.Frame(card, bg=self.card_bg)
        content.pack(padx=30, pady=25, fill=tk.BOTH, expand=True)
        
        # Select Video File Section
        file_label = tk.Label(content, text="📁 Select Video File",
                             font=("Poppins", 12, "bold"),
                             fg=self.text_dark, bg=self.card_bg)
        file_label.pack(anchor="w", pady=(0, 10))
        
        # File selection area (dashed border)
        file_frame = tk.Frame(content, bg=self.card_bg, relief=tk.RIDGE, bd=2)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_area = tk.Frame(file_frame, bg="#fafafa", height=100)
        file_area.pack(fill=tk.BOTH, padx=2, pady=2)
        file_area.pack_propagate(False)
        
        file_text = tk.Label(file_area, text="Click to select video file",
                            font=("Poppins", 11),
                            fg=self.text_light, bg="#fafafa")
        file_text.pack(expand=True)
        
        formats_text = tk.Label(file_area, text="Supported formats: MP4, AVI, MOV, MKV",
                               font=("Poppins", 9),
                               fg="#999999", bg="#fafafa")
        formats_text.pack(pady=(0, 10))
        
        # Start Phrase
        start_label = tk.Label(content, text="▶️ Start Phrase",
                              font=("Poppins", 12, "bold"),
                              fg=self.success_green, bg=self.card_bg)
        start_label.pack(anchor="w", pady=(10, 5))
        
        self.start_entry = tk.Entry(content, font=("Poppins", 11), relief=tk.SOLID, bd=1)
        self.start_entry.pack(fill=tk.X, pady=(0, 5))
        self.start_entry.insert(0, "PLN UPT Tanjung Karang")
        
        start_hint = tk.Label(content, text="Phrase that marks the beginning of clips",
                             font=("Poppins", 9),
                             fg="#999999", bg=self.card_bg)
        start_hint.pack(anchor="w", pady=(0, 15))
        
        # End Phrase
        end_label = tk.Label(content, text="⏹️ End Phrase",
                            font=("Poppins", 12, "bold"),
                            fg="#f44336", bg=self.card_bg)
        end_label.pack(anchor="w", pady=(10, 5))
        
        self.end_entry = tk.Entry(content, font=("Poppins", 11), relief=tk.SOLID, bd=1)
        self.end_entry.pack(fill=tk.X, pady=(0, 5))
        self.end_entry.insert(0, "Sekian")
        
        end_hint = tk.Label(content, text="Phrase that marks the end of clips",
                           font=("Poppins", 9),
                           fg="#999999", bg=self.card_bg)
        end_hint.pack(anchor="w", pady=(0, 15))
        
        # Maximum Clip Duration
        duration_label = tk.Label(content, text="⏱️ Maximum Clip Duration (seconds)",
                                 font=("Poppins", 12, "bold"),
                                 fg="#ff9800", bg=self.card_bg)
        duration_label.pack(anchor="w", pady=(10, 10))
        
        # Slider frame
        slider_frame = tk.Frame(content, bg=self.card_bg)
        slider_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.duration_slider = ttk.Scale(slider_frame, from_=10, to=300,
                                        orient=tk.HORIZONTAL, value=60)
        self.duration_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.duration_value = tk.Label(slider_frame, text="60\nsec",
                                      font=("Poppins", 11, "bold"),
                                      fg=self.text_dark, bg=self.card_bg)
        self.duration_value.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(content, bg=self.card_bg)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Process button
        process_btn = tk.Button(button_frame,
                               text="▶ Jalankan Ekstraksi",
                               font=("Poppins", 12, "bold"),
                               bg=self.primary_blue, fg="white",
                               relief=tk.FLAT, padx=30, pady=12,
                               cursor="hand2")
        process_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Reset button
        reset_btn = tk.Button(button_frame,
                             text="↻ Reset",
                             font=("Poppins", 12),
                             bg="#555555", fg="white",
                             relief=tk.FLAT, padx=20, pady=12,
                             cursor="hand2")
        reset_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_status_card(self, parent):
        # Status card
        status_card = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=1)
        status_card.pack(fill=tk.X, pady=(0, 20))
        status_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        status_content = tk.Frame(status_card, bg=self.card_bg)
        status_content.pack(padx=20, pady=20, fill=tk.X)
        
        status_title = tk.Label(status_content, text="✅ Process Status",
                               font=("Poppins", 12, "bold"),
                               fg=self.text_dark, bg=self.card_bg)
        status_title.pack(anchor="w", pady=(0, 15))
        
        # Status icon and text
        status_frame = tk.Frame(status_content, bg=self.card_bg)
        status_frame.pack()
        
        # Green checkmark circle
        check_frame = tk.Frame(status_frame, bg="#e8f5e9", width=60, height=60)
        check_frame.pack(pady=(0, 10))
        check_frame.pack_propagate(False)
        
        check_label = tk.Label(check_frame, text="✓",
                              font=("Poppins", 28, "bold"),
                              fg=self.success_green, bg="#e8f5e9")
        check_label.pack(expand=True)
        
        status_text = tk.Label(status_frame, text="Siap",
                              font=("Poppins", 14, "bold"),
                              fg=self.text_dark, bg=self.card_bg)
        status_text.pack()
        
        status_desc = tk.Label(status_frame, text="Ready to process",
                              font=("Poppins", 10),
                              fg=self.text_light, bg=self.card_bg)
        status_desc.pack()
        
    def create_results_card(self, parent):
        # Results card
        results_card = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=1)
        results_card.pack(fill=tk.X, pady=(0, 20))
        results_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        results_content = tk.Frame(results_card, bg=self.card_bg)
        results_content.pack(padx=20, pady=20, fill=tk.X)
        
        # Results header with Open Folder button
        results_header = tk.Frame(results_content, bg=self.card_bg)
        results_header.pack(fill=tk.X, pady=(0, 15))
        
        results_title = tk.Label(results_header, text="Results",
                                font=("Poppins", 12, "bold"),
                                fg=self.text_dark, bg=self.card_bg)
        results_title.pack(side=tk.LEFT)
        
        folder_btn = tk.Button(results_header, text="📁 Open Folder",
                              font=("Poppins", 10),
                              bg="#e8f5e9", fg=self.success_green,
                              relief=tk.FLAT, padx=10, pady=3,
                              cursor="hand2")
        folder_btn.pack(side=tk.RIGHT)
        
        # Results area
        results_area = tk.Frame(results_content, bg="#fafafa", height=80)
        results_area.pack(fill=tk.X)
        results_area.pack_propagate(False)
        
        # No results icon and text
        no_results = tk.Label(results_area, text="📂",
                             font=("Poppins", 24),
                             fg="#cccccc", bg="#fafafa")
        no_results.pack(pady=(10, 5))
        
        no_results_text = tk.Label(results_area, text="No clips extracted yet",
                                  font=("Poppins", 11, "bold"),
                                  fg=self.text_light, bg="#fafafa")
        no_results_text.pack()
        
        no_results_desc = tk.Label(results_area, text="Results will appear here",
                                  font=("Poppins", 9),
                                  fg="#999999", bg="#fafafa")
        no_results_desc.pack()
        
    def create_quick_actions_card(self, parent):
        # Quick Actions card
        actions_card = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=1)
        actions_card.pack(fill=tk.X)
        actions_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        actions_content = tk.Frame(actions_card, bg=self.card_bg)
        actions_content.pack(padx=20, pady=20, fill=tk.X)
        
        actions_title = tk.Label(actions_content, text="Quick Actions",
                                font=("Poppins", 12, "bold"),
                                fg=self.text_dark, bg=self.card_bg)
        actions_title.pack(anchor="w", pady=(0, 15))
        
        # Action items
        actions = [
            ("🕐", "View Processing History", "Last processed: Today", "#9c27b0"),
            ("⚙️", "Advanced Settings", "Configure detection parameters", "#f44336"),
            ("❓", "Help & Documentation", "User guide and tutorials", "#ff9800"),
            ("📊", "Export Report", "Generate processing summary", "#4caf50")
        ]
        
        for icon, title, desc, color in actions:
            action_frame = tk.Frame(actions_content, bg="#fafafa", relief=tk.FLAT)
            action_frame.pack(fill=tk.X, pady=(0, 8))
            
            # Icon
            icon_label = tk.Label(action_frame, text=icon,
                                 font=("Poppins", 16),
                                 fg=color, bg="#fafafa")
            icon_label.pack(side=tk.LEFT, padx=(15, 10), pady=10)
            
            # Text
            text_frame = tk.Frame(action_frame, bg="#fafafa")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)
            
            title_label = tk.Label(text_frame, text=title,
                                  font=("Poppins", 11, "bold"),
                                  fg=self.text_dark, bg="#fafafa")
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(text_frame, text=desc,
                                 font=("Poppins", 9),
                                 fg=self.text_light, bg="#fafafa")
            desc_label.pack(anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()