import os
import cv2
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def create_output_structure(output_base, video_path):
    """Buat struktur folder output berdasarkan tanggal video"""
    # Ekstrak tanggal dari nama file atau gunakan tanggal hari ini
    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    
    # Buat path folder output
    output_dir = os.path.join(output_base, year, month, f"{year}{month}{day}")
    clips_dir = os.path.join(output_dir, "clips")
    ocr_dir = os.path.join(output_dir, "ocr_raw")
    debug_dir = os.path.join(output_dir, "debug")
    
    # Buat folder jika belum ada
    for dir_path in [clips_dir, ocr_dir, debug_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Buat log file
    log_path = os.path.join(output_dir, "log_extraction.json")
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            json.dump({
                "video_path": video_path,
                "date_processed": today.strftime("%Y-%m-%d %H:%M:%S"),
                "clips": [],
                "total_clips": 0
            }, f, indent=2)
    
    return {
        "output_dir": output_dir,
        "clips_dir": clips_dir,
        "ocr_dir": ocr_dir,
        "debug_dir": debug_dir,
        "log_path": log_path
    }

def save_debug_images(frame, roi, preprocessed, output_dir, frame_idx):
    """Simpan gambar untuk visualisasi debugging"""
    debug_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_original.jpg")
    roi_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_roi.jpg")
    processed_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_processed.jpg")
    
    cv2.imwrite(debug_path, frame)
    cv2.imwrite(roi_path, roi)
    cv2.imwrite(processed_path, preprocessed)

def update_log(log_path, clip_info):
    """Update log file dengan informasi klip baru"""
    with open(log_path, 'r') as f:
        log_data = json.load(f)
    
    log_data["clips"].append(clip_info)
    log_data["total_clips"] = len(log_data["clips"])
    
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
        
def select_output_directory():
    """Pilih folder output secara manual"""
    root = tk.Tk()
    root.withdraw() 
    folder_selected = filedialog.askdirectory(title="Pilih Folder Output")
    root.destroy()
    return folder_selected