# 🖼️ Vision API Art Catalogue Extraction

This project extracts structured data from historical Dutch art catalogues using OpenAI Vision, OCR, and Python. It converts scanned PDF catalogues into clean Excel files, ideal for researchers and archivists.

---

## 🚀 What This Project Does

✅ Turns scanned PDFs of art catalogues into organized Excel files  
✅ Extracts artist names, locations, artwork titles, prices, and more  
✅ Matches prices from the back of the catalogue  
✅ Handles tricky stuff like “idem”, “dito”, missing names  

---

## 🛠 Tools Used

- Python
- OpenAI GPT-4 Vision API
- PaddleOCR
- PyMuPDF (PDF to image)
- Base64
- Pandas
- Openpyxl

---

## 📁 Folder Structure

vision-api-art-catalogue-extraction/  
├── main.py → Python script to run the extraction  
├── requirements.txt → List of Python packages  
├── prompts/ → Prompt rules and notes  
├── data/  
│   ├── input/ → PDF catalogues  
│   └── output/ → Excel result files  
└── docs/ → Thesis and methodology info  

---

## 🧪 How to Run It

1. Clone the repo:
```
git clone https://github.com/pascalestomp/vision-api-art-catalogue-extraction.git
cd vision-api-art-catalogue-extraction
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the script:
```
python main.py
```

---

## 📝 Outputs

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

---

## 💖 Made by

Pascale, Yagmur, Marianiki, Ava RKD, and GPT-4.


