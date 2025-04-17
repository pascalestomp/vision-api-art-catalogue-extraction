
📚 TXT to Excel: Structured Data Extraction from OCR Using OpenAI GPT

This script automates the transformation of raw OCR-extracted text (from a historical exhibition catalogue) 
into a structured tabular format saved as an Excel file. The process involves parsing unstructured `.txt` files 
and leveraging OpenAI’s GPT-4-turbo model to extract relevant metadata into a consistent schema.

🧠 Process Summary:
1. **Text Input**:
   - The script begins by reading a `.txt` file containing OCR-extracted text from a scanned catalogue.
   - The file path is defined by `TEXT_FILE_PATH`.

2. **Chunking for API Compatibility**:
   - Because of token limitations in the OpenAI API, the raw text is split into manageable chunks 
     (default: 4,000 characters) using the `textwrap` module.
   - Each chunk is processed independently.

3. **Prompt Engineering & LLM Formatting**:
   - For each chunk, a carefully engineered prompt is constructed, instructing GPT-4 to extract and 
     format the data as CSV according to a predefined column structure.
   - The prompt includes entity formatting rules, examples, and fallback behaviors (e.g., handling unknown data).

4. **DataFrame Assembly**:
   - The CSV text response from each chunk is parsed into a pandas DataFrame.
   - All chunks are combined into one final DataFrame and sorted by Entry Number.
   - Missing or "unknown" entry numbers are automatically inferred based on their order.

5. **Excel Export**:
   - The cleaned and structured data is exported as an `.xlsx` file using `pandas.to_excel()`.

🧩 Output Format (Columns):
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

⚠️ Known Limitations:
- **Character confusion**: The OCR often misreads characters (e.g., lowercase “l”, uppercase “I”, and the number “1”), 
  leading to errors in names and numbers.
- **LLM misinterpretation**: Phrases like “idem” or “dezelfde” can be misunderstood by the LLM, resulting in missing or 
  duplicated artist names.
- **Formatting consistency**: GPT output may occasionally deviate from expected CSV formatting, which could cause row misalignment.
- **Entity omission**: Not all entities are captured—especially in long catalogues—due to chunk boundaries or vague entry formatting.

💡 Notes:
- This approach is ideal for extracting structured data from historical text when the number of categories (columns) 
  is relatively small.
- When it comes to optimizing output quality, **prompt engineering** plays a critical role and should be treated 
  as a flexible and evolving component of the pipeline.

🚀 Dependencies:
- `openai` – for accessing GPT-4
- `pandas` – for data handling and Excel export
- `openpyxl` – as the Excel writer engine for `.xlsx` output

This script represents a hybrid approach where traditional OCR is combined with generative AI to tackle the 
nuanced task of historical data structuring.

