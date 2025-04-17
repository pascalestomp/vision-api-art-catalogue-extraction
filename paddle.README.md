# 🖼️ OCR Extraction Pipeline for Exhibition Catalogues

This project contains a Python script that uses **PaddleOCR** to extract text from scanned 19th-century Dutch exhibition catalogues. The goal is to convert PDF pages into clean, readable `.txt` files, which can later be structured into Excel or database-ready formats.

---

## 🚀 How It Works

**Input:** Scanned PDF of a catalogue (often a double-page spread)  
**Output:** `.txt` file containing extracted raw text (ordered by left/right pages)

---

## 🧩 Process Overview

```mermaid
flowchart LR
  A[PDF File] --> B[pdf2image Conversion]
  B --> C[Split Double Page]
  C --> D[OpenCV Image Read]
  D --> E[PaddleOCR Text Extraction]
  E --> F[Merge + Organize Text]
  F --> G[Save to .txt File]
```

---


## 🔧 Requirements

Install the following Python libraries before running the script:

```bash
pip install paddleocr paddlepaddle pdf2image opencv-python Pillow
```

> ⚠️ You may also need to install [Poppler](https://github.com/oschwartz10612/poppler-windows) for `pdf2image` to work (especially on Windows).

---

## 📂 How to Use

1. Add your PDF file (e.g., `catalogue.pdf`) to the project directory.
2. In your script, replace the `name.pdf` with the name of your file.
3. Run the script:

```bash
python paddle_ocr_extractor.py
```

4. The extracted text will be saved in a `.txt` file with the same base name as your PDF.

---

## 🧠 What This Script Does

- Converts each page of the PDF into an image
- Splits double-page spreads into two separate pages
- Uses **PaddleOCR (Dutch model)** to extract printed text from each half
- Merges the text in reading order (Left → Right)
- Saves the result as a plain `.txt` file



## 👥 Authors

- Yagmur, Pascale, Marianiki, Ava
