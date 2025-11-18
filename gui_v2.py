import customtkinter as ctk
from tkinter import font

# Initialize customtkinter with modern theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class VideoExtractionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Video Extraction Tool")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Configure Poppins font (with fallback)
        try:
            self.poppins = ctk.CTkFont(family="Poppins", size=13)
            self.poppins_bold = ctk.CTkFont(family="Poppins", size=14, weight="bold")
            self.title_font = ctk.CTkFont(family="Poppins", size=20, weight="bold")
        except:
            self.poppins = ctk.CTkFont(family="Segoe UI", size=13)
            self.poppins_bold = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            self.title_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main content frame (left side)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create sidebar frame (right side)
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#f0f2f5", corner_radius=20)
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.create_main_content()
        self.create_sidebar()
        
    def create_main_content(self):
        # Title section
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Video Extraction Tool", 
            font=self.title_font,
            text_color="#1a1a1a"
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 25))
        
        # Video Processing Control section
        control_frame = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color="white")
        control_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        control_frame.grid_columnconfigure((0,1), weight=1)
        
        ctk.CTkLabel(
            control_frame, 
            text="Video Processing Control", 
            font=self.poppins_bold,
            text_color="#1a1a1a"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))
        
        # File selection
        file_btn = ctk.CTkButton(
            control_frame,
            text=" Select Video File",
            font=self.poppins,
            fg_color="#e3f2fd",
            text_color="#1976d2",
            hover_color="#bbdefb",
            corner_radius=12,
            height=40,
            command=lambda: print("Select file")
        )
        file_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            control_frame,
            text="Supported formats: MP4, AVI, MOV, MKV",
            font=ctk.CTkFont(size=11),
            text_color="#616161"
        ).grid(row=2, column=0, columnspan=2, padx=20, sticky="w")
        
        # Start/End phrase inputs
        ctk.CTkLabel(control_frame, text="Start Phrase", font=self.poppins_bold).grid(
            row=3, column=0, padx=(20, 5), pady=(15, 5), sticky="w"
        )
        ctk.CTkLabel(control_frame, text="End Phrase", font=self.poppins_bold).grid(
            row=3, column=1, padx=(5, 20), pady=(15, 5), sticky="w"
        )
        
        start_entry = ctk.CTkEntry(
            control_frame,
            placeholder_text="PLN UPT Tanjung Karang",
            font=self.poppins,
            height=40,
            corner_radius=10
        )
        start_entry.grid(row=4, column=0, padx=(20, 5), pady=(0, 15), sticky="ew")
        
        end_entry = ctk.CTkEntry(
            control_frame,
            placeholder_text="Sekian",
            font=self.poppins,
            height=40,
            corner_radius=10
        )
        end_entry.grid(row=4, column=1, padx=(5, 20), pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            control_frame,
            text="Phrase that marks the beginning of clips",
            font=ctk.CTkFont(size=11),
            text_color="#616161"
        ).grid(row=5, column=0, padx=(20, 5), sticky="w")
        
        ctk.CTkLabel(
            control_frame,
            text="Phrase that marks the end of clips",
            font=ctk.CTkFont(size=11),
            text_color="#616161"
        ).grid(row=5, column=1, padx=(5, 20), sticky="w")
        
        # Max duration
        duration_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        duration_frame.grid(row=6, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="ew")
        
        ctk.CTkLabel(
            duration_frame,
            text="Maximum Clip Duration (seconds)",
            font=self.poppins_bold
        ).pack(side="left", padx=(0, 10))
        
        duration_entry = ctk.CTkEntry(
            duration_frame,
            width=80,
            justify="center",
            font=self.poppins,
            corner_radius=8
        )
        duration_entry.insert(0, "60")
        duration_entry.pack(side="left")
        
        ctk.CTkLabel(
            duration_frame,
            text="sec",
            font=self.poppins
        ).pack(side="left", padx=(5, 0))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="e")
        
        reset_btn = ctk.CTkButton(
            btn_frame,
            text=" Reset",
            font=self.poppins,
            fg_color="#f5f5f5",
            text_color="#616161",
            hover_color="#e0e0e0",
            corner_radius=12,
            width=120,
            height=40
        )
        reset_btn.pack(side="right", padx=(0, 10))
        
        extract_btn = ctk.CTkButton(
            btn_frame,
            text=" Jalankan Ekstraksi",
            font=self.poppins_bold,
            fg_color="#1976d2",
            hover_color="#1565c0",
            corner_radius=12,
            width=160,
            height=40
        )
        extract_btn.pack(side="right")
        
        # Process Status section
        status_frame = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color="white")
        status_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        ctk.CTkLabel(
            status_frame,
            text="Process Status",
            font=self.poppins_bold,
            text_color="#1a1a1a"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))
        
        status_badge = ctk.CTkFrame(
            status_frame,
            fg_color="#e8f5e9",
            corner_radius=10
        )
        status_badge.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        ctk.CTkLabel(
            status_badge,
            text=" Siap",
            text_color="#2e7d32",
            font=self.poppins_bold,
            padx=10,
            pady=5
        ).pack()
        
        ctk.CTkLabel(
            status_frame,
            text="Ready to process",
            text_color="#616161",
            font=ctk.CTkFont(size=12)
        ).grid(row=2, column=0, padx=20, sticky="w")
        
        # Results section
        results_frame = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color="white")
        results_frame.grid(row=3, column=0, sticky="nsew")
        
        ctk.CTkLabel(
            results_frame,
            text="Results",
            font=self.poppins_bold,
            text_color="#1a1a1a"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))
        
        folder_btn = ctk.CTkButton(
            results_frame,
            text=" Open Folder",
            font=self.poppins,
            fg_color="#f5f5f5",
            text_color="#616161",
            hover_color="#e0e0e0",
            corner_radius=12,
            height=35,
            width=120
        )
        folder_btn.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        ctk.CTkLabel(
            results_frame,
            text="No clips extracted yet",
            font=self.poppins_bold,
            text_color="#1a1a1a"
        ).grid(row=2, column=0, padx=20, sticky="w")
        
        ctk.CTkLabel(
            results_frame,
            text="Results will appear here",
            text_color="#616161",
            font=ctk.CTkFont(size=12)
        ).grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")
        
    def create_sidebar(self):
        # Quick Actions section
        quick_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="white", corner_radius=16)
        quick_frame.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="nsew")
        
        ctk.CTkLabel(
            quick_frame,
            text="Quick Actions",
            font=self.poppins_bold,
            text_color="#1a1a1a"
        ).pack(pady=(12, 0), anchor="w", padx=15)
        
        history_btn = ctk.CTkButton(
            quick_frame,
            text="View Processing History",
            font=self.poppins,
            fg_color="transparent",
            text_color="#1976d2",
            hover_color="#e3f2fd",
            corner_radius=8,
            height=35,
            anchor="w"
        )
        history_btn.pack(fill="x", padx=15, pady=(8, 5))
        
        ctk.CTkLabel(
            quick_frame,
            text="Last processed: Today",
            text_color="#616161",
            font=ctk.CTkFont(size=11)
        ).pack(pady=(0, 10), anchor="w", padx=15)
        
        # Sidebar actions
        actions = [
            (" Advanced Settings", "Configure detection parameters"),
            (" Help & Documentation", "User guide and tutorials"),
            (" Export Report", "Generate processing summary")
        ]
        
        for i, (title, desc) in enumerate(actions):
            action_frame = ctk.CTkFrame(
                self.sidebar_frame, 
                fg_color="white", 
                corner_radius=16
            )
            action_frame.grid(row=i+1, column=0, padx=15, pady=10, sticky="nsew")
            
            btn = ctk.CTkButton(
                action_frame,
                text=title,
                font=self.poppins_bold,
                fg_color="transparent",
                text_color="#1a1a1a",
                hover_color="#f5f5f5",
                height=45,
                anchor="w"
            )
            btn.pack(fill="x", padx=15, pady=(12, 5))
            
            ctk.CTkLabel(
                action_frame,
                text=desc,
                text_color="#616161",
                font=ctk.CTkFont(size=11)
            ).pack(pady=(0, 8), anchor="w", padx=15)

if __name__ == "__main__":
    app = VideoExtractionApp()
    app.mainloop()