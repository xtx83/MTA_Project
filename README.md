# MTA_Project
Python scripts to extract and analyze MTA labor cost metrics from financial PDFs and other MTA documents: analyzing labor expense effects caused by crises such as Hurricane Sandy and COVID-19 Pandemic.

# MTA Labor Cost Analysis 

This repository contains Python scripts to extract and analyze **MTA labor cost metrics** from financial PDFs and other MTA documents. The project focuses on understanding how **major crises** such as **Hurricane Sandy** and the **COVID-19 pandemic** affected the agency’s payroll structure, overtime costs, contract settlements, and overall labor spending.

## Objective

To automate the extraction of key labor-related metrics from unstructured financial documents and transform them into structured data that can support deeper trend analysis, visualization, and policy insight.

This project also tests the hypothesis that major operational crises (such as Hurricane Sandy and the COVID-19 pandemic) increase the unpredictability of MTA labor costs. These cost spikes are often driven by overtime pay, hazard pay, and large retroactive payments issued once delayed union contracts are eventually settled. As a result, the MTA is frequently forced to draw down reserve funds at high volumes, compromising its overall credit health.

---

## What It Does

- Parses annual MTA financial reports in PDF format
- Identifies and extracts relevant metrics such as:
  - Total Payroll
  - Overtime Pay
  - Labor Costs
  - Retroactive Pay
  - Contract Settlements
  - Reserve Usage
- Outputs a clean `.xlsx` spreadsheet of all matches for further analysis

---

## Stack

- Python 3
- [`pdfplumber`](https://github.com/jsvine/pdfplumber) – for parsing PDF texts
- `pandas` – for structuring and exporting data
- `openpyxl` – for excel output

---

## Usage

### 1. Install dependencies:
```bash
pip install pdfplumber pandas openpyxl
