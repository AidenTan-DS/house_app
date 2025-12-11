# 🏡 House & Browse - Housing Affordability Dashboard

An interactive U.S. housing affordability data visualization dashboard exploring 30 major metropolitan areas from 2012-2023.

## 🌐 Live Demo

**Try it online:** [[https://houseapp-cqznkr7u5sx3kctd8ui7gs.streamlit.app](https://houseapp-cqznkr7u5sx3kctd8ui7gs.streamlit.app)](https://houseapp-i2uqriykdh9d6ui38wvwev.streamlit.app)

## 📋 Project Structure

```
DATA511 project/
├── app.py                    # Main application entry (includes navigation)
├── pages/
│   ├── intro.py             # Home page with project overview
│   ├── design1.py           # Design 1: Interactive Map Explorer
│   ├── design2.py           # Design 2: Time Series Comparison
│   ├── design3.py           # Design 3: Price Affordability Finder
│   └── story.py             # Narrative visualization
├── design1/                 # Design 1 source code and data
│   ├── charts.py
│   ├── config_data.py
│   ├── geo_utils.py
│   ├── events.py
│   └── data/
│       ├── house_ts_agg.csv
│       ├── cbsa_shapes.zip
│       └── zcta_shapes.zip
├── design2/                 # Design 2 source code and data
│   ├── design2.py
│   ├── home.py
│   └── HouseTS.csv
├── design3/                  # Design 3 source code
│   └── Amber_design3/
│       ├── dataprep.py
│       ├── ui_components.py
│       ├── zip_module.py
│       └── city_geojson/    # GeoJSON files for metro areas
├── story/                    # Story page source code
│   ├── charts.py
│   ├── data_utils.py
│   └── data/
│       └── HouseTS_reduced.csv
├── utils/                    # Shared utilities
│   ├── path_utils.py
│   └── error_handling.py
├── requirements.txt         # Project dependencies
└── README.md
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

### 🏠 Home Page
- Project introduction and overview
- Navigation to three interactive designs
- Price-to-Income Ratio (PTI) explanation with tooltips
- References and data sources

### 🗺️ Design 1: Interactive Map Explorer
**Key Features:**
- **Metro-level Visualization**: Interactive choropleth map showing all 30 metro areas
- **Drill-down Functionality**: Click metro areas to explore ZIP codes within
- **Multiple Metrics**: Price-to-Income Ratio (PTI) and median sale price
- **Historical Trends**: Time series analysis for individual ZIP codes
- **Year-over-Year Analysis**: Compare changes between years
- **Ranking System**: See how areas rank within their metro

**How to Use:**
1. Use the control panel to select year and metric type
2. Hover over metro areas to preview statistics
3. Click on metro areas to view ZIP code details
4. Click on ZIP codes to see detailed metrics and historical trends
5. Use "Back to All Metros" to return to the national view

### 📊 Design 2: Time Series Comparison
**Key Features:**
- **Multi-city Comparison**: Compare price-to-income ratios across multiple metro areas
- **Affordability Level Visualization**: Color-coded affordability bands
- **Interactive Selection**: Select and compare multiple metropolitan areas
- **Annual Analysis**: View trends from 2012-2023
- **Hover Details**: See exact values for each year

**How to Use:**
1. Select metropolitan areas from the dropdown in the left panel
2. Charts automatically update to show selected cities
3. Hover over data points to view detailed information
4. Use "Reset to Default" to return to default selection

### 💰 Design 3: Price Affordability Finder
**Key Features:**
- **User Profile System**: Select persona (Student, Young Professional, Family) or set custom income
- **Metro Area Comparison**: Compare cities by PTI (price-to-income ratio) with tooltips
- **ZIP-code Level Details**: Explore affordable ZIP codes within selected metro areas
- **Interactive Map**: Visualize affordability at ZIP code level with color coding
- **Affordability Summary**: See maximum affordable price based on your income
- **Year Selection**: Analyze data across different years (2012-2023)

**How to Use:**
1. Set your income using the persona selector or manual input
2. View the affordability summary showing your maximum affordable price
3. Compare metro areas by PTI in the left column
4. Select a metro area to explore ZIP codes in the right column
5. Use the year selector to adjust the data being displayed

### 📖 Story Page
- Narrative visualization of housing affordability trends
- Data-driven storytelling across the 30 metro areas

## 📊 Data Description

### Data Sources
- **HouseTS Dataset**: From Kaggle, containing data for 30 major U.S. metropolitan areas from 2012-2023
- **Shapefiles**: CBSA (Core Based Statistical Area) and ZCTA (ZIP Code Tabulation Area) boundary data for map visualization
- **GeoJSON Files**: Pre-processed geographic data for metro areas in Design 3

### Metric Definitions

**Price-to-Income Ratio (PTI)**
```
PTI = median_sale_price / (per_capita_income × 2.54)
```
Where 2.54 is the median U.S. household size (2019-2023).

**Affordability Levels:**
- **0.0-3.0**: 🟢 Affordable
- **3.1-4.0**: 🟡 Moderately Unaffordable
- **4.1-5.0**: 🟠 Seriously Unaffordable
- **5.1-8.9**: 🔴 Severely Unaffordable
- **9.0+**: ⚫ Impossibly Unaffordable

*Affordability levels based on Demographia International Housing Affordability standards.*

## 🛠️ Tech Stack

- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and maps
- **GeoPandas**: Geospatial data processing
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computation
- **Shapely**: Geometric operations
- **PyArrow**: Efficient data storage and retrieval

## 📚 References

- **Dataset**: shengkunwang. (2025). *HouseTS Dataset*. Kaggle. https://www.kaggle.com/datasets/shengkunwang/housets-dataset/data
- **Price-to-Income Ratio Levels**: Cox, Wendell (2025). *Demographia International Housing Affordability, 2025 Edition*. Center for Demographics and Policy. https://www.chapman.edu/communication/_files/Demographia-International-Housing-Affordability-2025-Edition.pdf
- **Household Size**: U.S. Census Bureau. (2023). 2019—2023 ACS 5-Year Narrative Profile.

## 🔧 Troubleshooting

### Design 1 Cannot Load Data
- Ensure `design1/data/house_ts_agg.csv` file exists
- Check if shapefile ZIP files (`cbsa_shapes.zip`, `zcta_shapes.zip`) are complete
- Verify file paths in `config_data.py`

### Design 2 Cannot Load Data
- Ensure `design2/HouseTS.csv` file exists
- Check if the file path is correct

### Design 3 Cannot Load Data
- Ensure data files are accessible
- Check if GeoJSON files exist in `design3/Amber_design3/city_geojson/`
- Verify data file paths

### Map Not Displaying
- Ensure all dependencies are installed (especially `geopandas` and `shapely`)
- Check if shapefile files are complete
- Verify internet connection for map tiles (if using online map styles)

## 📝 Notes

- Design 1 requires significant memory to process geospatial data
- Initial map loading may take some time
- A modern browser is recommended for the best experience
- The application uses local data files by default (no Databricks connection required)

## 🏗️ Project Organization

- **Pages**: Main application pages in `pages/` directory
- **Design Modules**: Each design has its own directory with source code
- **Shared Utilities**: Common functions in `utils/` directory
- **Data Files**: Stored in respective design directories
