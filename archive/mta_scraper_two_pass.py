import os
import pdfplumber
import re
import json

folder_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials")
output_path = os.path.join(folder_path, "farebox_page_map.json")

page_map = {}

for filename in sorted(os.listdir(folder_path)):
    if filename.lower().endswith(".pdf"):
        year_match = re.findall(r"\d{4}", filename)
        if not year_match:
            continue
        year = int(year_match[0])
        pdf_path = os.path.join(folder_path, filename)
        print(f"🔍 Searching in {filename}...")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                search_range = min(34, total_pages)
                target_page = None

                for offset in range(search_range):
                    i = total_pages - 1 - offset
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text and "Farebox revenue" in text:
                        target_page = i
                        break

                if target_page is not None:
                    page_map[year] = target_page
                    print(f"    ✅ Found on page {target_page + 1}")
                else:
                    print(f"    ⚠️  'Farebox revenue' not found")

        except Exception as e:
            print(f"    ❌ Error with {filename}: {e}")

# Save as JSON
with open(output_path, "w") as f:
    json.dump(page_map, f)

print(f"\n📄 Saved page map to: {output_path}")
