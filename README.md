## 🛠️ Installation & Setup

### 1. Install Tesseract OCR (wajib)
- **Windows**:  
  Download installer dari [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)  
  Install, lalu tambahkan path ke environment variable:  
  ```
  C:\Program Files\Tesseract-OCR
  ```
- **Linux**:  
  ```bash
  sudo apt install tesseract-ocr
  ```

### 2. Tambahkan Bahasa Indonesia
Download file: [`ind.traineddata`](https://github.com/tesseract-ocr/tessdata/blob/main/ind.traineddata)  
Simpan ke folder `tessdata` (biasanya di `C:\Program Files\Tesseract-OCR\tessdata` atau `/usr/share/tesseract-ocr/4.00/tessdata/`)

### 3. Install dependensi Python
```bash
pip install opencv-python pytesseract moviepy
```

> ⚠️ Pastikan `pytesseract` bisa menemukan `tesseract`:
> ```python
> import pytesseract
> pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows only
> ```
---

## Struktur Proyek 

```
pcd-running-text/
├── src/
│   ├── main.py                 # Entry point
│   ├── image_pipeline.py       # Preprocessing + OCR
│   └── clip_manager.py         # Timestamp validation & clipping
├── data/
│   ├── input/                  # Dataset primer (rekaman TV lokal)
│   └── output/                 # Hasil klip & log                
├── requirements.txt
└── README.md
```

File `requirements.txt`:
```txt
opencv-python==4.10.0.84
pytesseract==0.3.13
moviepy==1.0.3
```
```bash
pip install -r requirements.txt
```

### 4. Running Program
```bash
python -u main.py
```