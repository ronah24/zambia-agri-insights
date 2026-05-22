"""
Zambia Agricultural Insights
Data analysis of crop yields, rainfall, and market prices across Zambian provinces.
Author: Your Name
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = ["#0B1F3A", "#C8922A", "#2E6B9E", "#5B9E4A", "#9E3A2E", "#6B4A9E"]
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 150,
})

# ── GENERATE REALISTIC ZAMBIA DATA ─────────────────────────────────────────

np.random.seed(42)

PROVINCES = ["Lusaka", "Copperbelt", "Southern", "Eastern", "Northern",
             "Central", "Western", "Luapula", "Muchinga", "North-Western"]

CROPS = ["Maize", "Soybean", "Groundnuts", "Sorghum", "Cassava"]

YEARS = list(range(2018, 2025))

# Crop yield data (tonnes per hectare) per province per year
yield_records = []
base_yields = {"Maize": 2.1, "Soybean": 1.4, "Groundnuts": 0.9, "Sorghum": 1.2, "Cassava": 8.5}
province_factors = {
    "Lusaka": 1.15, "Copperbelt": 1.05, "Southern": 1.20, "Eastern": 1.30,
    "Northern": 0.95, "Central": 1.10, "Western": 0.80, "Luapula": 0.85,
    "Muchinga": 0.90, "North-Western": 0.88
}

for province in PROVINCES:
    for crop in CROPS:
        for year in YEARS:
            trend = 1 + (year - 2018) * 0.025
            noise = np.random.normal(1.0, 0.12)
            yield_val = base_yields[crop] * province_factors[province] * trend * noise
            area = np.random.randint(800, 5000)
            yield_records.append({
                "province": province, "crop": crop, "year": year,
                "yield_tha": round(max(yield_val, 0.3), 2),
                "area_ha": area,
                "production_t": round(yield_val * area, 0)
            })

df_yield = pd.DataFrame(yield_records)

# Rainfall data (mm) per province per year
rainfall_records = []
base_rain = {
    "Lusaka": 820, "Copperbelt": 1200, "Southern": 650, "Eastern": 950,
    "Northern": 1300, "Central": 900, "Western": 750, "Luapula": 1400,
    "Muchinga": 1100, "North-Western": 1250
}
for province in PROVINCES:
    for year in YEARS:
        el_nino_effect = -120 if year in [2019, 2023] else 0
        rain = base_rain[province] + el_nino_effect + np.random.normal(0, 80)
        rainfall_records.append({"province": province, "year": year, "rainfall_mm": round(rain, 1)})

df_rain = pd.DataFrame(rainfall_records)

# Market price data (ZMW per 50kg bag)
price_records = []
base_prices = {"Maize": 180, "Soybean": 320, "Groundnuts": 420, "Sorghum": 150, "Cassava": 90}
for crop in CROPS:
    for year in YEARS:
        inflation = 1 + (year - 2018) * 0.07
        seasonal_months = list(range(1, 13))
        for month in seasonal_months:
            seasonal = 1 + 0.15 * np.sin((month - 3) * np.pi / 6)
            price = base_prices[crop] * inflation * seasonal * np.random.normal(1, 0.05)
            price_records.append({"crop": crop, "year": year, "month": month,
                                   "price_zmw": round(price, 2)})

df_price = pd.DataFrame(price_records)

print("✅ Data generated:")
print(f"   Yield records : {len(df_yield)}")
print(f"   Rainfall rows : {len(df_rain)}")
print(f"   Price records : {len(df_price)}")


# ── CHART 1: Maize yield trend by province (top 5) ─────────────────────────

def chart_maize_yield_trend():
    maize = df_yield[df_yield["crop"] == "Maize"]
    top5 = maize.groupby("province")["yield_tha"].mean().nlargest(5).index
    data = maize[maize["province"].isin(top5)].groupby(["year","province"])["yield_tha"].mean().unstack()

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, col in enumerate(data.columns):
        ax.plot(data.index, data[col], marker="o", linewidth=2,
                color=PALETTE[i], label=col, markersize=5)

    ax.set_title("Maize Yield Trend — Top 5 Provinces (2018–2024)", fontsize=14, fontweight="bold", pad=16)
    ax.set_xlabel("Year"); ax.set_ylabel("Yield (tonnes/hectare)")
    ax.legend(frameon=False, fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01_maize_yield_trend.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   Saved: {path}")

# ── CHART 2: Average yield by crop (bar) ───────────────────────────────────

def chart_crop_comparison():
    avg = df_yield.groupby("crop")["yield_tha"].mean().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(avg.index, avg.values, color=PALETTE[:len(avg)], height=0.5)
    for bar, val in zip(bars, avg.values):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f"{val:.2f} t/ha", va="center", fontsize=9, color="#333")

    ax.set_title("Average Crop Yield Across Zambia (2018–2024)", fontsize=14, fontweight="bold", pad=16)
    ax.set_xlabel("Average Yield (tonnes/hectare)")
    ax.set_xlim(0, avg.max() * 1.18)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "02_crop_yield_comparison.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   Saved: {path}")

# ── CHART 3: Rainfall heatmap by province and year ─────────────────────────

def chart_rainfall_heatmap():
    pivot = df_rain.pivot(index="province", columns="year", values="rainfall_mm")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
                linewidths=0.4, ax=ax, cbar_kws={"label": "Rainfall (mm)"})
    ax.set_title("Annual Rainfall by Province (mm)", fontsize=14, fontweight="bold", pad=16)
    ax.set_xlabel("Year"); ax.set_ylabel("")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "03_rainfall_heatmap.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   Saved: {path}")

# ── CHART 4: Maize price seasonality ───────────────────────────────────────

def chart_price_seasonality():
    maize_price = df_price[df_price["crop"] == "Maize"]
    avg_monthly = maize_price.groupby("month")["price_zmw"].mean()
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.fill_between(range(1,13), avg_monthly.values, alpha=0.15, color=PALETTE[1])
    ax.plot(range(1,13), avg_monthly.values, marker="o", color=PALETTE[1],
            linewidth=2.5, markersize=6)
    ax.set_xticks(range(1,13)); ax.set_xticklabels(months)
    ax.set_title("Maize Price Seasonality — Average Monthly Price (ZMW/50kg bag)", fontsize=13, fontweight="bold", pad=16)
    ax.set_ylabel("Price (ZMW)"); ax.set_xlabel("")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "04_maize_price_seasonality.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   Saved: {path}")

# ── CHART 5: Production volume by province ─────────────────────────────────

def chart_production_by_province():
    total = df_yield.groupby("province")["production_t"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [PALETTE[0] if i < 3 else "#B0BEC5" for i in range(len(total))]
    ax.bar(total.index, total.values / 1000, color=colors, width=0.6)
    ax.set_title("Total Agricultural Production by Province (2018–2024)", fontsize=13, fontweight="bold", pad=16)
    ax.set_ylabel("Production (thousand tonnes)")
    ax.set_xlabel("")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "05_production_by_province.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   Saved: {path}")


# ── RUN ALL ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n📊 Running Zambia Agricultural Insights Analysis...\n")
    chart_maize_yield_trend()
    chart_crop_comparison()
    chart_rainfall_heatmap()
    chart_price_seasonality()
    chart_production_by_province()
    print("\n✅ All charts saved to /charts/")

    # Summary stats
    print("\n📈 Key Findings:")
    best_province = df_yield[df_yield["crop"]=="Maize"].groupby("province")["yield_tha"].mean().idxmax()
    avg_maize = df_yield[df_yield["crop"]=="Maize"]["yield_tha"].mean()
    print(f"   Best maize province : {best_province}")
    print(f"   National avg yield  : {avg_maize:.2f} t/ha")
    print(f"   Highest rainfall    : {df_rain.groupby('province')['rainfall_mm'].mean().idxmax()}")
