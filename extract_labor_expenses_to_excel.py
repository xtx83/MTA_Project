import os
import pdfplumber
import pandas as pd

# Base folder
base_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials")
output_folder = os.path.join(base_path, "excel outputs")
os.makedirs(output_folder, exist_ok=True)

# Expense labels to extract
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

# Process each PDF
for filename in sorted(os.listdir(base_path)):
    if filename.endswith(".pdf"):
        year = filename.split(".")[0]
        file_path = os.path.join(base_path, filename)
        print(f"🔍 Processing {filename}...")

        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            found = False

            for i in range(max(0, total_pages - 50), total_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                if text and "Farebox revenue" in text and "RECONCILIATION BETWEEN FINANCIAL PLAN" in text:
                    print(f"✅ Match found on page {i + 1}")
                    found = True
                    for line in text.split("\n"):
                        for label in target_labels:
                            if line.strip().startswith(label):
                                split_line = line.strip().split()
                                try:
                                    for j in range(1, len(split_line)):
                                        cleaned = split_line[j].replace(",", "").replace("(", "-").replace(")", "").replace("$", "")
                                        try:
                                            value = float(cleaned)
                                            output_data.append({
                                                "Year": year,
                                                "Item": label,
                                                "Financial Plan Actual": value
                                            })
                                            break
                                        except ValueError:
                                            continue
                                except Exception:
                                    continue
                    break

            if not found:
                print(f"❌ No match found in last 50 pages of {filename}")

# Export to Excel inside 'excel outputs'
if output_data:
    df = pd.DataFrame(output_data)
    output_path = os.path.join(output_folder, "mta_labor_expenses.xlsx")
    df.to_excel(output_path, index=False)
    print(f"\n✅ Data saved to: {output_path}")
else:
    print("\n⚠️ No data extracted.")
