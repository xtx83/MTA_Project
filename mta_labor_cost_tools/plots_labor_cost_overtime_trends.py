import pandas as pd
import matplotlib.pyplot as plt
import os

# === File paths ===
base_folder = '/Users/asim/Downloads/Hurricane Sandy Financials'
excel_path = os.path.join(base_folder, 'excel outputs', 'mta_labor_expenses_final.xlsx')
output_folder = os.path.join(base_folder, 'visualizations')
os.makedirs(output_folder, exist_ok=True)

# === Load data ===
df = pd.read_excel(excel_path)
df.columns = df.columns.str.strip()

# === Pivot to wide format ===
df_wide = df.pivot(index='Year', columns='Item', values='Financial Plan Actual')
df_wide = df_wide.rename(columns=lambda x: x.strip())
df_wide.reset_index(inplace=True)

# === Check required columns ===
if 'Overtime' not in df_wide.columns or 'Total labor expenses' not in df_wide.columns:
    raise ValueError("Missing 'Overtime' or 'Total labor expenses' column in pivoted data.")

# === Calculate Overtime % ===
df_wide['Overtime_Pct'] = df_wide['Overtime'] / df_wide['Total labor expenses'] * 100

# === Set up plots ===
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# --- Plot 1: Overtime % (All Years) ---
axs[0].plot(df_wide['Year'], df_wide['Overtime_Pct'], marker='o')
axs[0].axvline(x=2012, color='red', linestyle='--', label='Hurricane Sandy (2012)')
axs[0].axvspan(2020, 2022, color='gray', alpha=0.3, label='COVID-19 (2020–2022)')
axs[0].set_title('Overtime as % of Total Labor (All Years)')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Overtime %')
axs[0].legend()
axs[0].grid(True)

# --- Plot 2: Total Labor Cost ---
axs[1].plot(df_wide['Year'], df_wide['Total labor expenses'], marker='o')
axs[1].axvline(x=2012, color='red', linestyle='--', label='Hurricane Sandy (2012)')
axs[1].axvspan(2020, 2022, color='gray', alpha=0.3, label='COVID-19 (2020–2022)')
axs[1].set_title('Total Labor Cost by Year')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Total Labor Cost')
axs[1].legend()
axs[1].grid(True)

# === Save and show ===
plt.tight_layout()
output_file = os.path.join(output_folder, 'mta_overtime_vs_total_labor_trends.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.close()  # <- prevents freezing or manual interruption

