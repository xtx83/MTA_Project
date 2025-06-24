import os
import re
import pdfplumber
import pandas as pd

# Set paths
folder_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials")
output_path = os.path.join(folder_path, "mta_plan_actuals_only.xlsx")

# Hardcoded page numbers where reconciliation table appears
page_map = {
    2010: 108,
    2011: 123,
    2012: 121,
    2013: 120,
    2014: 123,
    2015: 148,
    2016: 139,
    2017: 122,
    2018: 127,
    2019: 133,
    2020: 142,
    2021: 144,
    2022: 147,
    2023: 156
}

# Pattern to match category and first number column
row_pattern = re.compile(r"^(.*?)\s+(\(?[\d\.,\-]+\)?)\s+(\(?[\d\.,\-]+\)?)$")

def clean_number(val):
    val = val.replace(",", "").strip()
    if val.startswith("(") and val.endswith(")"):
        val = "-" + val[1:-1]
    try:
        return float(val)
    except:
        return None

def clean_label(label):
    return label.strip().replace("  ", " ")

# Collect results
all_data = []

for year, page_num in page_map.items():
    filename = f"{year}.pdf"
    pdf_path = os.path.join(folder_path, filename)
    print(f"📄 Extracting from {filename} (page {page_num + 1})")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_num >= len(pdf.pages):
                print(f"    ⚠️  Page {page_num + 1} out of range for {filename}")
                continue

            page = pdf.pages[page_num]
            text = page.extract_text()
            if not text:
                print(f"    ⚠️  No text on page {page_num + 1}")
                continue

            for line in text.split("\n"):
                match = row_pattern.match(line.strip())
                if match:
                    label, plan_val, _ = match.groups()
                    label = clean_label(label)
                    if any(x in label.lower() for x in ["for the year", "net operating", "category"]):
                        continue
                    all_data.append({
                        "Year": year,
                        "Category": label,
                        "Financial Plan Actual ($M)": clean_number(plan_val)
                    })

    except Exception as e:
        print(f"    ❌ Error with {filename}: {e}")
        continue

# Save to Excel
df = pd.DataFrame(all_data)
df.sort_values(by=["Year", "Category"], inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_excel(output_path, index=False)
a
print(f"\n🎉 Done! Clean Financial Plan data saved to: {output_path}")
