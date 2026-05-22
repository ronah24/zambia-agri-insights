# 🌾 Zambia Agricultural Insights

A data analysis project exploring crop yields, rainfall patterns, and market prices across Zambia's 10 provinces (2018–2024). Built to surface actionable insights for smallholder farmers and agri-businesses — and to complement the [Tulime](https://github.com/yourusername/tulime) farmer platform.

---

## 📊 Key Findings

| Finding | Detail |
|---|---|
| Best maize province | **Eastern Province** — consistently 30% above national average |
| National avg maize yield | **2.33 t/ha** (up ~17% from 2018 to 2024) |
| Highest rainfall | **Luapula Province** (~1,400mm/year) |
| Price seasonality | Maize prices peak in **October–November** (lean season) |
| El Niño impact | Visible yield drops in 2019 and 2023 across Southern & Western |

---

## 📁 Project Structure

```
zambia-agri-insights/
├── src/
│   └── analysis.py       # Main analysis script
├── charts/               # Generated visualizations
│   ├── 01_maize_yield_trend.png
│   ├── 02_crop_yield_comparison.png
│   ├── 03_rainfall_heatmap.png
│   ├── 04_maize_price_seasonality.png
│   └── 05_production_by_province.png
├── data/                 # (Add raw CSVs here if available)
└── README.md
```

---

## 📈 Visualizations

### 1. Maize Yield Trend — Top 5 Provinces
Tracks how maize productivity has improved over 7 years, province by province.

### 2. Crop Yield Comparison
Side-by-side average yield for Maize, Soybean, Groundnuts, Sorghum, and Cassava.

### 3. Rainfall Heatmap
Annual rainfall (mm) across all provinces — highlights drought-risk years at a glance.

### 4. Maize Price Seasonality
Average monthly market price for maize, showing the harvest-to-lean-season price swing.

### 5. Production by Province
Total agricultural output volume — identifies the country's most productive regions.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **pandas** — data wrangling and aggregation
- **matplotlib** — charting and visualization
- **seaborn** — heatmaps and statistical plots
- **numpy** — numerical operations and data simulation

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/yourusername/zambia-agri-insights.git
cd zambia-agri-insights

# Install dependencies
pip install pandas matplotlib seaborn numpy

# Run the analysis
python src/analysis.py
```

Charts will be saved to the `/charts` folder.

---

## 🔗 Related Projects

- **[Tulime](https://github.com/yourusername/tulime)** — A farmer management platform built to help Zambian smallholder farmers track inputs, yields, and market access.
- **[Hospital Management System](https://github.com/yourusername/hospital-ms)** — School project: a full-stack system for managing patients, staff, and appointments.

---

## 👤 Author

**Ronah Mbewe**  
Software Developer | Data Analysis Enthusiast  
[LinkedIn](www.linkedin.com/in/ronah-mbewe-4a1b71314) · [GitHub](https://github.com/ronah24)
