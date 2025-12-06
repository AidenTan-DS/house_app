import sys
from pathlib import Path

# Add utils to path for shared utilities
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.path_utils import setup_design_path, add_to_path

# Setup design2 path
design2_path, _ = setup_design_path("design2")
add_to_path(design2_path)

import streamlit as st
import pandas as pd
import plotly.express as px

# Hide navigation bar on design pages
st.markdown("""
<style>
/* Hide navigation bar on design pages */
header[data-testid="stHeader"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Return home button at the top
col_back, col_spacer = st.columns([2, 20])
with col_back:
    if st.button("🏠 Return Home", use_container_width=True, help="Return to home page", type="secondary"):
        st.switch_page("pages/intro.py")

st.title("📊 Time Series Comparison")
st.markdown(
    """
    <p style="color: #6b7280; font-size: 0.875rem; margin-top: -1rem; margin-bottom: 1rem;">
        Compare <span title="PTI Formula: Median Sale Price / Median Household Income. Lower values indicate better affordability." style="cursor: help; text-decoration: underline; text-decoration-style: dotted;">Price-to-Income Ratio</span> across multiple metropolitan areas over time
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stVirtualDropdown"] > div {
        height: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(show_spinner="Loading required data...", ttl=3600) 
def load_data():
    # Load HouseTS.csv from design2 directory using absolute path
    csv_path = design2_path / "HouseTS.csv"
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"❌ **File Not Found**: HouseTS.csv not found at {csv_path}")
        st.info("Please ensure HouseTS.csv exists in the design2 directory.")
        return pd.DataFrame(), []
    except Exception as e:
        st.error(f"❌ **Error loading data**: {str(e)}")
        st.info("Please check that HouseTS.csv is a valid CSV file.")
        return pd.DataFrame(), []
    
    # Check if file is a Git LFS pointer file
    if df.empty or len(df.columns) == 0 or "version https://git-lfs.github.com/spec/v1" in str(df.columns[0]):
        st.error("⚠️ HouseTS.csv appears to be a Git LFS pointer file.")
        st.markdown("""
        **To fix this issue:**
        1. Install Git LFS: `git lfs install`
        2. Pull the actual file: `git lfs pull` or `git lfs checkout HouseTS.csv`
        3. Or download the actual CSV file from the repository
        
        The file should be approximately 271 MB in size.
        """)
        return pd.DataFrame(), []
    
    # Normalize column names - handle both formats
    # Check for different possible column name formats
    price_col = None
    income_col = None
    
    # Try to find median_sale_price column (case-insensitive)
    for col in df.columns:
        col_lower = col.lower().replace(" ", "_").replace("-", "_")
        if "median" in col_lower and "sale" in col_lower and "price" in col_lower:
            price_col = col
        elif ("per_capita" in col_lower or "capita" in col_lower) and "income" in col_lower:
            income_col = col
    
    # If not found, try exact matches
    if price_col is None:
        if "median_sale_price" in df.columns:
            price_col = "median_sale_price"
        elif "Median Sale Price" in df.columns:
            price_col = "Median Sale Price"
    
    if income_col is None:
        if "Per Capita Income" in df.columns:
            income_col = "Per Capita Income"
        elif "per_capita_income" in df.columns:
            income_col = "per_capita_income"
    
    if price_col is None or income_col is None:
        st.error(f"Could not find required columns. Available columns: {list(df.columns)}")
        st.info("Expected columns: 'median_sale_price' (or 'Median Sale Price') and 'Per Capita Income' (or 'per_capita_income')")
        return pd.DataFrame(), []
    
    # Check for city_full column
    city_col = None
    if "city_full" in df.columns:
        city_col = "city_full"
    elif "city" in df.columns:
        # If only city column exists, we might need to use it
        city_col = "city"
        st.warning("Using 'city' column instead of 'city_full'. Some city names might be abbreviated.")
    
    if city_col is None:
        st.error(f"Could not find city column. Available columns: {list(df.columns)}")
        return pd.DataFrame(), []
    
    # Filter out rows with invalid data
    df = df[(df[price_col] > 0) & (df[income_col] > 0)].copy()
    df = df.fillna(0)

    # Price to Income Data Preparation
    df["Price_Income_Ratio"] = df[price_col] / (2.54 * df[income_col])
    
    # Group by city and year, then aggregate
    ratio_agg = (
        df.groupby([city_col, "year"], as_index=False)
        .agg({
            "Price_Income_Ratio": "median",
            price_col: "median",
            income_col: "median"
        })
    )
    
    # Rename columns for consistency
    ratio_agg = ratio_agg.rename(columns={
        city_col: "city_full",
        price_col: "median_sale_price",
        income_col: "Per Capita Income"
    })

    ratio_agg["Affordability"] = ""

    ratio_agg.loc[ratio_agg["Price_Income_Ratio"] <= 3.0,
                "Affordability"] = "Affordable"

    ratio_agg.loc[(ratio_agg["Price_Income_Ratio"] > 3.0) &
                (ratio_agg["Price_Income_Ratio"] <= 4.0),
                "Affordability"] = "Moderately Unaffordable"

    ratio_agg.loc[(ratio_agg["Price_Income_Ratio"] > 4.0) &
                (ratio_agg["Price_Income_Ratio"] <= 5.0),
                "Affordability"] = "Seriously Unaffordable"

    ratio_agg.loc[(ratio_agg["Price_Income_Ratio"] > 5.0) &
                (ratio_agg["Price_Income_Ratio"] < 9.0),
                "Affordability"] = "Severely Unaffordable"

    ratio_agg.loc[ratio_agg["Price_Income_Ratio"] >= 9.0,
                "Affordability"] = "Impossibly Unaffordable"

    city_order = sorted(df["city_full"].unique())
    
    return ratio_agg, city_order

data = load_data()
ratio_agg = data[0]
city_order = data[1]

# Check if data loaded successfully
if ratio_agg.empty or len(city_order) == 0:
    st.error("⚠️ No data available. Please check that the data files exist and are properly formatted.")
    st.stop()

with st.expander("How to Use This Tool", expanded=True, icon="💡"):
    st.markdown("""
                - 🎯 Pick any metropolitan area from the list above — the chart updates instantly.
                - 📊 Compare how affordable house prices are across metropolitan area and over time.
                - 🔍 Hover over any point to see detailed numbers for that year.

                Enjoy exploring! 🚀
                """)

if "selected_cities" not in st.session_state:
    st.session_state.selected_cities = city_order[:5]

def reset_cities():
    st.session_state.selected_cities = city_order[:5]

col1, col2 = st.columns([1.5,5], vertical_alignment="top")
with col1:
    with st.container(border=True, height="content"):
        st.markdown("<h2 style='font-size: 24px;'>Select Metropolitan Area</h2>", unsafe_allow_html=True)
        
        st.button("Reset to Default", on_click=reset_cities)
        selected_cities = st.multiselect(
            "Metro Areas",
            options=city_order,
            key="selected_cities"
        )

    

if len(selected_cities) == 0:
    with col2:
        st.warning("Please select at least one metropolitan area.")
else:
        # ===================================
        # Price to Income Ratio Visualization
        # ===================================

        price_income = ratio_agg[ratio_agg["city_full"].isin(selected_cities)].copy()

        customdata = price_income[["Per Capita Income", "median_sale_price", "Affordability"]].values

        colors = px.colors.qualitative.Plotly  
        color_map = {city: colors[i % len(colors)] for i, city in enumerate(selected_cities)}

        price_income_fig = px.line(
            price_income,
            x="year",
            y="Price_Income_Ratio",
            color="city_full",
            color_discrete_map=color_map,
            markers=True
        )

        for i, trace in enumerate(price_income_fig.data):
            city_name = trace.name
            mask = price_income["city_full"] == city_name
            price_income_fig.data[i].customdata = customdata[mask.values]

        price_income_fig.add_hline(
            y=3,
            line_width=2,
            line_dash="dash",
            line_color="silver",
            annotation_text="0.0-3.0: Affordable",
            annotation_position="bottom right",
            annotation_bgcolor="rgba(255,255,255,0.7)"
        )

        price_income_fig.add_hrect(
            y0=0.0, 
            y1=3.0, 
            line_width=0, 
            fillcolor="Green", 
            layer="below", 
            opacity=0.2
        )

        price_income_fig.add_hline(
            y=4,
            line_width=2,
            line_dash="dash",
            line_color="silver",
            annotation_text="3.1-4.0: Moderately Unaffordable",
            annotation_position="bottom right",
            annotation_bgcolor="rgba(255,255,255,0.7)"
        )

        price_income_fig.add_hrect(
            y0=3.0, 
            y1=4.0, 
            line_width=0, 
            fillcolor="Yellow", 
            layer="below", 
            opacity=0.2
        )

        price_income_fig.add_hline(
            y=5,
            line_width=2,
            line_dash="dash",
            line_color="silver",
            annotation_text="4.1-5.0: Seriously Unaffordable",
            annotation_position="bottom right",
            annotation_bgcolor="rgba(255,255,255,0.7)"
        )

        price_income_fig.add_hrect(
            y0=4.0, 
            y1=5.0, 
            line_width=0, 
            fillcolor="Orange", 
            layer="below", 
            opacity=0.2
        )

        price_income_fig.add_hline(
            y=9,
            line_width=2,
            line_dash="dash",
            line_color="silver",
            annotation_text="5.1-8.9: Severely Unaffordable",
            annotation_position="bottom right",
            annotation_bgcolor="rgba(255,255,255,0.7)"
        )

        price_income_fig.add_hrect(
            y0=5.0, 
            y1=9.0, 
            line_width=0, 
            fillcolor="Red", 
            layer="below", 
            opacity=0.2
        )

        ymax = price_income["Price_Income_Ratio"].max() + 1
        if ymax < 9.0:
            ymax = 10
        
        price_income_fig.add_hline(
            y=ymax,
            line_width=2,
            line_dash="dash",
            line_color="silver",
            annotation_text="9.0+: Impossibly Unaffordable",
            annotation_position="bottom right",
            annotation_bgcolor="rgba(255,255,255,0.7)"
        )

        price_income_fig.add_hrect(
            y0=9.0, 
            y1=ymax,
            line_width=0, 
            fillcolor="DarkRed", 
            layer="below", 
            opacity=0.2
        )

        price_income_fig.update_traces(
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                "%{customdata[2]}<br>" +
                "Year: %{x}<br>" +
                "Ratio: x%{y:.2f}<br>" +
                "Median Income: $%{customdata[0]:.0f}<br>" +
                "Median Sale Price: $%{customdata[1]:.0f}<extra></extra>"
        )

        price_income_fig.update_layout(
            title={"text": "Price-to-Income (PTI):<br>U.S. Metropolitan Areas from 2012 to 2023", "font": {"size": 28}},
            yaxis_title="Price-to-Income Ratio",
            yaxis2=dict(
            title='Right Y-Axis Label',
            overlaying='y',
            side='right'
            ),
            xaxis_title="Year",
            hovermode="closest",
            template="plotly_white",
            legend=dict(title="Metro Area"),
            height=600,
            margin=dict(l=20, r=20, t=120),
            font=dict(size=14)
        )

        # ====================================
        # Dashboard Display
        # ====================================

        with col2:
            with st.container(border=True):
                st.plotly_chart(price_income_fig, use_container_width=True)
                st.caption("Affordability levels based on Price-to-Income Ratio thresholds from: Cox, Wendell (2025). *Demographia International Housing Affordability, 2025 Edition*. Center for Demographics and Policy.")

