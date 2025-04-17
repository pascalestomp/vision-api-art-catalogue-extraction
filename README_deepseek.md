# 🖼️ Dutch Exhibition Catalogue PDF Parser

This tool extracts and structures data from **Dutch exhibition catalog PDFs** using the **DeepSeek AI API** and formats the information into a structured Excel sheet.

It uses:
- `PyMuPDF` for PDF text extraction
- `pandas` for data handling
- `DeepSeek` (via OpenAI-style API) for intelligent text-to-table conversion

---

## 📦 Requirements

Install the necessary Python packages:

```bash
pip install pandas tqdm openai PyMuPDF
```

---

## 🔐 Environment Setup

Set your DeepSeek API key as an environment variable:

```bash
export DEEPSEEK_API_KEY=your_api_key_here  # On Unix/macOS
# or
set DEEPSEEK_API_KEY=your_api_key_here     # On Windows
```

---

## 📁 Input

Place all your `.pdf` files inside a single directory. These PDFs should be **Dutch exhibition catalogues** with entries like:

```
123. VAN GOGH, J. H., Amsterdam, GL - "Zonnebloemen", ƒ200
```

---

## 📤 Output

The script generates an Excel file (`__.xlxs`) containing structured data with the following columns:

- Catalogue Identifier
- Keyword Person
- Artist City
- Artist Address
- Artist Abbreviations
- Entry Number
- Free Title
- Additional Artwork Info
- Asterisk
- Amount Type
- Currency
- Price
- Full Entry Quote

---

## 🚀 How to Use

Update the last section of the script with the full path to your PDF folder:

```python
BASE_FOLDER = r"/path/to/your/pdf/folder"
```

Then run the script:

```bash
python your_script_name.py
```

Once complete, you'll find an Excel file in the current directory containing the extracted information.

---

## ⚙️ How It Works

1. **PDF Parsing**: Each PDF is opened and text is extracted page by page.
2. **Chunking**: The raw text is split into ~3000 character chunks to avoid API truncation.
3. **AI Formatting**: Each chunk is sent to DeepSeek's API with formatting rules to convert to CSV format.
4. **DataFrame Merge**: All returned CSVs are parsed and merged into a single Excel spreadsheet.

---

## 🛠️ Notes

- Handles edge cases like:
  - `idem`, `"`, `dito` → same as previous
  - Different currency symbols (ƒ, gulden, fl, etc.)
  - Artist abbreviation parsing
  - Asterisk detection (`*` → `true`)
- Outputs "unknown" for missing values.
- Designed for high consistency and low hallucination (temperature = 0.1).

---

## 📌 To Do

- Add GUI for file selection (optional)
- Improve typo correction
- Handle multi-language catalogs
