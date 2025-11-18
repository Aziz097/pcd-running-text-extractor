import cv2
import pytesseract
from moviepy.editor import VideoFileClip
import os
import sys

# ========== Input Dinamis ==========
VIDEO_PATH = input("Masukkan path video (cth: nama_video.mp4): ").strip()
OUTPUT_DIR = input("Masukkan nama folder output (cth: nama_folder): ").strip()
if not OUTPUT_DIR:
    OUTPUT_DIR = "clips"

# ========== Konfigurasi ==========
START_TEXT = "PLN UPT Tanjung Karang"
END_TEXT = "INFO PLN"
MIN_CLIP_DURATION = 4.0
FRAME_SKIP = 30
MAX_WAIT_AFTER_START =float( input("Masukan limit durasi video clip (cth: 15): "))

# ========== Utility ==========
def print_section(title):
    print("\n" + "═" * 60)  
    print(f"{title}")
    print("═" * 60)

def color(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

# Warna ANSI
GREEN = "92"
YELLOW = "93"
BLUE = "94"
CYAN = "96"
RED = "91"

# ========== Setup ==========
os.makedirs(OUTPUT_DIR, exist_ok=True)
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"{color('[ERROR]', RED)} Gagal membuka video: {VIDEO_PATH}")
    sys.exit(1)
    
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print_section(color("📁 VIDEO TERDETEKSI", BLUE))
print(f"{color('[INFO]', CYAN)} File          : {VIDEO_PATH}")
print(f"{color('[INFO]', CYAN)} Durasi        : {duration:.2f} detik")
print(f"{color('[INFO]', CYAN)} Resolusi FPS  : {fps:.2f}")
print(f"{color('[INFO]', CYAN)} Total Frame   : {frame_count}")
print(f"{color('[INFO]', CYAN)} Frame Skip    : setiap {FRAME_SKIP} frame")

# ========== Deteksi Teks ==========
timestamps = []
start_time = None
ready_to_end = False
frame_idx = 0
progress_interval = max(int(frame_count / 10), 1)

print_section(color("🧠 MEMULAI DETEKSI TEKS", BLUE))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_idx % FRAME_SKIP == 0:
        h, w, _ = frame.shape
        cropped = frame[int(h * 0.92):h, :]
        text = pytesseract.image_to_string(cropped, lang='ind').replace('\n', ' ').strip()
        cur_time = frame_idx / fps

        # Deteksi awal
        if START_TEXT in text and start_time is None:
            start_time = cur_time
            ready_to_end = False
            print(f"{color('[DETEKSI]', YELLOW)} START @ {start_time:.2f}s → Tunggu {MIN_CLIP_DURATION:.1f}s sebelum cek END...")

        # Siap mendeteksi END
        if start_time is not None:
            if not ready_to_end and cur_time >= start_time + MIN_CLIP_DURATION:
                ready_to_end = True

            # Normal END detection
            if END_TEXT in text and ready_to_end:
                end_time = cur_time
                duration_clip = end_time - start_time
                timestamps.append((start_time, end_time))
                print(f"{color('[KLIP]', GREEN)} END @ {end_time:.2f}s → Klip berdurasi {duration_clip:.2f}s disimpan.")
                start_time = None
                ready_to_end = False

            # Fallback jika melebihi batas waktu
            elif cur_time >= start_time + MAX_WAIT_AFTER_START:
                end_time = start_time + MAX_WAIT_AFTER_START
                duration_clip = end_time - start_time
                timestamps.append((start_time, end_time))
                print(f"{color('[FALLBACK]', RED)} END tidak terdeteksi, fallback @ {end_time:.2f}s → Klip berdurasi {duration_clip:.2f}s.")
                start_time = None
                ready_to_end = False

    if frame_idx % progress_interval == 0:
        progress = (frame_idx / frame_count) * 100
        print(f"{color('[PROGRESS]', CYAN)} {progress:.0f}% frame diproses...")

    frame_idx += 1

cap.release()

# ========== Pemotongan Video ==========
print_section(color("✂️  PEMOTONGAN KLIP", BLUE))
print(f"{color('[INFO]', CYAN)} Total klip terdeteksi: {len(timestamps)}\n")

clip = VideoFileClip(VIDEO_PATH)
for idx, (start, end) in enumerate(timestamps):
    outname = os.path.join(OUTPUT_DIR, f"clip_{idx+1:02d}.mp4")
    print(f"{color('[CLIP]', GREEN)} #{idx+1:02d} → {start:.2f}s sampai {end:.2f}s → {outname}")
    subclip = clip.subclip(start, end)
    subclip.write_videofile(outname, codec="libx264", audio_codec="aac", verbose=False, logger=None)

# ========== Selesai ==========
print_section(color("✅ SELESAI", GREEN))
print(f"{color('[DONE]', GREEN)} {len(timestamps)} klip berhasil disimpan di folder: '{OUTPUT_DIR}'")
