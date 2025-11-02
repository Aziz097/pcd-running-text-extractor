import cv2
import pytesseract
from moviepy.editor import VideoFileClip
import os

VIDEO_PATH = "shortvid.mp4"
OUTPUT_DIR = "clips"
START_TEXT = "PLN UPT Tanjung Karang"
END_TEXT = "INFO PLN"
MIN_CLIP_DURATION = 3.0  # detik
FRAME_SKIP = 60           # proses OCR setiap 5 frame

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

timestamps = []
start_time = None
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Hanya OCR setiap N frame
    if frame_idx % FRAME_SKIP == 0:
        h, w, _ = frame.shape
        cropped = frame[int(h*0.92):h, :]

        text = pytesseract.image_to_string(cropped, lang='ind')
        text = text.replace('\n', ' ').strip()

        cur_time = frame_idx / fps

        if START_TEXT in text and start_time is None:
            start_time = cur_time

        if END_TEXT in text and start_time is not None:
            end_time = cur_time
            if end_time - start_time >= MIN_CLIP_DURATION:
                timestamps.append((start_time, end_time))
            start_time = None

    frame_idx += 1

cap.release()

# Filter timestamps duplikat atau berdurasi pendek
timestamps = [(s, e) for (s, e) in timestamps if e - s >= MIN_CLIP_DURATION]

clip = VideoFileClip(VIDEO_PATH)

for idx, (start, end) in enumerate(timestamps):
    outname = os.path.join(OUTPUT_DIR, f"clip_{idx+1:02d}.mp4")
    subclip = clip.subclip(start, end)
    subclip.write_videofile(outname, codec="libx264", audio_codec="aac")

print(f"Done, total {len(timestamps)} clips created.")
