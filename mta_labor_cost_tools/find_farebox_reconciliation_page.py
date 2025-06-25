import os
import pdfplumber

# Path to your folder
folder_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials")

# Loop through each PDF file
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            found = False

            for i in range(max(0, total_pages - 50), total_pages):
                text = pdf.pages[i].extract_text()
                if text:
                    if "Farebox revenue" in text and "RECONCILIATION BETWEEN FINANCIAL PLAN" in text:
                        print(f"{filename}: match found on page {i + 1}")
                        found = True
                        break

            if not found:
                print(f"{filename}: no match found in last 50 pages")
