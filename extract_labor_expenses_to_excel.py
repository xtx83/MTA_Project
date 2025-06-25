import os
import pdfplumber
import pandas as pd

# === CONFIGURATION ===
base_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials")
output_folder = os.path.join(base_path, "excel outputs")
os.makedirs(output_folder, exist_ok=True)

page_map = {
    "2010": 108,
    "2011": 123,
    "2012": 121,
    "2013": 120,
    "2014": 123,
    "2015": 148,
    "2016": 139,
    "2017": 122,
    "2018": 127,
    "2019": 133,
    "2020": 142,
    "2021": 144,
    "2022": 147,
    "2023": 156
}

target_labels = [
    "Payroll",
    "Overtime",
    "Health and welfare",
    "Pensions",
    "Other fringe benefits",
    "Postemployment benefits",
    "Reimbursable overhead",
    "Total labor expenses"
]

output_data = []

for filename in sorted(os.listdir(base_path)):
    if filename.endswith(".pdf"):
        year = filename.split(".")[0]
        file_path = os.path.join(base_path, filename)

        if year not in page_map:
            continue

        print(f"🔍 Processing {filename} (page {page_map[year]})...")
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[page_map[year] - 1]
            words = page.extract_words(x_tolerance=2, keep_blank_chars=True, use_text_flow=True)

            for label in target_labels:
                label_words = [w for w in words if w["text"].strip() == label]
                if not label_words:
                    continue

                label_word = label_words[0]
                label_y = label_word["top"]
                label_x = label_word["x1"]

                # Find numeric words on same line (±3 pts), and to the right of label
                number_candidates = [
                    w for w in words
                    if abs(w["top"] - label_y) <= 3 and w["x0"] > label_x and any(c.isdigit() for c in w["text"])
                ]

                if number_candidates:
                    # Sort left to right, pick first valid number
                    number_candidates.sort(key=lambda w: w["x0"])
                    for w in number_candidates:
                        raw = w["text"].replace(",", "").replace("(", "-").replace(")", "")
                        try:
                            value = float(raw)
                            output_data.append({
                                "Year": year,
                                "Item": label,
                                "Financial Plan Actual": value
                            })
                            break
                        except ValueError:
                            continue

# === EXPORT TO EXCEL ===
if output_data:
    df = pd.DataFrame(output_data)
    output_path = os.path.join(output_folder, "mta_labor_expenses_final.xlsx")
    df.to_excel(output_path, index=False)
    print(f"\n✅ Data saved to: {output_path}")
else:
    print("\n⚠️ No data extracted.")
