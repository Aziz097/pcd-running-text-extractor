from moviepy.editor import VideoFileClip
import os
import json
from difflib import SequenceMatcher
import numpy as np
from datetime import datetime

class ClipManager:
    def __init__(self, video_path):
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        self.fps = self.clip.fps
    
    def load_existing_clips(self, log_path):
        """Muat klip yang sudah ada dari log file"""
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                return json.load(f).get('clips', [])
        return []
    
    def is_similar_text(self, text1, text2, threshold=0.8):
        """Periksa kesamaan teks dengan fuzzy matching"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio() >= threshold
    
    def find_clips(self, frames_data, config):
        """Cari klip berdasarkan frasa awal dan akhir"""
        clips = []
        start_time = None
        current_text = ""
        
        for frame_data in frames_data:
            text = frame_data['cleaned_text']
            timestamp = frame_data['timestamp']
            
            # Cek frasa awal
            if config['phrase_start'] in text and start_time is None:
                start_time = timestamp
                current_text = text
            
            # Jika sudah ada start_time, cek frasa akhir dalam batas waktu
            if start_time is not None:
                # Cek jika frasa akhir ditemukan
                if config['phrase_end'] in text:
                    end_time = timestamp
                    
                    # Pastikan durasi minimal terpenuhi
                    if end_time - start_time >= config['min_duration_sec']:
                        clips.append({
                            'start_time': start_time,
                            'end_time': end_time,
                            'text': current_text,
                            'frame_start': frame_data['frame_idx'],
                            'confidence': 0.95  # Bisa dihitung berdasarkan kesamaan teks
                        })
                    
                    # Reset untuk pencarian berikutnya
                    start_time = None
                    current_text = ""
                
                # Jika melebihi batas waktu maksimal, reset
                elif timestamp - start_time > config['max_duration_sec']:
                    start_time = None
                    current_text = ""
        
        return clips
    
    def extract_clips(self, clips_data, output_dir, log_path):
        """Ekstrak klip video berdasarkan data klip"""
        existing_clips = self.load_existing_clips(log_path)
        new_clips = []
        
        for idx, clip_data in enumerate(clips_data):
            # Skip jika klip sudah ada
            if any(abs(clip_data['start_time'] - ec['start_time']) < 0.5 and 
                  abs(clip_data['end_time'] - ec['end_time']) < 0.5 for ec in existing_clips):
                continue
            
            # Potong klip dengan margin
            margin = 0.3  # 0.3 detik margin di awal dan akhir
            start = max(0, clip_data['start_time'] - margin)
            end = min(self.clip.duration, clip_data['end_time'] + margin)
            
            # Nama file
            clip_name = f"clip_{idx+1:03d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            output_path = os.path.join(output_dir, clip_name)
            
            try:
                # Ekstrak subclip
                subclip = self.clip.subclip(start, end)
                subclip.write_videofile(output_path, 
                                      codec="libx264", 
                                      audio_codec="aac",
                                      verbose=False,
                                      logger=None)
                
                # Update log
                clip_info = {
                    "clip_name": clip_name,
                    "start_time": start,
                    "end_time": end,
                    "original_text": clip_data['text'],
                    "confidence": clip_data['confidence'],
                    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                new_clips.append(clip_info)
                
                print(f"✓ Klip berhasil diekstraksi: {clip_name}")
                
            except Exception as e:
                print(f"✗ Error ekstrak klip {idx+1}: {e}")
        
        return new_clips
    
    def close(self):
        """Tutup resource video"""
        self.clip.close()