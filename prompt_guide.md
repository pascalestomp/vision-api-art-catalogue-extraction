# 🧠 Prompt Logic Summary

This guide summarizes how the Vision API is prompted to extract structured data from historical Dutch art catalogues.

---

## 🎨 Artist Information

- **Format**: Artist name appears first, often with surname first and initials/titles after (e.g., VAN GOGH, J. H.).
- **Goal format**: First name or initials + infix (if any) + surname → `e.g., J. H. van Gogh`
- **Location**:
  - Split by comma: `City, Address`
  - If no address → `Artist Address = unknown`
- **Abbreviations**:
  - Extract known codes (GL, BL, KL, M, BM, etc.) if found near the name or location.
  - Normalize: e.g., `B. L.` → `BL`

---

## 🖼️ Artwork Entries

- Each entry starts with an **entry number** under the artist name.
- Next line is the **title** of the artwork → stored as `Free Title`
- Extra info in **parentheses**, indented, or stylized text → `Additional Artwork Info`
- **Asterisk (*)** present? → Set `Asterisk = true`, else `false`

---

## 💰 Price Matching

- Price list is usually at the beginning or end of the catalogue.
- Recognize by Dutch keywords: “Lijst”, “Prijzen”
- Match entry numbers between artwork and price list.
- Format:
  - Amount Type: `"Asking Price"`
  - Currency:
    - `f` = florin, `m` = mark
    - `""` (double quotes) means inherit currency from row above
  - Price = numeric or worded value

---

## 🧾 Full Entry Text

- Store the full extracted text in a `Full Entry Quote` column.
- If an artist has multiple artworks, only include the matching entry number.

---

## 🔁 Special Rules

- Words like `"idem"`, `"dito"` mean "same as above" — repeat previous artist’s name and location.
- Entries must follow numerical order; don’t skip numbers.

---

Use this logic to ensure consistent, high-quality parsing across catalogues.
