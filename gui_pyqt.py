import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFrame, QSlider, QLineEdit, QSizePolicy,
                            QFileDialog, QScrollArea, QGridLayout, QSpacerItem, QStyle)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QLinearGradient, QBrush, QPen, QIcon, QPixmap, QCursor

class ModernButton(QPushButton):
    def __init__(self, text, primary=False, icon=None):
        super().__init__(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2962ff;
                    color: white;
                    border-radius: 12px;
                    font-family: 'Poppins';
                    font-weight: bold;
                    font-size: 12px;
                    padding: 10px 15px;
                }
                QPushButton:hover {
                    background-color: #1a55e6;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    color: #333333;
                    border-radius: 12px;
                    font-family: 'Poppins';
                    font-size: 12px;
                    padding: 10px 15px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
        
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))
            self.setStyleSheet(self.styleSheet() + "text-align: left; padding-left: 30px;")

class StatusCard(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("✅ Process Status")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #333333;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Status content
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        
        # Status circle
        status_circle = QWidget()
        status_circle.setFixedSize(60, 60)
        status_circle.setStyleSheet("""
            background-color: #e8f5e9;
            border-radius: 30px;
            border: 2px solid #4caf50;
        """)
        
        check_label = QLabel("✓", status_circle)
        check_label.setStyleSheet("""
            font-family: 'Poppins';
            font-weight: bold;
            font-size: 24px;
            color: #4caf50;
        """)
        check_label.setAlignment(Qt.AlignCenter)
        
        status_layout.addWidget(status_circle, alignment=Qt.AlignCenter)
        
        # Status text
        status_text = QLabel("Siap")
        status_text.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 14px;
                color: #333333;
                margin-top: 5px;
            }
        """)
        status_text.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_text)
        
        # Status description
        status_desc = QLabel("Ready to process")
        status_desc.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 10px;
                color: #666666;
                margin-top: 2px;
            }
        """)
        status_desc.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_desc)
        
        main_layout.addLayout(status_layout)
        main_layout.addStretch()

class ResultsCard(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header with title and button
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Results")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #333333;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        folder_btn = QPushButton("📁 Open Folder")
        folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8f5e9;
                color: #4caf50;
                border-radius: 8px;
                font-family: 'Poppins';
                font-size: 10px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #c8e6c9;
            }
        """)
        folder_btn.setCursor(QCursor(Qt.PointingHandCursor))
        header_layout.addWidget(folder_btn)
        
        main_layout.addLayout(header_layout)
        
        # Results area
        results_area = QWidget()
        results_area.setFixedHeight(80)
        results_area.setStyleSheet("""
            background-color: #fafafa;
            border-radius: 12px;
        """)
        
        results_layout = QVBoxLayout(results_area)
        results_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel("📂")
        icon_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 24px;
                color: #cccccc;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(icon_label)
        
        title_label = QLabel("No clips extracted yet")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 11px;
                color: #666666;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(title_label)
        
        desc_label = QLabel("Results will appear here")
        desc_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 9px;
                color: #999999;
            }
        """)
        desc_layout = QHBoxLayout()
        desc_layout.addStretch()
        desc_layout.addWidget(desc_label)
        desc_layout.addStretch()
        results_layout.addLayout(desc_layout)
        
        main_layout.addWidget(results_area)
        main_layout.addStretch()

class QuickActionsCard(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Quick Actions")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #333333;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Actions
        actions = [
            ("🕐", "View Processing History", "Last processed: Today", "#9c27b0"),
            ("⚙️", "Advanced Settings", "Configure detection parameters", "#f44336"),
            ("❓", "Help & Documentation", "User guide and tutorials", "#ff9800"),
            ("📊", "Export Report", "Generate processing summary", "#4caf50")
        ]
        
        for icon, title, desc, color in actions:
            action_widget = QWidget()
            action_widget.setStyleSheet("""
                QWidget {
                    background-color: #fafafa;
                    border-radius: 10px;
                }
            """)
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(15, 10, 15, 10)
            action_layout.setSpacing(15)
            
            # Icon
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(f"""
                QLabel {{
                    font-family: 'Poppins';
                    font-size: 16px;
                    color: {color};
                }}
            """)
            action_layout.addWidget(icon_label)
            
            # Text container
            text_widget = QWidget()
            text_layout = QVBoxLayout(text_widget)
            text_layout.setContentsMargins(0, 0, 0, 0)
            text_layout.setSpacing(2)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-family: 'Poppins';
                    font-weight: bold;
                    font-size: 11px;
                    color: #333333;
                }
            """)
            text_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("""
                QLabel {
                    font-family: 'Poppins';
                    font-size: 9px;
                    color: #666666;
                }
            """)
            text_layout.addWidget(desc_label)
            
            action_layout.addWidget(text_widget)
            action_layout.addStretch()
            
            main_layout.addWidget(action_widget)
        
        main_layout.addStretch()

class VideoControlCard(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Select Video File section
        file_label = QLabel("📁 Select Video File")
        file_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #333333;
            }
        """)
        main_layout.addWidget(file_label)
        
        # File selection area
        file_frame = QWidget()
        file_frame.setFixedHeight(100)
        file_frame.setStyleSheet("""
            background-color: #fafafa;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
        """)
        
        file_layout = QVBoxLayout(file_frame)
        file_layout.setAlignment(Qt.AlignCenter)
        
        file_text = QLabel("Click to select video file")
        file_text.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 11px;
                color: #666666;
            }
        """)
        file_text.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(file_text)
        
        formats_text = QLabel("Supported formats: MP4, AVI, MOV, MKV")
        formats_text.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 9px;
                color: #999999;
            }
        """)
        formats_text.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(formats_text)
        
        main_layout.addWidget(file_frame)
        
        # Start and End Phrase section
        phrase_layout = QHBoxLayout()
        phrase_layout.setSpacing(20)
        
        # Start Phrase
        start_layout = QVBoxLayout()
        start_layout.setSpacing(5)
        
        start_label = QLabel("▶️ Start Phrase")
        start_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #4caf50;
            }
        """)
        start_layout.addWidget(start_label)
        
        self.start_entry = QLineEdit()
        self.start_entry.setText("PLN UPT Tanjung Karang")
        self.start_entry.setStyleSheet("""
            QLineEdit {
                font-family: 'Poppins';
                font-size: 11px;
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
        """)
        self.start_entry.setFixedHeight(36)
        start_layout.addWidget(self.start_entry)
        
        start_hint = QLabel("Phrase that marks the beginning of clips")
        start_hint.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 9px;
                color: #999999;
            }
        """)
        start_layout.addWidget(start_hint)
        
        # End Phrase
        end_layout = QVBoxLayout()
        end_layout.setSpacing(5)
        
        end_label = QLabel("⏹️ End Phrase")
        end_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #f44336;
            }
        """)
        end_layout.addWidget(end_label)
        
        self.end_entry = QLineEdit()
        self.end_entry.setText("Sekian")
        self.end_entry.setStyleSheet("""
            QLineEdit {
                font-family: 'Poppins';
                font-size: 11px;
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
            }
        """)
        self.end_entry.setFixedHeight(36)
        end_layout.addWidget(self.end_entry)
        
        end_hint = QLabel("Phrase that marks the end of clips")
        end_hint.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 9px;
                color: #999999;
            }
        """)
        end_layout.addWidget(end_hint)
        
        phrase_layout.addLayout(start_layout)
        phrase_layout.addLayout(end_layout)
        main_layout.addLayout(phrase_layout)
        
        # Duration section
        duration_label = QLabel("⏱️ Maximum Clip Duration (seconds)")
        duration_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                color: #ff9800;
            }
        """)
        main_layout.addWidget(duration_label)
        
        # Slider container
        slider_container = QWidget()
        slider_layout = QHBoxLayout(slider_container)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        
        # Custom slider
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(10, 300)
        self.duration_slider.setValue(60)
        self.duration_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #e0e0e0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #2962ff;
                border: 2px solid white;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #2962ff;
                border-radius: 3px;
            }
        """)
        
        slider_layout.addWidget(self.duration_slider)
        
        # Duration value
        self.duration_value = QLabel("60\nsec")
        self.duration_value.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 11px;
                color: #333333;
                margin-left: 10px;
                text-align: right;
            }
        """)
        slider_layout.addWidget(self.duration_value)
        
        main_layout.addWidget(slider_container)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # Process button
        process_btn = QPushButton("▶ Jalankan Ekstraksi")
        process_btn.setStyleSheet("""
            QPushButton {
                background-color: #2962ff;
                color: white;
                border-radius: 12px;
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1a55e6;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn, 2)
        
        # Reset button
        reset_btn = QPushButton("↻ Reset")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                border-radius: 12px;
                font-family: 'Poppins';
                font-size: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)
        reset_btn.setFixedHeight(40)
        button_layout.addWidget(reset_btn, 1)
        
        main_layout.addWidget(button_container)
        main_layout.addStretch()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup window
        self.setWindowTitle("PLN UPT Tanjung Karang - Video Processing Control")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(20)
        
        # Title section
        title_label = QLabel("📹 Video Processing Control")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 20px;
                color: #333333;
            }
        """)
        content_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Extract video clips from TV broadcast recordings")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 12px;
                color: #666666;
            }
        """)
        content_layout.addWidget(subtitle_label)
        
        # Create two columns
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setContentsMargins(0, 0, 0, 0)
        columns_layout.setSpacing(30)
        
        # Left column - Video Control
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        
        video_control_card = VideoControlCard()
        video_control_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        left_layout.addWidget(video_control_card)
        left_layout.addStretch()
        
        # Right column - Status, Results, Quick Actions
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        
        # Status card
        status_card = StatusCard()
        status_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        right_layout.addWidget(status_card)
        
        # Results card
        results_card = ResultsCard()
        results_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        right_layout.addWidget(results_card)
        
        # Quick actions card
        quick_actions_card = QuickActionsCard()
        quick_actions_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
            }
        """)
        right_layout.addWidget(quick_actions_card)
        right_layout.addStretch()
        
        # Add columns to layout
        columns_layout.addWidget(left_column, 2)  # 2/3 width
        columns_layout.addWidget(right_column, 1)  # 1/3 width
        
        content_layout.addWidget(columns_widget)
        main_layout.addWidget(content_area)
        
        # Connect slider to value display
        video_control_card.duration_slider.valueChanged.connect(
            lambda value: setattr(video_control_card.duration_value, 'text', f"{value}\nsec")
        )
        
        # Connect file selection area
        file_frame = video_control_card.findChild(QWidget)
        if file_frame:
            file_frame.mousePressEvent = lambda event: self.select_video_file()
    
    def create_header(self):
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #2962ff;")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(40, 0, 40, 0)
        
        # Left side - Logo and title
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lightning icon
        icon_label = QLabel("⚡")
        icon_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 24px;
                color: white;
            }
        """)
        left_layout.addWidget(icon_label)
        left_layout.addSpacing(10)
        
        # Title container
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        title_label = QLabel("PLN UPT Tanjung Karang")
        title_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-weight: bold;
                font-size: 16px;
                color: white;
            }
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Video Extraction Tool")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 12px;
                color: #e0e0e0;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        left_layout.addWidget(title_container)
        left_layout.addStretch()
        
        # Right side - Officer info
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        officer_label = QLabel("Officer Komunikasi")
        officer_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 12px;
                color: white;
            }
        """)
        right_layout.addWidget(officer_label)
        
        # Avatar
        avatar = QWidget()
        avatar.setFixedSize(35, 35)
        avatar.setStyleSheet("""
            background-color: white;
            border-radius: 17px;
        """)
        
        avatar_label = QLabel("👤", avatar)
        avatar_label.setStyleSheet("""
            QLabel {
                font-family: 'Poppins';
                font-size: 16px;
                color: #2962ff;
            }
        """)
        avatar_label.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(avatar)
        
        layout.addWidget(left_container, 1)
        layout.addWidget(right_container, 0)
        
        return header
    
    def select_video_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
            options=options
        )
        if file_name:
            print(f"Selected file: {file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font to Poppins if available
    font = QFont("Poppins", 10)
    if not font.exactMatch():
        # Fallback to system font if Poppins is not available
        font = QFont()
        font.setFamily("Segoe UI" if sys.platform == "win32" else "Helvetica")
        font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())