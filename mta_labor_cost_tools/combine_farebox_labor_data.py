import os
import pandas as pd
from tqdm import tqdm

base_path = os.path.expanduser("~/Downloads/Hurricane Sandy Financials/excel outputs")
farebox_path = os.path.join(base_path, "farebox_revenue_2010_2023.xlsx")
labor_path = os.path.join(base_path, "labor_to_debt_percentages.xlsx")
output_path = os.path.join(base_path, "labor_vs_farebox_combined.xlsx")

print("📂 Loading Excel files...")
df_farebox = pd.read_excel(farebox_path)
df_labor = pd.read_excel(labor_path)

df_farebox.columns = [col.strip() for col in df_farebox.columns]
df_labor.columns = [col.strip() for col in df_labor.columns]

print("Merging data on 'Year'...")
df_combined = pd.merge(df_farebox, df_labor, on="Year", how="inner")

df_combined = df_combined.rename(columns={
    "Farebox Revenue ($M)": "Farebox Revenue ($M)",
    "Total Labor Expenses ($M)": "Labor Expense ($M)"
})

df_combined.to_excel(output_path, index=False)
print(f"\n Combined file saved to: {output_path}")
