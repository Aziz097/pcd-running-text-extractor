import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QProgressBar, QTextEdit, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import os
import json
from datetime import datetime
import cv2

# Import modul lain
from pipeline import ImageProcessingPipeline
from clip_manager import ClipManager
from utils import create_output_structure, select_output_directory

class ProcessingThread(QThread):
    progress_update = pyqtSignal(int, int)
    log_message = pyqtSignal(str)
    finished = pyqtSignal(dict)

    def __init__(self, video_path, config, output_dirs):
        super().__init__()
        self.video_path = video_path
        self.config = config
        self.output_dirs = output_dirs
        self.pipeline = ImageProcessingPipeline(lang='ind')

    def run(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise Exception(f"Tidak dapat membuka video: {self.video_path}")
            
            self.config['fps'] = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / self.config['fps']
            
            self.log_message.emit(f"🎬 Memproses video: {os.path.basename(self.video_path)}")
            self.log_message.emit(f"📊 Durasi: {duration:.1f} detik | Frame: {frame_count} | FPS: {self.config['fps']:.1f}")
            self.log_message.emit(f"⚙️  Konfigurasi: Frasa awal='{self.config['phrase_start']}', Frasa akhir='{self.config['phrase_end']}', ROI={self.config['roi_bottom_percent']}%")
            
            frames_data = []
            frame_skip = int(self.config['fps'] * 0.5)
            processed_frames = 0
            total_frames_to_process = frame_count // frame_skip
            
            self.log_message.emit(f"🔍 Menganalisis {total_frames_to_process} frame (1 frame per 0.5 detik)...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                
                if frame_idx % frame_skip == 0:
                    frame_data = self.pipeline.process_frame(
                        frame, frame_idx, self.config,
                        debug_dir=self.output_dirs['debug_dir'] if processed_frames % 20 == 0 else None
                    )
                    
                    if frame_data['cleaned_text']:
                        frames_data.append(frame_data)
                        self.log_message.emit(f"📝 Frame {frame_idx}: '{frame_data['cleaned_text']}'")
                    
                    processed_frames += 1
                    
                    # Update progress
                    if processed_frames % 10 == 0:
                        progress = (processed_frames / total_frames_to_process) * 100
                        self.progress_update.emit(int(progress), processed_frames)
            
            cap.release()
            self.log_message.emit(f"✅ Selesai analisis frame. Ditemukan {len(frames_data)} frame dengan teks terdeteksi.")
            
            # Cari klip berdasarkan frasa
            self.log_message.emit("🎯 Mencari klip berdasarkan frasa awal dan akhir...")
            clip_manager = ClipManager(self.video_path)
            clips = clip_manager.find_clips(frames_data, self.config)
            self.log_message.emit(f"📋 Ditemukan {len(clips)} klip potensial.")
            
            # Ekstrak klip video
            if clips:
                self.log_message.emit("✂️  Mengekstrak klip video...")
                new_clips = clip_manager.extract_clips(
                    clips, 
                    self.output_dirs['clips_dir'], 
                    self.output_dirs['log_path']
                )
                
                if new_clips:
                    self.log_message.emit(f"✅ Berhasil mengekstrak {len(new_clips)} klip baru!")
                    for clip in new_clips:
                        self.log_message.emit(f"   - {clip['clip_name']}: {clip['start_time']:.1f}s - {clip['end_time']:.1f}s")
                else:
                    self.log_message.emit("ℹ️  Tidak ada klip baru yang diekstrak (mungkin sudah ada di log)")
            else:
                self.log_message.emit("⚠️  Tidak ditemukan klip yang memenuhi kriteria")
            
            clip_manager.close()
            
            # Kirim hasil ke UI
            result = {
                'success': True,
                'clip_count': len(clips),
                'output_dir': self.output_dirs['output_dir']
            }
            self.finished.emit(result)
            
        except Exception as e:
            self.log_message.emit(f"❌ Error: {str(e)}")
            result = {
                'success': False,
                'error': str(e)
            }
            self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ekstraksi Running Text - KPI Komunikasi PLN")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
            }
            QProgressBar {
                height: 20px;
                border: 1px solid #bbb;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 10px;
                font-family: Consolas;
                font-size: 12px;
            }
        """)
        
        self.init_ui()
        
        # Variabel
        self.video_path = ""
        self.is_processing = False
        self.processing_thread = None
        self.output_dirs = None
    
    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Sistem Ekstraksi Running Text TV")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1a365d;")
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Untuk Verifikasi KPI Komunikasi PLN UPT Tanjung Karang")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #4a5568; font-size: 12px;")
        main_layout.addWidget(subtitle_label)
        
        # Video Input
        video_group = QGroupBox("Input Video")
        video_layout = QHBoxLayout()
        
        self.video_path_input = QLineEdit()
        self.video_path_input.setReadOnly(True)
        
        browse_btn = QPushButton("Pilih Video")
        browse_btn.clicked.connect(self.browse_video)
        
        video_layout.addWidget(self.video_path_input)
        video_layout.addWidget(browse_btn)
        video_group.setLayout(video_layout)
        main_layout.addWidget(video_group)
        
        # Parameter Ekstraksi
        param_group = QGroupBox("Parameter Ekstraksi")
        param_layout = QVBoxLayout()
        
        # Frasa Awal
        phr_start_layout = QHBoxLayout()
        phr_start_layout.addWidget(QLabel("Frasa Awal:"))
        self.phrase_start_input = QLineEdit("PLN UPT Tanjung Karang")
        phr_start_layout.addWidget(self.phrase_start_input)
        param_layout.addLayout(phr_start_layout)
        
        # Frasa Akhir
        phr_end_layout = QHBoxLayout()
        phr_end_layout.addWidget(QLabel("Frasa Akhir:"))
        self.phrase_end_input = QLineEdit("Sekian")
        phr_end_layout.addWidget(self.phrase_end_input)
        param_layout.addLayout(phr_end_layout)
        
        # Durasi Maksimal
        dur_layout = QHBoxLayout()
        dur_layout.addWidget(QLabel("Durasi Maks (detik):"))
        self.max_duration_input = QLineEdit("10")
        dur_layout.addWidget(self.max_duration_input)
        param_layout.addLayout(dur_layout)
        
        # ROI Percentage
        roi_layout = QHBoxLayout()
        roi_layout.addWidget(QLabel("ROI Bawah (%):"))
        self.roi_percent_input = QLineEdit("10")
        roi_layout.addWidget(self.roi_percent_input)
        param_layout.addLayout(roi_layout)
        
        param_group.setLayout(param_layout)
        main_layout.addWidget(param_group)
        
        # Control Buttons
        control_layout = QHBoxLayout()
        
        self.process_btn = QPushButton("Jalankan Ekstraksi")
        self.process_btn.clicked.connect(self.start_processing)
        
        self.open_output_btn = QPushButton("Buka Folder Output")
        self.open_output_btn.clicked.connect(self.open_output_folder)
        self.open_output_btn.setEnabled(False)
        
        control_layout.addWidget(self.process_btn)
        control_layout.addWidget(self.open_output_btn)
        main_layout.addLayout(control_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)
        
        # Log Area
        log_group = QGroupBox("Log Proses")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Siap - Pilih file video untuk memulai")
    
    def browse_video(self):
        """Pilih file video"""
        file_types = "Video files (*.mp4 *.avi *.mov *.mkv);;All files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            self, "Pilih File Video", "", file_types
        )
        
        if filename:
            self.video_path = filename
            self.video_path_input.setText(filename)
            self.log_message(f"✓ Video dipilih: {os.path.basename(filename)}")
            self.open_output_btn.setEnabled(False)
    
    def log_message(self, message):
        """Tambahkan pesan ke log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"{timestamp} - {message}")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
    
    def validate_inputs(self):
        """Validasi input sebelum proses"""
        if not self.video_path:
            QMessageBox.critical(self, "Error", "Silakan pilih file video terlebih dahulu")
            return False
        
        if not os.path.exists(self.video_path):
            QMessageBox.critical(self, "Error", "File video tidak ditemukan")
            return False
        
        try:
            max_duration = float(self.max_duration_input.text())
            if max_duration <= 0:
                raise ValueError("Durasi harus positif")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Durasi maksimal tidak valid: {e}")
            return False
        
        try:
            roi_percent = float(self.roi_percent_input.text())
            if not (1 <= roi_percent <= 30):
                raise ValueError("ROI harus antara 1-30%")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Persentase ROI tidak valid: {e}")
            return False
        
        if not self.phrase_start_input.text().strip():
            QMessageBox.critical(self, "Error", "Frasa awal tidak boleh kosong")
            return False
        
        if not self.phrase_end_input.text().strip():
            QMessageBox.critical(self, "Error", "Frasa akhir tidak boleh kosong")
            return False
        
        return True
    
    def start_processing(self):
        """Mulai proses ekstraksi"""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            return
        
        # Disable buttons selama proses
        self.process_btn.setEnabled(False)
        self.open_output_btn.setEnabled(False)
        self.is_processing = True
        self.status_bar.showMessage("Memproses... Harap tunggu")
        
        # Konfigurasi
        config = {
            'phrase_start': self.phrase_start_input.text().strip(),
            'phrase_end': self.phrase_end_input.text().strip(),
            'max_duration_sec': float(self.max_duration_input.text()),
            'min_duration_sec': 0.5,
            'roi_bottom_percent': float(self.roi_percent_input.text()),
            'fps': 30
        }
        
        # Pilih folder output
        output_base = select_output_directory()
        if not output_base:
            self.status_bar.showMessage("Proses dibatalkan: Folder output belum dipilih")
            self.process_btn.setEnabled(True)
            self.is_processing = False
            return
        
        # Buat struktur folder output
        self.output_dirs = create_output_structure(output_base, self.video_path)
        
        # Jalankan proses di thread terpisah
        self.processing_thread = ProcessingThread(self.video_path, config, self.output_dirs)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.log_message.connect(self.log_message)
        self.processing_thread.finished.connect(self.process_finished)
        self.processing_thread.start()
    
    def update_progress(self, value, processed_frames):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        self.status_bar.showMessage(f"Memproses... {value}% ({processed_frames} frame)")
    
    def process_finished(self, result):
        """Update UI setelah selesai proses"""
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.status_bar.showMessage("Proses selesai")
        
        if result['success']:
            clip_count = result['clip_count']
            output_dir = result['output_dir']
            
            self.log_message(f"✅ Selesai! Ditemukan {clip_count} klip.")
            self.open_output_btn.setEnabled(True)
            
            QMessageBox.information(
                self, "Selesai",
                f"Proses ekstraksi selesai!\n"
                f"Total klip ditemukan: {clip_count}\n"
                f"Hasil tersimpan di: {output_dir}"
            )
        else:
            error_msg = result['error']
            self.log_message(f"❌ Proses gagal: {error_msg}")
            QMessageBox.critical(self, "Error", f"Proses gagal:\n{error_msg}")
    
    def open_output_folder(self):
        """Buka folder output"""
        if hasattr(self, 'output_dirs') and os.path.exists(self.output_dirs['output_dir']):
            if os.name == 'nt':  # Windows
                os.startfile(self.output_dirs['output_dir'])
            else:  # Mac/Linux
                import subprocess
                subprocess.call(['open' if os.name == 'posix' else 'xdg-open', self.output_dirs['output_dir']])
        else:
            QMessageBox.information(self, "Info", "Folder output belum tersedia")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())