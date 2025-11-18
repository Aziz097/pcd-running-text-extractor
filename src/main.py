import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import cv2
from datetime import datetime
from pipeline import ImageProcessingPipeline
from clip_manager import ClipManager
from utils import create_output_structure, select_output_directory

class RunningTextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ekstraksi Running Text - KPI Komunikasi PLN")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Setup UI
        self.setup_ui()
        
        # Inisialisasi variabel
        self.video_path = ""
        self.is_processing = False
        self.pipeline = ImageProcessingPipeline(lang='ind')
        
    def setup_ui(self):
        """Buat antarmuka pengguna"""
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul aplikasi
        title_label = ttk.Label(main_frame, 
                              text="Sistem Ekstraksi Running Text TV",
                              font=("Arial", 16, "bold"),
                              foreground="#1a365d")
        title_label.pack(pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame,
                                 text="Untuk Verifikasi KPI Komunikasi PLN UPT Tanjung Karang",
                                 font=("Arial", 10),
                                 foreground="#4a5568")
        subtitle_label.pack(pady=(0, 30))
        
        # Frame input video
        video_frame = ttk.LabelFrame(main_frame, text="Input Video", padding="10")
        video_frame.pack(fill=tk.X, pady=10)
        
        self.video_path_var = tk.StringVar()
        video_entry = ttk.Entry(video_frame, textvariable=self.video_path_var, width=50)
        video_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(video_frame, text="Pilih Video", command=self.browse_video)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame parameter ekstraksi
        param_frame = ttk.LabelFrame(main_frame, text="Parameter Ekstraksi", padding="10")
        param_frame.pack(fill=tk.X, pady=10)
        
        # Frasa awal
        ttk.Label(param_frame, text="Frasa Awal:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.phrase_start_var = tk.StringVar(value="PLN UPT Tanjung Karang")
        ttk.Entry(param_frame, textvariable=self.phrase_start_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        
        # Frasa akhir
        ttk.Label(param_frame, text="Frasa Akhir:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phrase_end_var = tk.StringVar(value="Sekian")
        ttk.Entry(param_frame, textvariable=self.phrase_end_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        
        # Durasi maksimal
        ttk.Label(param_frame, text="Durasi Maks (detik):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_duration_var = tk.StringVar(value="10")
        ttk.Entry(param_frame, textvariable=self.max_duration_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # ROI percentage
        ttk.Label(param_frame, text="ROI Bawah (%):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.roi_percent_var = tk.StringVar(value="10")
        ttk.Entry(param_frame, textvariable=self.roi_percent_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame kontrol
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=20)
        
        self.process_btn = ttk.Button(control_frame, 
                                    text="Jalankan Ekstraksi", 
                                    command=self.start_processing,
                                    style="Accent.TButton")
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_output_btn = ttk.Button(control_frame, 
                                         text="Buka Folder Output", 
                                         command=self.open_output_folder,
                                         state=tk.DISABLED)
        self.open_output_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Siap - Pilih file video untuk memulai")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=10)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log Proses", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=10, 
                                                 font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Tambahkan style untuk tombol utama
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
        
        # Folder output default
        self.output_base = os.path.join(os.getcwd(), "data", "output")
        os.makedirs(self.output_base, exist_ok=True)
    
    def browse_video(self):
        """Pilih file video"""
        file_types = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Pilih File Video",
            filetypes=file_types,
            initialdir=os.path.join(os.getcwd(), "data", "input")
        )
        
        if filename:
            self.video_path = filename
            self.video_path_var.set(filename)
            self.add_log(f"✓ Video dipilih: {os.path.basename(filename)}")
            self.open_output_btn.config(state=tk.DISABLED)
    
    def add_log(self, message):
        """Tambahkan pesan ke log area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update()
    
    def open_output_folder(self):
        """Buka folder output"""
        if hasattr(self, 'current_output_dir') and os.path.exists(self.current_output_dir):
            if os.name == 'nt':  # Windows
                os.startfile(self.current_output_dir)
            else:  # Mac/Linux
                import subprocess
                subprocess.call(['open' if os.name == 'posix' else 'xdg-open', self.current_output_dir])
        else:
            messagebox.showinfo("Info", "Folder output belum tersedia")
    
    def validate_inputs(self):
        """Validasi input sebelum proses"""
        if not self.video_path:
            messagebox.showerror("Error", "Silakan pilih file video terlebih dahulu")
            return False
        
        if not os.path.exists(self.video_path):
            messagebox.showerror("Error", "File video tidak ditemukan")
            return False
        
        try:
            max_duration = float(self.max_duration_var.get())
            if max_duration <= 0:
                raise ValueError("Durasi harus positif")
        except ValueError as e:
            messagebox.showerror("Error", f"Durasi maksimal tidak valid: {e}")
            return False
        
        try:
            roi_percent = float(self.roi_percent_var.get())
            if not (1 <= roi_percent <= 30):
                raise ValueError("ROI harus antara 1-30%")
        except ValueError as e:
            messagebox.showerror("Error", f"Persentase ROI tidak valid: {e}")
            return False
        
        if not self.phrase_start_var.get().strip():
            messagebox.showerror("Error", "Frasa awal tidak boleh kosong")
            return False
        
        if not self.phrase_end_var.get().strip():
            messagebox.showerror("Error", "Frasa akhir tidak boleh kosong")
            return False
        
        return True
    
    def start_processing(self):
        """Mulai proses ekstraksi"""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            return
        
        # Disable buttons selama proses
        self.process_btn.config(state=tk.DISABLED)
        self.open_output_btn.config(state=tk.DISABLED)
        self.is_processing = True
        
        # Konfigurasi
        config = {
            'phrase_start': self.phrase_start_var.get().strip(),
            'phrase_end': self.phrase_end_var.get().strip(),
            'max_duration_sec': float(self.max_duration_var.get()),
            'min_duration_sec': 0.5,
            'roi_bottom_percent': float(self.roi_percent_var.get()),
            'fps': 30
        } # Ensure to replace 'your_module' with the actual module name

        output_base = select_output_directory()
        if not output_base:
            messagebox.showwarning("Batal", "Folder output belum dipilih.")
            self.process_btn.config(state=tk.NORMAL)
            self.is_processing = False
            return
        
        # Buat struktur folder output
        output_dirs = create_output_structure(output_base, self.video_path)
        self.current_output_dir = output_dirs['output_dir']
        
        # Jalankan proses di thread terpisah
        thread = threading.Thread(target=self.process_video, args=(config, output_dirs))
        thread.daemon = True
        thread.start()
    
    def process_video(self, config, output_dirs):
        """Proses video utama"""
        try:
            # Buka video untuk mendapatkan FPS
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise Exception(f"Tidak dapat membuka video: {self.video_path}")
            
            config['fps'] = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / config['fps']
            
            self.add_log(f"🎬 Memproses video: {os.path.basename(self.video_path)}")
            self.add_log(f"📊 Durasi: {duration:.1f} detik | Frame: {frame_count} | FPS: {config['fps']:.1f}")
            self.add_log(f"⚙️  Konfigurasi: Frasa awal='{config['phrase_start']}', Frasa akhir='{config['phrase_end']}', ROI={config['roi_bottom_percent']}%")
            
            # Setup struktur output
            output_dirs = create_output_structure(self.output_base, self.video_path)
            self.current_output_dir = output_dirs['output_dir']
            
            # Inisialisasi ClipManager
            clip_manager = ClipManager(self.video_path)
            
            # Proses frame
            frames_data = []
            frame_skip = int(config['fps'] * 0.5)  # 1 frame per 0.5 detik
            processed_frames = 0
            total_frames_to_process = frame_count // frame_skip
            
            self.add_log(f"🔍 Menganalisis {total_frames_to_process} frame (1 frame per 0.5 detik)...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                
                # Hanya proses setiap N frame
                if frame_idx % frame_skip == 0:
                    frame_data = self.pipeline.process_frame(
                        frame, frame_idx, config,
                        debug_dir=output_dirs['debug_dir'] if processed_frames % 20 == 0 else None
                    )
                    
                    if frame_data['cleaned_text']:
                        frames_data.append(frame_data)
                        self.add_log(f"📝 Frame {frame_idx}: '{frame_data['cleaned_text']}'")
                    
                    processed_frames += 1
                    
                    # Update progress
                    if processed_frames % 10 == 0:
                        progress = (processed_frames / total_frames_to_process) * 100
                        self.update_status(f"Memproses... {progress:.1f}% ({processed_frames}/{total_frames_to_process})")
            
            cap.release()
            self.add_log(f"✅ Selesai analisis frame. Ditemukan {len(frames_data)} frame dengan teks terdeteksi.")
            
            # Cari klip berdasarkan frasa
            self.add_log("🎯 Mencari klip berdasarkan frasa awal dan akhir...")
            clips = clip_manager.find_clips(frames_data, config)
            self.add_log(f"📋 Ditemukan {len(clips)} klip potensial.")
            
            # Ekstrak klip video
            if clips:
                self.add_log("✂️  Mengekstrak klip video...")
                new_clips = clip_manager.extract_clips(
                    clips, 
                    output_dirs['clips_dir'], 
                    output_dirs['log_path']
                )
                
                if new_clips:
                    self.add_log(f"✅ Berhasil mengekstrak {len(new_clips)} klip baru!")
                    # Update log
                    for clip in new_clips:
                        self.add_log(f"   - {clip['clip_name']}: {clip['start_time']:.1f}s - {clip['end_time']:.1f}s")
                else:
                    self.add_log("ℹ️  Tidak ada klip baru yang diekstrak (mungkin sudah ada di log)")
            else:
                self.add_log("⚠️  Tidak ditemukan klip yang memenuhi kriteria")
            
            # Tutup resource
            clip_manager.close()
            
            # Update UI
            self.root.after(0, self.update_ui_after_processing, len(clips))
            
        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}")
            self.root.after(0, self.update_ui_after_error)
    
    def update_ui_after_processing(self, clip_count):
        """Update UI setelah selesai proses"""
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.open_output_btn.config(state=tk.NORMAL)
        
        if clip_count > 0:
            self.update_status(f"✅ Selesai! Ditemukan {clip_count} klip. Klik 'Buka Folder Output' untuk melihat hasil.")
        else:
            self.update_status("⚠️ Selesai! Tidak ditemukan klip yang sesuai kriteria.")
        
        messagebox.showinfo("Selesai", 
                           f"Proses ekstraksi selesai!\n"
                           f"Total klip ditemukan: {clip_count}\n"
                           f"Hasil tersimpan di: {self.current_output_dir}")
    
    def update_ui_after_error(self):
        """Update UI jika terjadi error"""
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.update_status("❌ Proses gagal - lihat log untuk detail error")

if __name__ == "__main__":
    root = tk.Tk()
    app = RunningTextExtractorApp(root)
    root.mainloop()