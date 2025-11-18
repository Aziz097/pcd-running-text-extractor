import customtkinter as ctk
from tkinter import font

class ModernVideoProcessingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pengaturan jendela - ukuran yang pas tanpa perlu scroll
        self.title("PLN UPT Tanjung Karang - Video Processing Control")
        self.geometry("1000x700")
        self.minsize(950, 650)
        
        # Color scheme modern
        self.primary_blue = "#2962ff"
        self.card_bg = "#ffffff"
        self.success_green = "#4caf50"
        self.warning_orange = "#ff9800"
        self.error_red = "#f44336"
        self.purple = "#9c27b0"
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Main content area
        
        # Buat header dan konten utama
        self.create_header()
        self.create_main_content()
        
    def create_header(self):
        # Header frame modern dengan gradient effect
        header_frame = ctk.CTkFrame(self, height=80, fg_color=self.primary_blue, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        # Kontainer untuk header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30)
        
        # Logo dan title container
        title_container = ctk.CTkFrame(header_content, fg_color="transparent")
        title_container.pack(side="left")
        
        # Lightning bolt icon dengan style modern
        icon_label = ctk.CTkLabel(
            title_container, 
            text="⚡", 
            font=ctk.CTkFont(family="Poppins", size=24, weight="bold"),
            text_color="white"
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Title text dengan hierarki visual yang jelas
        title_label = ctk.CTkLabel(
            title_container, 
            text="PLN UPT Tanjung Karang",
            font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
            text_color="white"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Video Extraction Tool",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#e0e0e0"
        )
        subtitle_label.pack(anchor="w")
        
        # Right side - Officer info dengan tampilan modern
        officer_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        officer_frame.pack(side="right")
        
        officer_label = ctk.CTkLabel(
            officer_frame,
            text="Officer Komunikasi",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="white"
        )
        officer_label.pack(side="left", padx=(0, 15))
        
        # User avatar circle modern
        avatar_frame = ctk.CTkFrame(
            officer_frame, 
            fg_color="white", 
            width=35, 
            height=35,
            corner_radius=17.5  # Lingkaran sempurna
        )
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        avatar_label = ctk.CTkLabel(
            avatar_frame, 
            text="👤", 
            font=ctk.CTkFont(family="Poppins", size=16),
            text_color=self.primary_blue
        )
        avatar_label.pack(expand=True)
    
    def create_main_content(self):
        # Main container dengan padding yang tepat
        main_container = ctk.CTkFrame(self, fg_color="#f5f5f5")
        main_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=25)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=0, minsize=320)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Title section
        title_label = ctk.CTkLabel(
            main_container,
            text="📹 Video Processing Control",
            font=ctk.CTkFont(family="Poppins", size=20, weight="bold"),
            text_color="#333333"
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Extract video clips from TV broadcast recordings",
            font=ctk.CTkFont(family="Poppins", size=12),
            text_color="#666666"
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 20))
        
        # Columns container
        columns_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        columns_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=0, minsize=320)
        
        # Left column - Video Processing Control
        left_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Right column - Status, Results, Quick Actions
        right_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(0, 0))
        
        # Buat semua card
        self.create_video_control_card(left_column)
        self.create_status_card(right_column)
        self.create_results_card(right_column)
        self.create_quick_actions_card(right_column)
    
    def create_video_control_card(self, parent):
        # Card frame dengan rounded corners dan shadow effect
        card = ctk.CTkFrame(
            parent, 
            fg_color=self.card_bg,
            corner_radius=16,
            border_width=1,
            border_color="#e0e0e0"
        )
        card.pack(fill="both", expand=True)
        
        # Card content dengan padding
        content = ctk.CTkFrame(card, fg_color=self.card_bg)
        content.pack(padx=25, pady=25, fill="both", expand=True)
        
        # Select Video File Section
        file_label = ctk.CTkLabel(
            content, 
            text="📁 Select Video File",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color="#333333"
        )
        file_label.pack(anchor="w", pady=(0, 10))
        
        # File selection area dengan rounded corners
        file_frame = ctk.CTkFrame(
            content, 
            fg_color="#fafafa",
            corner_radius=12,
            border_width=1,
            border_color="#e0e0e0",
            height=100
        )
        file_frame.pack(fill="x", pady=(0, 20))
        file_frame.pack_propagate(False)
        
        file_text = ctk.CTkLabel(
            file_frame, 
            text="Click to select video file",
            font=ctk.CTkFont(family="Poppins", size=11),
            text_color="#666666"
        )
        file_text.pack(expand=True)
        
        formats_text = ctk.CTkLabel(
            file_frame, 
            text="Supported formats: MP4, AVI, MOV, MKV",
            font=ctk.CTkFont(family="Poppins", size=9),
            text_color="#999999"
        )
        formats_text.pack(pady=(0, 8), side="bottom")
        
        # Start Phrase
        start_label = ctk.CTkLabel(
            content, 
            text="▶️ Start Phrase",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color=self.success_green
        )
        start_label.pack(anchor="w", pady=(10, 5))
        
        self.start_entry = ctk.CTkEntry(
            content,
            font=ctk.CTkFont(family="Poppins", size=11),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0",
            height=36
        )
        self.start_entry.pack(fill="x", pady=(0, 5))
        self.start_entry.insert(0, "PLN UPT Tanjung Karang")
        
        start_hint = ctk.CTkLabel(
            content, 
            text="Phrase that marks the beginning of clips",
            font=ctk.CTkFont(family="Poppins", size=9),
            text_color="#999999"
        )
        start_hint.pack(anchor="w", pady=(0, 15))
        
        # End Phrase
        end_label = ctk.CTkLabel(
            content, 
            text="⏹️ End Phrase",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color=self.error_red
        )
        end_label.pack(anchor="w", pady=(10, 5))
        
        self.end_entry = ctk.CTkEntry(
            content,
            font=ctk.CTkFont(family="Poppins", size=11),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0",
            height=36
        )
        self.end_entry.pack(fill="x", pady=(0, 5))
        self.end_entry.insert(0, "Sekian")
        
        end_hint = ctk.CTkLabel(
            content, 
            text="Phrase that marks the end of clips",
            font=ctk.CTkFont(family="Poppins", size=9),
            text_color="#999999"
        )
        end_hint.pack(anchor="w", pady=(0, 15))
        
        # Maximum Clip Duration
        duration_label = ctk.CTkLabel(
            content, 
            text="⏱️ Maximum Clip Duration (seconds)",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color=self.warning_orange
        )
        duration_label.pack(anchor="w", pady=(10, 10))
        
        # Slider frame dengan styling modern
        slider_frame = ctk.CTkFrame(content, fg_color="transparent")
        slider_frame.pack(fill="x", pady=(0, 20))
        
        self.duration_slider = ctk.CTkSlider(
            slider_frame,
            from_=10,
            to=300,
            number_of_steps=29,
            button_color=self.primary_blue,
            button_hover_color="#1a55e6",
            progress_color=self.primary_blue,
            height=6,
            corner_radius=3
        )
        self.duration_slider.pack(fill="x", expand=True)
        self.duration_slider.set(60)
        
        self.duration_value = ctk.CTkLabel(
            slider_frame, 
            text="60\nsec",
            font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
            text_color="#333333"
        )
        self.duration_value.pack(anchor="e", padx=(0, 10), pady=(5, 0))
        
        # Buttons container
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Process button dengan gradient effect
        process_btn = ctk.CTkButton(
            button_frame,
            text="▶ Jalankan Ekstraksi",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            fg_color=self.primary_blue,
            hover_color="#1a55e6",
            text_color="white",
            corner_radius=12,
            height=40
        )
        process_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Reset button
        reset_btn = ctk.CTkButton(
            button_frame,
            text="↻ Reset",
            font=ctk.CTkFont(family="Poppins", size=12),
            fg_color="#555555",
            hover_color="#444444",
            text_color="white",
            corner_radius=12,
            height=40,
            width=100
        )
        reset_btn.pack(side="right")
    
    def create_status_card(self, parent):
        # Status card dengan rounded corners
        status_card = ctk.CTkFrame(
            parent, 
            fg_color=self.card_bg,
            corner_radius=16,
            border_width=1,
            border_color="#e0e0e0"
        )
        status_card.pack(fill="x", pady=(0, 20))
        
        status_content = ctk.CTkFrame(status_card, fg_color=self.card_bg)
        status_content.pack(padx=20, pady=20, fill="x")
        
        status_title = ctk.CTkLabel(
            status_content, 
            text="✅ Process Status",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color="#333333"
        )
        status_title.pack(anchor="w", pady=(0, 15))
        
        # Status icon dan teks dalam frame terpusat
        status_frame = ctk.CTkFrame(status_content, fg_color="transparent")
        status_frame.pack()
        
        # Green checkmark circle dengan tampilan modern
        check_frame = ctk.CTkFrame(
            status_frame, 
            fg_color="#e8f5e9",
            width=60, 
            height=60,
            corner_radius=30,
            border_width=2,
            border_color=self.success_green
        )
        check_frame.pack(pady=(0, 10))
        check_frame.pack_propagate(False)
        
        check_label = ctk.CTkLabel(
            check_frame, 
            text="✓",
            font=ctk.CTkFont(family="Poppins", size=24, weight="bold"),
            text_color=self.success_green
        )
        check_label.pack(expand=True)
        
        status_text = ctk.CTkLabel(
            status_frame, 
            text="Siap",
            font=ctk.CTkFont(family="Poppins", size=14, weight="bold"),
            text_color="#333333"
        )
        status_text.pack(pady=(0, 5))
        
        status_desc = ctk.CTkLabel(
            status_frame, 
            text="Ready to process",
            font=ctk.CTkFont(family="Poppins", size=10),
            text_color="#666666"
        )
        status_desc.pack()
    
    def create_results_card(self, parent):
        # Results card
        results_card = ctk.CTkFrame(
            parent, 
            fg_color=self.card_bg,
            corner_radius=16,
            border_width=1,
            border_color="#e0e0e0"
        )
        results_card.pack(fill="x", pady=(0, 20))
        
        results_content = ctk.CTkFrame(results_card, fg_color=self.card_bg)
        results_content.pack(padx=20, pady=20, fill="x")
        
        # Results header dengan Open Folder button
        results_header = ctk.CTkFrame(results_content, fg_color="transparent")
        results_header.pack(fill="x", pady=(0, 15))
        
        results_title = ctk.CTkLabel(
            results_header, 
            text="Results",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color="#333333"
        )
        results_title.pack(side="left")
        
        folder_btn = ctk.CTkButton(
            results_header,
            text="📁 Open Folder",
            font=ctk.CTkFont(family="Poppins", size=10),
            fg_color="#e8f5e9",
            text_color=self.success_green,
            hover_color="#c8e6c9",
            corner_radius=8,
            height=28
        )
        folder_btn.pack(side="right")
        
        # Results area dengan rounded corners
        results_area = ctk.CTkFrame(
            results_content, 
            fg_color="#fafafa",
            corner_radius=12,
            height=80
        )
        results_area.pack(fill="x")
        results_area.pack_propagate(False)
        
        # No results icon dan teks
        no_results = ctk.CTkLabel(
            results_area, 
            text="📂",
            font=ctk.CTkFont(family="Poppins", size=24),
            text_color="#cccccc"
        )
        no_results.pack(pady=(10, 5))
        
        no_results_text = ctk.CTkLabel(
            results_area, 
            text="No clips extracted yet",
            font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
            text_color="#666666"
        )
        no_results_text.pack()
        
        no_results_desc = ctk.CTkLabel(
            results_area, 
            text="Results will appear here",
            font=ctk.CTkFont(family="Poppins", size=9),
            text_color="#999999"
        )
        no_results_desc.pack()
    
    def create_quick_actions_card(self, parent):
        # Quick Actions card
        actions_card = ctk.CTkFrame(
            parent, 
            fg_color=self.card_bg,
            corner_radius=16,
            border_width=1,
            border_color="#e0e0e0"
        )
        actions_card.pack(fill="x")
        
        actions_content = ctk.CTkFrame(actions_card, fg_color=self.card_bg)
        actions_content.pack(padx=20, pady=20, fill="x")
        
        actions_title = ctk.CTkLabel(
            actions_content, 
            text="Quick Actions",
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
            text_color="#333333"
        )
        actions_title.pack(anchor="w", pady=(0, 15))
        
        # Action items dengan styling modern
        actions = [
            ("🕐", "View Processing History", "Last processed: Today", self.purple),
            ("⚙️", "Advanced Settings", "Configure detection parameters", self.error_red),
            ("❓", "Help & Documentation", "User guide and tutorials", self.warning_orange),
            ("📊", "Export Report", "Generate processing summary", self.success_green)
        ]
        
        for i, (icon, title, desc, color) in enumerate(actions):
            action_frame = ctk.CTkFrame(
                actions_content, 
                fg_color="#fafafa",
                corner_radius=10
            )
            action_frame.pack(fill="x", pady=(0, 8))
            
            # Icon dengan warna sesuai kategori
            icon_label = ctk.CTkLabel(
                action_frame, 
                text=icon,
                font=ctk.CTkFont(family="Poppins", size=16),
                text_color=color
            )
            icon_label.pack(side="left", padx=(15, 10), pady=10)
            
            # Text container
            text_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True, pady=10)
            
            title_label = ctk.CTkLabel(
                text_frame, 
                text=title,
                font=ctk.CTkFont(family="Poppins", size=11, weight="bold"),
                text_color="#333333"
            )
            title_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(
                text_frame, 
                text=desc,
                font=ctk.CTkFont(family="Poppins", size=9),
                text_color="#666666"
            )
            desc_label.pack(anchor="w")

if __name__ == "__main__":
    # Set theme dan default appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = ModernVideoProcessingApp()
    app.mainloop()