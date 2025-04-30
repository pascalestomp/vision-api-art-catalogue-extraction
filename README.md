# 🖼️ Art Catalogue Extraction pipelines

This project experimented with and provided three distinct methodologies for extracting and structuring data from historical Dutch art exhibition catalogues. Combining Python, OCR and LLMs (PaddleOCR, OpenAI Vision, DeepSeek-Chat) capabilties. It converts scanned PDF catalogues into clean Excel files, ideal for researchers and archivists.

---

## 🚀 What This Project Does

✅ Turns scanned PDFs of art catalogues into organized Excel files  
✅ Extracts artist names, locations, artwork titles, prices, and more  
✅ Matches prices from the back of the catalogue  
✅ Handles tricky stuff like “idem”, “dito”, missing names  

---
## Pipelines overview

### OpenAI Vision Pipeline

- Input: Scanned PDFs (images)
  
- Process:
  Converts PDFs to images
  Uses GPT-4 Vision for combined OCR and structuring

- Output: Excel (.xlsx) with art metadata
  
- Best for: Quick processing with stable integrated OCR+structuring

### DeepSeek Pipeline (Digital PDFs)

- Input: Digital PDFs (with extractable text)
  
- Process:
  Extracts text directly using PyMuPDF
  Splits text into chunks for LLM processing
  Uses DeepSeek-Chat API for structuring

- Output: Excel (.xlsx) with art metadata

- Best for: Clean digital documents where text extraction is reliable and cost effectiveness

### OCR + LLM Pipeline (PaddleOCR + OpenAI/DeepSeek)

- Input: Scanned PDFs (images)

- Process:
  Uses PaddleOCR to extract text from images
  Splits text into chunks for LLM processing
  Leverages OpenAI GPT-4-turbo or DeepSeek-Chat to structure data

- Output: Excel (.xlsx) with art metadata

- Best for: Poor quality scans where direct text extraction isn't possible
  
---
## 🛠 Tools Used
### Vision Pipeline
- Python
- OpenAI GPT-4 Vision API
- PaddleOCR
- PyMuPDF (PDF to image)
- Base64
- Pandas
- Openpyxl

### DeepSeek Pipeline
- Python
- DeepSeek-Chat API (OpenAI-compatible)
- OpenAI
- PyMuPDF
- Pandas
- TQDM

### OCR + LLM Pipeline
- Python
- PaddleOCR
- pdf2image
- opencv-python
- Pillow
- OpenAI
- Textwrap
---

## 📁 Folder Structure

vision-api-art-catalogue-extraction/  
├── main.py → Python script to run the Vision extraction & structuring

├── requirements.txt → List of Python packages

├── prompts/ → Prompt rules and notes

├── deepseek_pipeline.py → Python script to run deepseek extraction & structuring

├── paddle_ocr_rawtext → Python script for text extraction

├── OCR_LLMS → Python script for structuring

├── data/  
│   ├── input/ → PDF catalogues  
│   └── output/ → Excel result files  
└── docs/ → Thesis and methodology info  

## 📁 Folder Structure OpenAI API 

vision_api_code/  
├── main.py                → Main script to run the extraction  
├── requirements.txt       → Python dependencies  
│
├── pdfs/                  → Input PDF catalogues  
├── images/                → Converted images from PDFs  
├── output/                → Extracted Excel files  

---

## 🧪 How to Run It

1. Clone the repo:
```
git clone https://github.com/pascalestomp/vision-api-art-catalogue-extraction.git
cd vision-api-art-catalogue-extraction
```
### Vision Pipeline

2. Install the required packages:
```
pip install -r requirements.txt
```
3. Mount your own API Key and adjust folder paths.
   
4. Run the script:
```
python main.py
```

### DeepSeek Pipeline

2. Mount your own API Key locally.
   
3. Adjust the script to your own folder paths.
   
4. Run the script:
```
deepseek_pipeline.py
```

### OCR + LLM Pipeline
**OCR**

2. Adjust file paths and run the script:
```
paddle_ocr_rawtext
```
**Structuring LLM**

3. Mount your own API Key.
  
4. Adjust script to own folder paths and preferred LLM Model (Deepseek or OpenAI)
     
5. Run the script:
```
OCR_LLMs
```
---

## 📝 Outputs

### Vision Pipeline
An Excel file with:
- Catalogue ID
- Entry number
- Artist Name
- Place
- Artwork Title
- Asterisk (yes/no)
- Currency
- Price (matched if available)
- Additonal info
- Full entry Quote

### Deepseek Pipeline
An Excel file with:
- Catalogue Identifier
- Keyword Person  
- Artist City  
- Artist Address
- Artist Abbreviations  
- Entry Number 
- Free Title  
- Additional Artwork Info  
- Asterisk *(boolean: true/false)*  
- Amount Type  
- Currency 
- Price 
- Full Entry Quote

### OCR + LLM Pipeline
1. A txt file with raw text
2. An Excel file with:
   - Catalogue Identifier
   - Keyword Person
   - Artist City
   - Artist Address
   - Entry Number
   - Free Title
   - Additional Artwork Info
   - Asterisk
   - Amount Type
   - Currency
   - Price
   - Full Entry Quote

---

## 💖 Made by

Pascale, Yagmur, Marianiki, Ava, RKD, DeepSeek and GPT-4.


