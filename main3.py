import openai
import os
import pandas as pd
from PIL import Image
import base64
from pdf2image import convert_from_path

api_key = #ownapikey
if not api_key:
    raise ValueError("❌ OpenAI API key not found! Set it using 'export OPENAI_API_KEY=your-api-key'")

openai.api_key = api_key

def compress_image(image_path, output_path, quality=30):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality)
        return output_path
    except Exception as e:
        print(f"❌ Error compressing {image_path}: {e}")
        return image_path

def convert_pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path, dpi=300)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    os.makedirs(pdf_output_folder, exist_ok=True)
    image_paths = []
    for i, image in enumerate(images):
        img_path = os.path.join(pdf_output_folder, f"page_{i+1}.jpg")
        image.save(img_path, "JPEG")
        image_paths.append(img_path)
    return pdf_name, image_paths

def gpt_response(image_path, prompt_text):
    compressed_path = "compressed.jpg"
    image_path = compress_image(image_path, compressed_path)
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            temperature=0.2,
            messages=[
                {"role": "system", "content": "Process auction catalogue images and return structured output."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                ]}
            ],
            max_tokens=6000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ API Error for {image_path}: {e}")
        return ""

def extract_artworks_from_text(raw_text):
    lines = raw_text.split("\n")
    artworks = []
    last_artist = ""
    last_place = ""
    last_title = ""
    for line in lines:
        if "|" in line:
            parts = [part.strip() for part in line.split("|")]
            fields = {k.strip(): "unknown" for k in ["Number", "Artist", "Place", "Title", "Asterisk", "Currency", "Price", "Info"]}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    fields[key.strip()] = value.strip()

            if "*" in fields["Number"]:
                fields["Number"] = fields["Number"].replace("*", "").strip()
                fields["Asterisk"] = "true"
            if "*" in fields["Title"]:
                fields["Title"] = fields["Title"].replace("*", "").strip()
                fields["Asterisk"] = "true"

            if fields["Artist"].lower().strip() in ["dezelfde", "idem", "dito"]:
                fields["Artist"] = last_artist
            else:
                last_artist = fields["Artist"]

            if fields["Place"].lower().strip() in ["dezelfde", "idem", "dito"]:
                fields["Place"] = last_place
            else:
                last_place = fields["Place"]

            if fields["Title"].lower().strip() in ["dezelfde", "idem", "dito"]:
                fields["Title"] = last_title
            else:
                last_title = fields["Title"]

            # 🧹 Strong filter: skip if artist or title are missing or fake
            artist_clean = fields["Artist"].strip().lower()
            title_clean = fields["Title"].strip().lower()
            if artist_clean == "unknown" or title_clean == "unknown" or not artist_clean or not title_clean:
                continue

            fields["Full Entry"] = line.strip()
            fields["Price"] = "unknown"
            artworks.append(fields)
    return artworks


def extract_prices_from_text(raw_text):
    prices = {}
    lines = raw_text.split("\n")
    for line in lines:
        if ":" in line and "Price" not in line:
            try:
                number, price = line.split(":", 1)
                prices[number.strip()] = price.strip()
            except:
                continue
    return prices

def process_pdfs(pdf_folder="pdfs", output_excel="extracted_catalogue.xlsx"):
    data = []
    image_output = "images"
    os.makedirs(image_output, exist_ok=True)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"):
            print(f"📂 Found PDF: {pdf_file}")
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_name, image_paths = convert_pdf_to_images(pdf_path, image_output)
            artworks = []
            prices = {}

            prompt_entries = """
            This image contains entries from a 19th-century Dutch art auction catalogue.
            Each entry includes:
            - Number (must always be included)
            - Artist (name)
            - Place (of artist)
            - Title (of the artwork)
            - Currency (ƒ, gulden, fl, etc. — do not skip)
            - Price (if visible)
            - Asterisk (true/false if * is present)
            - Additional Info

            Format each entry like this:
            Number: [X] | Artist: [Name] | Place: [City] | Title: [Text] | Asterisk: [true/false] | Currency: [ƒ] | Price: [Y] | Info: [optional]

            If a value is missing, still include the field with "unknown"
            Replace placeholders like "dezelfde", "idem", or "dito" with the last valid value from above

            Return only structured entries in this format. Do NOT return any commentary or explanations.
            """


            prompt_prices = """
            This image contains a price list from an auction catalogue.
            Extract a mapping of entry number to price.
            Format: [Entry Number]: [Price]
            Return only number: price lines, nothing else.
            """

            for image in image_paths:
                print(f"🖼️ Checking: {os.path.basename(image)}")
                raw = gpt_response(image, prompt_entries)
                artworks.extend(extract_artworks_from_text(raw))

                raw_price = gpt_response(image, prompt_prices)
                price_dict = extract_prices_from_text(raw_price)
                prices.update(price_dict)

            for item in artworks:
                num = item.get("Number", "")
                if num in prices:
                    price_value = prices[num]
                    currency = item.get("Currency", "")
                    if currency.lower() in ["gulden", "ƒ", "fl."]:
                        item["Price"] = f"ƒ{price_value}"
                    else:
                        item["Price"] = price_value

                row = [
                    pdf_name,
                    item.get("Number", "unknown"),
                    item.get("Artist", "unknown"),
                    item.get("Place", "unknown"),
                    item.get("Title", "unknown"),
                    item.get("Asterisk", "unknown"),
                    item.get("Currency", "unknown"),
                    item.get("Price", ""),
                    item.get("Info", "unknown"),
                    item.get("Full Entry", "unknown")
                ]
                data.append(row)

    df = pd.DataFrame(data, columns=["PDF Name", "Number", "Artist", "Place", "Title", "Asterisk", "Currency", "Price", "Additional Info", "Full Entry"])
    df.to_excel(output_excel, index=False)
    print(f"✅ Extraction complete! Data saved to {output_excel} with {len(data)} entries.")

if __name__ == "__main__":
    process_pdfs()




