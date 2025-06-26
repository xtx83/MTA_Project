import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/Users/asim/Downloads/Hurricane Sandy Financials/excel outputs/labor_vs_farebox_combined.xlsx")

df["Labor Indexed"] = df["Total labor expenses"] / df["Total labor expenses"].iloc[0] * 100
df["Farebox Indexed"] = df["Farebox Revenue ($M)"] / df["Farebox Revenue ($M)"].iloc[0] * 100

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.plot(
    df["Year"],
    df["Labor Indexed"],
    label="Labor Expense (2010 = 100)",
    color="#285cab",
    linewidth=2.5,
    marker="o"
)

ax.plot(
    df["Year"],
    df["Farebox Indexed"],
    label="Farebox Revenue (2010 = 100)",
    color="black",
    linewidth=2.5,
    marker="o"
)

ax.axvspan(2020, 2021, color="#eebebe", alpha=0.3, label="COVID-19 (2020–2021)")

plt.text(
    0.5,
    1.06,
    "Labor Cost vs. Farebox Revenue",
    fontsize=18,
    fontweight="bold",
    ha="center",
    transform=ax.transAxes
)

plt.text(
    0.5,
    1.02,
    "Growth Since 2010 Baseline — Indexed values show % change from 2010 (set to 100)",
    fontsize=12,
    ha="center",
    transform=ax.transAxes
)

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Indexed Value", fontsize=12)
ax.set_xticks(df["Year"])

ax.grid(True, axis="y", linestyle="--", linewidth=0.7, color="#ccc", alpha=0.8)
ax.legend(loc="upper left", frameon=False)

plt.figtext(
    0.99,
    0.01,
    "Data source: MTA annual financials",
    ha="right",
    fontsize=9,
    color="gray"
)

plt.tight_layout(rect=[0, 0.03, 1, 0.88])
plt.savefig("/Users/asim/Downloads/Hurricane Sandy Financials/excel outputs/labor_vs_farebox_indexed_FINAL.png", dpi=300)
plt.show()
