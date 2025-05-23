pip install pandas tqdm openai PyMuPDF

import os
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from io import StringIO
import fitz

# Initialize DeepSeek client
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the DEEPSEEK_API_KEY environment variable.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"  # DeepSeek API base URL
)
# Define Excel columns
COLUMNS = [
    "Catalogue Identifier", "Keyword Person", "Artist City",
    "Artist Address", "Artist Abbreviations", "Entry Number",
    "Free Title", "Additional Artwork Info", "Asterisk",
    "Amount Type", "Currency", "Price", "Full Entry Quote"
]

def extract_text_from_pdf(pdf_path):
    """Extracts text directly from a PDF file using PyMuPDF."""
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()  # Extract text from each page
        return text.strip()
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return ""

def format_text_into_table(raw_text, pdf_name):
    """Formats extracted text into structured table using DeepSeek."""
    catalogue_identifier = pdf_name
    extracted_data = []
    chunk_size = 3000  # Limit characters per request to avoid API truncation

    # Split the raw text into manageable chunks
    text_chunks = [raw_text[i:i + chunk_size] for i in range(0, len(raw_text), chunk_size)]

    for chunk in text_chunks:
        try:
            prompt = f"""Convert this Dutch exhibition catalog text into a CSV table:
            {chunk}

            Rules:
            - **Catalogue Identifier:** Use `{catalogue_identifier}` for every row.
            - **Artist Name:** Extract the surname first, then first name. If written like:
            - "VAN GOGH, J. H." → Convert to "J. H. Van Gogh"
            - "VAN GOGH (J. H.)" → Convert to "J. H. Van Gogh"
            - **Location:** If separated by a comma, extract before and after the comma as:
            - First part (before comma) → `Artist City`
            - Second part (after comma) → `Artist Address`
            - **Artist Abbreviations:** Extract if present (e.g., "GL, BL, KL, BM"). these are usually found after the artist name or location
            - do not confuse abbreviations with initials
            - **Entry Number:** Extract the **actual number appearing before each line**.
            - **Free Title:** Extract the artwork title after the entry number.
            - **Additional Artwork Info:** If parentheses appear next to the title, store their content here.
            - **Asterisk:** If an asterisk (`*`) appears, store `"true"`, otherwise `"false"`.
            - **Currency & Pricing:**
            - **Full Entry Quote:** Copy the full text of the entry exactly as it appears. Including the related artist information.
            - If a price list is detected, match the entry number to its corresponding price.
            - Extract currency symbols (ƒ, gulden, fl, m, mark, mrk, etc.).
            - If price is `""`, inherit the most recent currency.
            - If no price list, store `"unknown"` for Amount Type, Currency, and Price.
            - fill empty cells with "unknown"
            - assume entries like 'idem', 'deselfde', 'dezelfde', 'dito', '"' mean same as above.
            - assume Amount Type is always "Asking price"
            - correct typos automatically
            - Output **only** the CSV table. No explanations or formatting outside of CSV.
            - Always include header row: {','.join(COLUMNS)}
            """

            response = client.chat.completions.create(
                model="deepseek-chat", #mount preferred model here
                messages=[
                    {"role": "system", "content": "You are a data formatting assistant. Output CSV data only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4000,
                stream=False
            )

            if response.choices[0].message.content:
                formatted_data = response.choices[0].message.content.strip()

                # Optional: Clean unexpected lines (defensive programming)
                csv_lines = [line for line in formatted_data.splitlines() if line.strip() and not line.lower().startswith("here is")]
                formatted_data_cleaned = "\n".join(csv_lines)

                df_chunk = pd.read_csv(StringIO(formatted_data_cleaned), delimiter=",", names=COLUMNS, quotechar='"', on_bad_lines="warn")

                extracted_data.append(df_chunk)

        except Exception as e:
            print(f"❌ Error formatting text chunk from {pdf_name}: {e}")

    # Concatenate all DataFrames from chunks
    if extracted_data:
        return pd.concat(extracted_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=COLUMNS)

def process_pdfs(base_folder):
    """Processes all PDFs in a folder and extracts structured data."""
    extracted_data = []

    for pdf_file in tqdm(os.listdir(base_folder), desc="📁 Processing PDFs"):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(base_folder, pdf_file)
            print(f"\n📄 Processing PDF: {pdf_file}")

            # Extract raw text from PDF
            raw_text = extract_text_from_pdf(pdf_path)
            if not raw_text:
                print(f"⚠️ No text extracted from {pdf_file}")
                continue

            # Format text into structured table
            df_entries = format_text_into_table(raw_text, pdf_file)
            if not df_entries.empty:
                extracted_data.append(df_entries)

    # Combine all data into one DataFrame
    final_df = pd.concat(extracted_data, ignore_index=True) if extracted_data else pd.DataFrame(columns=COLUMNS)

    # Save extracted data to Excel
    if not final_df.empty:
        output_file = "__.xlxs" #input name of output file
        final_df.to_excel(output_file, index=False)
        print(f"\n✅ Extraction complete! Data saved to {output_file}")
    else:
        print("❌ No data extracted! Check API responses.")

# Run the process
if __name__ == "__main__":
    BASE_FOLDER = r"" #input folder file path
    process_pdfs(BASE_FOLDER)
