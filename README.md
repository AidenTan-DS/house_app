# 🏡 House & Browse - Housing Affordability Dashboard

An interactive U.S. housing affordability data visualization dashboard with two different designs.

## 📋 Project Structure

```
DATA511 project/
├── app.py                    # Main application entry (includes navigation)
├── pages/
│   ├── intro.py             # Introduction page
│   ├── design1.py           # Design 1: Interactive Map Explorer
│   └── design2.py           # Design 2: Time Series Comparison
├── desgin1/                 # Design 1 source code and data
│   ├── app.py
│   ├── charts.py
│   ├── config_data.py
│   ├── geo_utils.py
│   ├── events.py
│   └── data/
│       ├── house_ts_agg.csv
│       ├── cbsa_shapes.zip
│       └── zcta_shapes.zip
├── design2/                  # Design 2 source code and data
│   ├── design2.py
│   ├── home.py
│   └── HouseTS.csv
└── requirements.txt         # Project dependencies
```

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501` by default.

## 🎯 Features

### 🏠 Intro Page
- Project introduction
- Description of the two designs
- Price-to-Income Ratio (PTI) calculation method
- References

### 🗺️ Design 1: Interactive Map Explorer
**Key Features:**
- **Metro-level Visualization**: Interactive choropleth map
- **Drill-down Functionality**: Drill down from Metro areas to ZIP codes
- **Multiple Metrics**: Price-to-Income Ratio (PTI) and median sale price
- **Historical Trends**: Time series analysis for individual ZIP codes
- **Geographic Exploration**: Clickable map

**How to Use:**
1. Use the control panel at the top to select year and metric
2. Click on Metro areas on the map to view ZIP code details
3. Click on ZIP codes to view detailed metrics and historical trends

### 📊 Design 2: Time Series Comparison
**Key Features:**
- **Multi-city Comparison**: Time series comparison of price-to-income ratios
- **Affordability Level Visualization**: Color-coded level bands
- **Interactive Selection**: Select multiple metropolitan areas
- **Annual Analysis**: Yearly changes from 2012-2023

**How to Use:**
1. Select metropolitan areas to compare in the left panel
2. Charts will automatically update to show selected cities
3. Hover to view detailed data

## 📊 Data Description

### Data Sources
- **HouseTS Dataset**: From Kaggle, containing data for 30 major U.S. metropolitan areas from 2012-2023
- **Shapefiles**: CBSA and ZCTA boundary data for map visualization

### Metric Definitions

**Price-to-Income Ratio (PTI)**
```
PTI = median_sale_price / (per_capita_income × 2.51)
```
Where 2.51 is the median U.S. household size.

**Affordability Levels:**
- **0.0-3.0**: Affordable 🟢
- **3.1-4.0**: Moderately Unaffordable 🟡
- **4.1-5.0**: Seriously Unaffordable 🟠
- **5.1-8.9**: Severely Unaffordable 🔴
- **9.0+**: Impossibly Unaffordable ⚫

## 🛠️ Tech Stack

- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and maps
- **GeoPandas**: Geospatial data processing
- **Pandas**: Data processing
- **NumPy**: Numerical computation

## 📚 References

- **Dataset**: shengkunwang. (2025). *HouseTS Dataset*. Kaggle
- **Affordability Levels**: Cox, Wendell (2025). *Demographia International Housing Affordability, 2025 Edition*. Center for Demographics and Policy

## 🔧 Troubleshooting

### Design 1 Cannot Load Data
- Ensure `desgin1/data/house_ts_agg.csv` file exists
- Check if shapefile ZIP files are complete

### Design 2 Cannot Load Data
- Ensure `design2/HouseTS.csv` file exists
- Check if the file path is correct

### Map Not Displaying
- Ensure all dependencies are installed (especially geopandas and shapely)
- Check if shapefile files are complete

## 📝 Notes

- Design 1 requires significant memory to process geospatial data
- Initial map loading may take some time
- A modern browser is recommended for the best experience

