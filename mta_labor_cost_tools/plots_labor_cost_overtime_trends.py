import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

# === Calculate Overtime % ===
df_wide['Overtime_Pct'] = df_wide['Overtime'] / df_wide['Total labor expenses'] * 100

# === Style ===
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'axes.edgecolor': 'gray',
    'axes.linewidth': 1
})

x_ticks = list(range(2010, 2024))  # Include 2023 for x-axis

# === Plot 1: Overtime % ===
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(df_wide['Year'], df_wide['Overtime_Pct'], color='#0039A6', linewidth=2.5, marker='o', markersize=6)
ax1.fill_between(df_wide['Year'], df_wide['Overtime_Pct'], color='#0039A6', alpha=0.1)

ymin1, ymax1 = 4, 12
ax1.vlines(2012, ymin1, ymin1 + 0.8 * (ymax1 - ymin1), color='crimson', linestyle='--', linewidth=1.5, label='Hurricane Sandy (2012)')
ax1.axvspan(2020, 2022, color='#F7C6C6', alpha=0.4, label='COVID-19 (2020–2022)')
ax1.set_title('MTA Overtime as % of Total Labor')
ax1.set_ylabel('Overtime (%)')
ax1.set_xlabel('Year')
ax1.legend(loc='upper left', frameon=False)
ax1.set_ylim(ymin1, ymax1)
ax1.set_xticks(x_ticks)
ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
ax1.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
fig1.text(0.99, 0.01, 'Data source: MTA annual financials', ha='right', va='bottom', fontsize=9, color='gray')
plt.savefig(os.path.join(output_folder, 'mta_overtime_percent_trend.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig1)

# === Plot 2: Total Labor Cost ===
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(df_wide['Year'], df_wide['Total labor expenses'], color='#2ca02c', linewidth=2.5, marker='o', markersize=6)
ax2.fill_between(df_wide['Year'], df_wide['Total labor expenses'], color='#2ca02c', alpha=0.1)
ymin2, ymax2 = 7000, 14000
ax2.vlines(2012, ymin2, ymin2 + 0.8 * (ymax2 - ymin2), color='crimson', linestyle='--', linewidth=1.5, label='Hurricane Sandy (2012)')
ax2.axvspan(2020, 2022, color='#F7C6C6', alpha=0.4, label='COVID-19 (2020–2022)')
ax2.set_title('MTA Total Labor Cost by Year')
ax2.set_ylabel('Total Labor Cost ($ Millions)')
ax2.set_xlabel('Year')
ax2.legend(loc='upper left', frameon=False)
ax2.set_ylim(ymin2, ymax2)
ax2.set_xticks(x_ticks)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
ax2.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
fig2.text(0.99, 0.01, 'Data source: MTA annual financials', ha='right', va='bottom', fontsize=9, color='gray')
plt.savefig(os.path.join(output_folder, 'mta_total_labor_cost_trend.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig2)
