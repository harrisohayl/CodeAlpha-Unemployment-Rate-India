"""
India Unemployment Analysis
----------------------------
Cleans, explores, and visualizes unemployment data across Indian states,
examines the COVID-19 shock, and surfaces seasonal / regional patterns.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120

CHARTS = "../charts"

# ---------------------------------------------------------------
# 1. LOAD & CLEAN
# ---------------------------------------------------------------
df1 = pd.read_csv("../data/Unemployment_in_India.csv")
df2 = pd.read_csv("../data/Unemployment_Rate_upto_11_2020.csv")

for df in (df1, df2):
    df.columns = df.columns.str.strip()

rename_map = {
    "Estimated Unemployment Rate (%)": "unemployment_rate",
    "Estimated Employed": "employed",
    "Estimated Labour Participation Rate (%)": "labour_participation_rate",
    "Region": "state",
    "Date": "date",
    "Frequency": "frequency",
    "Area": "area",
}
df1 = df1.rename(columns=rename_map)
df2 = df2.rename(columns=rename_map)

# df2 has a duplicate "Region" column used for zone (South/North/etc) + lat/long
df2 = df2.rename(columns={df2.columns[6]: "zone"})

for df in (df1, df2):
    df["state"] = df["state"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"].astype(str).str.strip(), format="%d-%m-%Y")

# Drop fully-empty rows (df1 has 28 blank rows)
df1 = df1.dropna(subset=["unemployment_rate"]).copy()

# Dataset 1 only runs Jan-2019 to Oct-2020 (its Feb 2020 entry above is a data artifact
# from a single row) -- keep as-is, just sort
df1 = df1.sort_values("date")
df2 = df2.sort_values("date")

df1["month"] = df1["date"].dt.month
df1["month_name"] = df1["date"].dt.strftime("%b")
df1["year"] = df1["date"].dt.year

print("Dataset 1 (state-level, Rural/Urban split):", df1.shape, df1["date"].min().date(), "to", df1["date"].max().date())
print("Dataset 2 (state-level, up to Nov-2020, with zone):", df2.shape, df2["date"].min().date(), "to", df2["date"].max().date())
print("States covered:", df1["state"].nunique())

df1.to_csv("../data/cleaned_unemployment_in_india.csv", index=False)
df2.to_csv("../data/cleaned_unemployment_upto_nov2020.csv", index=False)

# ---------------------------------------------------------------
# 2. NATIONAL TREND OVER TIME (highlighting COVID)
# ---------------------------------------------------------------
national = df1.groupby("date", as_index=False)["unemployment_rate"].mean()

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(national["date"], national["unemployment_rate"], marker="o", color="#2563eb", linewidth=2)
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"), color="red", alpha=0.12, label="National Lockdown (Mar–May 2020)")
ax.set_title("India: Average Estimated Unemployment Rate Over Time", fontsize=14, weight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Unemployment Rate (%)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))
ax.legend()
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(f"{CHARTS}/01_national_trend_covid.png")
plt.close()

# ---------------------------------------------------------------
# 3. COVID IMPACT: PRE vs DURING vs POST
# ---------------------------------------------------------------
def covid_phase(d):
    if d < pd.Timestamp("2020-03-25"):
        return "Pre-COVID"
    elif d <= pd.Timestamp("2020-05-31"):
        return "Lockdown (Mar-May 2020)"
    else:
        return "Post-Lockdown Recovery"

df1["covid_phase"] = df1["date"].apply(covid_phase)
phase_summary = (
    df1.groupby("covid_phase", as_index=False)["unemployment_rate"]
    .mean()
    .assign(order=lambda d: d["covid_phase"].map({"Pre-COVID": 0, "Lockdown (Mar-May 2020)": 1, "Post-Lockdown Recovery": 2}))
    .sort_values("order")
)
print("\nCOVID Phase Averages:\n", phase_summary[["covid_phase", "unemployment_rate"]])

fig, ax = plt.subplots(figsize=(8, 5.5))
colors = ["#22c55e", "#ef4444", "#f59e0b"]
bars = ax.bar(phase_summary["covid_phase"], phase_summary["unemployment_rate"], color=colors)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.1f}%", ha="center", fontsize=11, weight="bold")
ax.set_title("Unemployment Rate: Pre-COVID vs Lockdown vs Recovery", fontsize=14, weight="bold")
ax.set_ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig(f"{CHARTS}/02_covid_phase_comparison.png")
plt.close()

# ---------------------------------------------------------------
# 4. TOP / BOTTOM STATES DURING LOCKDOWN PEAK
# ---------------------------------------------------------------
peak_month = df1[(df1["date"] >= "2020-04-01") & (df1["date"] <= "2020-04-30")]
state_peak = peak_month.groupby("state", as_index=False)["unemployment_rate"].mean().sort_values("unemployment_rate", ascending=False)

fig, ax = plt.subplots(figsize=(9, 8))
top15 = state_peak.head(15)
ax.barh(top15["state"][::-1], top15["unemployment_rate"][::-1], color="#dc2626")
ax.set_title("Top 15 States by Unemployment Rate — April 2020 (COVID Peak)", fontsize=13, weight="bold")
ax.set_xlabel("Unemployment Rate (%)")
plt.tight_layout()
plt.savefig(f"{CHARTS}/03_top_states_covid_peak.png")
plt.close()

# ---------------------------------------------------------------
# 5. RURAL VS URBAN COMPARISON
# ---------------------------------------------------------------
area_trend = df1.dropna(subset=["area"]).groupby(["date", "area"], as_index=False)["unemployment_rate"].mean()

fig, ax = plt.subplots(figsize=(11, 5.5))
for area, grp in area_trend.groupby("area"):
    ax.plot(grp["date"], grp["unemployment_rate"], marker="o", label=area, linewidth=2)
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"), color="red", alpha=0.10)
ax.set_title("Rural vs Urban Unemployment Rate Over Time", fontsize=14, weight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Unemployment Rate (%)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))
ax.legend()
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(f"{CHARTS}/04_rural_vs_urban.png")
plt.close()

rural_urban_gap = area_trend.pivot(index="date", columns="area", values="unemployment_rate")
rural_urban_gap["gap_urban_minus_rural"] = rural_urban_gap["Urban"] - rural_urban_gap["Rural"]
print("\nAvg Rural vs Urban unemployment:\n", area_trend.groupby("area")["unemployment_rate"].mean())

# ---------------------------------------------------------------
# 6. SEASONAL PATTERN (month-of-year, pre-COVID only to avoid distortion)
# ---------------------------------------------------------------
pre_covid = df1[df1["date"] < "2020-03-01"]
seasonal = pre_covid.groupby("month", as_index=False)["unemployment_rate"].mean().sort_values("month")
month_labels = [pd.Timestamp(2019, m, 1).strftime("%b") for m in seasonal["month"]]

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(month_labels, seasonal["unemployment_rate"], marker="o", color="#7c3aed", linewidth=2.5)
ax.fill_between(month_labels, seasonal["unemployment_rate"], alpha=0.15, color="#7c3aed")
ax.set_title("Seasonal Pattern: Avg Unemployment Rate by Month (Pre-COVID)", fontsize=14, weight="bold")
ax.set_ylabel("Unemployment Rate (%)")
ax.set_xlabel("Month")
plt.tight_layout()
plt.savefig(f"{CHARTS}/05_seasonal_pattern.png")
plt.close()

print("\nSeasonal averages (pre-COVID):\n", seasonal)

# ---------------------------------------------------------------
# 7. REGIONAL ZONE COMPARISON (dataset 2 has zone labels)
# ---------------------------------------------------------------
zone_trend = df2.groupby(["date", "zone"], as_index=False)["unemployment_rate"].mean()

fig, ax = plt.subplots(figsize=(11, 6))
for zone, grp in zone_trend.groupby("zone"):
    ax.plot(grp["date"], grp["unemployment_rate"], marker="o", label=zone, linewidth=2)
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"), color="red", alpha=0.10)
ax.set_title("Unemployment Rate by Zone (2020)", fontsize=14, weight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Unemployment Rate (%)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))
ax.legend(title="Zone")
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(f"{CHARTS}/06_zone_comparison.png")
plt.close()

zone_summary = df2.groupby("zone", as_index=False)["unemployment_rate"].mean().sort_values("unemployment_rate", ascending=False)
print("\nAvg unemployment by zone:\n", zone_summary)

# ---------------------------------------------------------------
# 8. LABOUR PARTICIPATION vs UNEMPLOYMENT (correlation)
# ---------------------------------------------------------------
corr = df1[["unemployment_rate", "labour_participation_rate", "employed"]].corr()
print("\nCorrelation matrix:\n", corr)

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, vmin=-1, vmax=1)
ax.set_title("Correlation: Unemployment vs Labour Participation vs Employment", fontsize=12, weight="bold")
plt.tight_layout()
plt.savefig(f"{CHARTS}/07_correlation_heatmap.png")
plt.close()

# ---------------------------------------------------------------
# 9. STATE-LEVEL AVERAGE (full period) — who structurally struggles most
# ---------------------------------------------------------------
state_avg = df1.groupby("state", as_index=False)["unemployment_rate"].mean().sort_values("unemployment_rate", ascending=False)

fig, ax = plt.subplots(figsize=(9, 9))
ax.barh(state_avg["state"][::-1], state_avg["unemployment_rate"][::-1], color="#0891b2")
ax.set_title("Average Unemployment Rate by State (Full Period)", fontsize=13, weight="bold")
ax.set_xlabel("Unemployment Rate (%)")
plt.tight_layout()
plt.savefig(f"{CHARTS}/08_state_avg_full_period.png")
plt.close()

print("\nHighest avg unemployment states:\n", state_avg.head(5))
print("\nLowest avg unemployment states:\n", state_avg.tail(5))

print("\nAll charts saved to /charts. Analysis complete.")
