import os
import cv2
import pytesseract
import numpy as np
import re
from datetime import datetime

class ImageProcessingPipeline:
    def __init__(self, lang='ind'):
        self.lang = lang
        # Set path Tesseract jika di Windows
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_roi(self, frame, roi_bottom_percent=10):
        """Ekstrak ROI (10% bagian bawah layar)"""
        h, w = frame.shape[:2]
        y_start = int(h * (1 - roi_bottom_percent/100))
        roi = frame[y_start:h, 0:w]
        return roi, (y_start, h, 0, w)
    
    def preprocess_image(self, roi, save_debug=False, debug_path=None):
        """Preprocessing dengan 3 operasi PCD wajib"""
        # 1. Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        if save_debug and debug_path:
            cv2.imwrite(os.path.join(debug_path, "gray.jpg"), gray)
        
        # 2. Filtering - Median Blur (3x3) untuk mengurangi noise
        denoised = cv2.medianBlur(gray, 3)
        
        if save_debug and debug_path:
            cv2.imwrite(os.path.join(debug_path, "denoised.jpg"), denoised)
        
        # 3. Thresholding - Otsu dengan inversi (teks hitam di latar putih)
        _, binary = cv2.threshold(denoised, 0, 255, 
                                 cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        if save_debug and debug_path:
            cv2.imwrite(os.path.join(debug_path, "binary.jpg"), binary)
        
        # 4. Morphological Operations - Closing untuk menyambungkan fragmen teks
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = binary 
        
        if save_debug and debug_path:
            cv2.imwrite(os.path.join(debug_path, "cleaned.jpg"), cleaned)
        
        return cleaned
    
    def ocr_text(self, processed_roi):
        """Ekstraksi teks menggunakan Tesseract OCR"""
        # Gunakan PSM 7 (Single uniform line of text)
        config = f'--psm 6 --oem 3 -l {self.lang}'
        
        try:
            text = pytesseract.image_to_string(processed_roi, config=config)
            # Normalisasi teks
            text = text.replace('\n', ' ').strip()
            text = re.sub(r'\s+', ' ', text)  # Hilangkan multiple spaces
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
    
    def clean_text(self, text):
        """Pembersihan teks tambahan"""
        # Hanya simpan karakter alfanumerik dan spasi
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return cleaned.strip()
    
    def process_frame(self, frame, frame_idx, config, debug_dir=None):
        """Proses lengkap satu frame"""
        # Ekstrak ROI
        roi, roi_coords = self.extract_roi(frame, config['roi_bottom_percent'])
        
        # Debug: simpan ROI asli
        if debug_dir and frame_idx % 100 == 0:  # Simpan setiap 100 frame untuk debug
            cv2.imwrite(os.path.join(debug_dir, f"frame_{frame_idx:06d}_roi.jpg"), roi)
        
        # Preprocessing dengan 3 operasi PCD
        processed = self.preprocess_image(roi, 
                                         save_debug=(debug_dir is not None and frame_idx % 100 == 0),
                                         debug_path=debug_dir if frame_idx % 100 == 0 else None)
        
        # OCR
        raw_text = self.ocr_text(processed)
        cleaned_text = self.clean_text(raw_text)
        
        return {
            'frame_idx': frame_idx,
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'roi_coords': roi_coords,
            'timestamp': frame_idx / config['fps']
        }