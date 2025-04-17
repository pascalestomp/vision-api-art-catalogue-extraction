
# 🖼️ Dutch Art Catalogue PDF Extraction Pipelines

This project provides **two different pipelines** to extract structured data from scanned or digital Dutch art catalogues and export them into clean Excel sheets. These tools assist archivists, researchers, and historians by simplifying the cataloguing of artwork data.

---

## 🧭 Overview of Both Pipelines

| Feature                                | OpenAI Vision Pipeline                                  | DeepSeek AI Pipeline                                       |
|----------------------------------------|----------------------------------------------------------|-------------------------------------------------------------|
| 📚 Input Format                         | **Scanned PDFs** (images)                                | **Digital PDFs** (with extractable text)                    |
| 🧠 AI Model Used                        | OpenAI GPT-4 Vision                                      | DeepSeek-Chat API (OpenAI-compatible)                       |
| 📄 PDF Handling                         | Converts PDFs to images, uses OCR                        | Extracts text directly using PyMuPDF                        |
| 📤 Output Format                        | Excel `.xlsx`                                            | Excel `.xlsx`                                               |
| 📦 Libraries Used                       | `paddleocr`, `openai`, `PyMuPDF`, `pandas`, `openpyxl`   | `PyMuPDF`, `pandas`, `tqdm`, `openai` (for DeepSeek)       |
| 🧩 Special Handling                     | Deals with "idem", "dito", missing names using vision    | Deals with same tokens + currency parsing & abbreviations  |
| 🔑 API Key Needed                      | OpenAI                                                   | DeepSeek (set as `DEEPSEEK_API_KEY`)                       |
| 🧪 Output Fields (Examples)            | Catalogue ID, Artist, Title, Place, Price, etc.          | Artist City, Address, Entry Number, Title, Price, etc.     |
| 🔍 Parsing Strategy                    | Vision → OCR → AI for structure                          | Text chunks → DeepSeek CSV → DataFrame merge               |

---

## 🛠 Tools Used

### Vision Pipeline
- Python
- OpenAI GPT-4 Vision API
- PaddleOCR
- PyMuPDF
- Pandas
- Base64
- Openpyxl

### DeepSeek Pipeline
- Python
- DeepSeek-Chat API (OpenAI-compatible)
- PyMuPDF
- Pandas
- TQDM

---

## 📁 Folder Structure (OpenAI Vision)

```
vision-api-art-catalogue-extraction/  
├── main.py → Python script to run the extraction  
├── requirements.txt → List of Python packages  
├── prompts/ → Prompt rules and notes  
├── data/  
│   ├── input/ → PDF catalogues  
│   └── output/ → Excel result files  
└── docs/ → Thesis and methodology info  
```

---

## 🧪 Running the Pipelines

### 🔷 OpenAI Vision Pipeline

1. **Install Dependencies**  
```bash
pip install -r requirements.txt
```

2. **Run**  
```bash
python main.py
```

3. **Expected Output**  
Excel file in `/data/output` with the following columns:
- Catalogue ID  
- Entry Number  
- Artist Name  
- Place  
- Artwork Title  
- Asterisk (yes/no)  
- Currency  
- Price (matched if available)  
- Additional Info  
- Full Entry Quote  

---

### 🔶 DeepSeek Pipeline

1. **Install Dependencies**  
```bash
pip install pandas tqdm openai PyMuPDF
```

2. **Set API Key**  
```bash
export DEEPSEEK_API_KEY=your_api_key_here  # or use Windows equivalent
```

3. **Set PDF Folder Path in Script**  
```python
BASE_FOLDER = r"/path/to/your/pdf/folder"
```

4. **Run Script**  
```bash
python your_script_name.py
```

5. **Expected Output**  
The generated Excel file will contain the following **structured columns**:

- **Catalogue Identifier**  
- **Keyword Person**  
- **Artist City**  
- **Artist Address**  
- **Artist Abbreviations**  
- **Entry Number**  
- **Free Title**  
- **Additional Artwork Info**  
- **Asterisk** (boolean: true/false)  
- **Amount Type**  
- **Currency**  
- **Price**  
- **Full Entry Quote**

---

## 💖 Made by  
Pascale, Yagmur, Marianiki, Ava, RKD, GPT-4 & DeepSeek.
