import sys
import os
from pathlib import Path

# Add story directory to Python path
project_root = Path(__file__).parent.parent
story_path = project_root / "story"

# Remove any conflicting paths from sys.path first
# This ensures we import from the correct directory
if str(story_path) not in sys.path:
    sys.path.insert(0, str(story_path))

# Remove other design directories from sys.path to avoid conflicts
desgin1_path = project_root / "desgin1"
design2_path = project_root / "design2"
design3_path = project_root / "design3" / "Amber_design3"

# Remove conflicting paths if they exist
paths_to_remove = [str(desgin1_path), str(design2_path), str(design3_path)]
for path in paths_to_remove:
    if path in sys.path:
        sys.path.remove(path)

# Ensure story path is first
if sys.path[0] != str(story_path):
    sys.path.insert(0, str(story_path))

# Store original working directory but don't change it
# Use absolute paths instead to avoid issues with os.chdir
original_cwd = os.getcwd()
# Note: We don't change directory to avoid path issues in Streamlit Cloud
# All file paths should be absolute or relative to project_root

try:
    import streamlit as st
    
    # Clear any cached modules to avoid conflicts with other pages that have modules with same names
    # Force clear all conflicting modules from cache before importing
    modules_to_clear = ['data_utils', 'charts']
    for module_name in modules_to_clear:
        # Remove from cache if exists
        if module_name in sys.modules:
            del sys.modules[module_name]
        # Also try removing from submodule cache
        for key in list(sys.modules.keys()):
            if key.startswith(f"{module_name}."):
                del sys.modules[key]
    
    # Use importlib to import from specific directory
    import importlib.util
    
    # Import modules using file paths to ensure we get the right ones
    def import_from_path(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module {module_name} from {file_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    # Import from story directory using file paths to avoid conflicts
    # Import in dependency order: data_utils first, then charts (which depends on data_utils)
    data_utils = import_from_path('data_utils', story_path / 'data_utils.py')
    # Make sure data_utils is in sys.modules so charts can import it
    sys.modules['data_utils'] = data_utils
    charts_module = import_from_path('charts', story_path / 'charts.py')
    
    # Import what we need directly from the loaded modules
    load_raw_data = data_utils.load_raw_data
    add_derived_columns = data_utils.add_derived_columns
    composite_series = data_utils.composite_series
    yearly_metro_summary = data_utils.yearly_metro_summary
    affordability_counts_by_year = data_utils.affordability_counts_by_year
    latest_year = data_utils.latest_year
    AFFORDABILITY_ORDER = data_utils.AFFORDABILITY_ORDER
    AFFORDABILITY_COLORS = data_utils.AFFORDABILITY_COLORS
    
    composite_price_income_index_chart = charts_module.composite_price_income_index_chart
    metro_pti_lines = charts_module.metro_pti_lines
    composite_rent_to_income = charts_module.composite_rent_to_income
    metro_snapshot_bar = charts_module.metro_snapshot_bar
    affordability_bands_with_us_ratio = charts_module.affordability_bands_with_us_ratio

    # ----- GLOBAL STYLE FIXES -----
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 3rem !important;
        }
        h1 {
            margin-top: 0rem !important;
            margin-bottom: 0.5rem !important;
            padding-top: 1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Page title (parent app handles navigation)
    st.title("📖 Housing Affordability Story")
    st.caption("Explore the data story behind housing affordability trends across U.S. metropolitan areas")

    # ---- load & prep data ----
    try:
        raw = load_raw_data()
        if raw.empty:
            st.error("❌ **Data Loading Error**: The data file is empty. Please check that `story/data/HouseTS_reduced.csv` exists and contains data.")
            st.stop()
        df = add_derived_columns(raw)
        comp = composite_series(df)
        summary = yearly_metro_summary(df)
        counts = affordability_counts_by_year(summary)
        year_latest = latest_year(summary)
    except FileNotFoundError as e:
        st.error(f"""
        ❌ **Data File Not Found**
        
        Unable to load the required data file. Please ensure:
        - The file `story/data/HouseTS_reduced.csv` exists
        - The file path is correct
        - File permissions are set correctly
        
        **Technical details:** {str(e)}
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ **Data Loading Error**: {str(e)}")
        import traceback
        with st.expander("Error Details"):
            st.code(traceback.format_exc())
        st.stop()

    # ---- tabs / chapters ----
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Prices vs Incomes (Macro Trend)",
        "2. Metro Affordability Divergence",
        "3. Affordability Bands",
        "4. Rent Burden vs Ownership Burden",
        "5. 2023 Metro Snapshot",
    ])
            
    with tab1:
        st.subheader("1. Prices vs Incomes (Macro Trend)")

        st.markdown(
            """
            Home prices and household incomes do not move together. This chapter compares both series indexed to **2012 = 100**.

            The macro trend answers the first big question: **Is the U.S. housing affordability problem structural?**  
            The answer is: Yes, prices have consistently pulled away from incomes.
            """
        )

        
        with st.container(border=True):
            st.plotly_chart(
                composite_price_income_index_chart(comp),
                use_container_width=True,
            )
        
        with st.container(border=True):

            st.markdown(
                """
                ### What We notice
                - If home prices and incomes grew at the same rate, the lines would stay close.  
                - **Home prices outpaced incomes throughout the last decade.**  
                - This widening gap sets the foundation for today's affordability pressures.
                """
            )

    with tab2:
        
        col_left, col_right = st.columns([2.3, 1])   # wider left column, narrower right

        with col_left:
            st.subheader("2. Metro Affordability Divergence")
            st.markdown(
                """
                Even though national averages show prices growing faster than incomes,
                the **severity varies dramatically across metros**.

                This chapter ranks metros by **Price-to-Income ratio (PTI)** and
                traces their affordability trajectories over time.
                """
            )

        with col_right:
            with st.container(border=True):
                st.markdown("#### What is PTI?")
                st.markdown(
                    """
                    PTI is a simple measure:  
                    **PTI = Median Home Price / Median Household Income**

                    - Higher PTI → **less affordable**  
                    - Lower PTI → **more attainable**
                    """
                )

            focus_year = 2023

        # Chart in a bordered container
        with st.container(border=True):
            st.plotly_chart(
                metro_pti_lines(df, focus_year=focus_year),
                use_container_width=True,
            )

        # --- compute top/bottom 7 metros for that year using `summary` ---
        summary_year = (
            summary[summary["year"] == focus_year]
            .dropna(subset=["price_to_income"])
        )

        top7 = (
            summary_year.sort_values("price_to_income", ascending=False)
            .head(7)["city_full"]
            .tolist()
        )

        bottom7 = (
            summary_year.sort_values("price_to_income", ascending=True)
            .head(7)["city_full"]
            .tolist()
        )

        # --- list in a card-style container ---
        with st.container(border=True):
            st.markdown(
                """
                ### What We Notice
                - Which metros have become "outliers" (extreme PTI)  
                - Whether affordable metros stayed affordable or caught up to expensive ones

                The story:  
                **Housing affordability is not evenly distributed—metros are splitting into different trajectories.**
                """
            )
            st.markdown(f"### Metros Highlighted in {focus_year}")
            st.markdown(f"**Top 7 (Least Affordable – highest PTI):** {', '.join(top7)}")
            st.markdown(f"**Bottom 7 (Most Affordable – lowest PTI):** {', '.join(bottom7)}")

    # ----- CHAPTER 3 -----
    with tab3:
        st.subheader("3. Affordability Bands")

        st.markdown(
            """
            PTI ratios become even more meaningful when grouped into **affordability categories**.  

            ### PTI Affordability Categories
            - **Affordable**: PTI ≤ 3.0  
            - **Moderately Unaffordable**: PTI 3.1–4.0  
            - **Seriously Unaffordable**: PTI 4.1–5.0  
            - **Severely Unaffordable**: PTI 5.1-8.9  
            - **Impossibly Unaffordable**: PTI ≥ 9.0
            """
        )

        year_focus = latest_year(summary)
        
        with st.container(border=True):
            st.plotly_chart(
            affordability_bands_with_us_ratio(counts, comp),
            use_container_width=True,
            )

        with st.container(border=True):
            st.markdown(
                """
            ### What We Notice
            - Each year, fewer metros remain in the Affordable category, while more are moving into higher PTI ranges.
            - This indicates a structural and widespread drift toward unaffordability, rather than short-term volatility or isolated market spikes.

            In short:  
            A decade ago, many metros were still reasonably affordable for median-income households.
            Today, a growing share has moved into seriously, severely, or even impossibly unaffordable territory.
            """
            )

    # ----- CHAPTER 4 -----
    with tab4:
        st.subheader("4. Rent Burden vs Ownership Burden")

        st.markdown(
            """
            The affordability crisis looks very different depending on whether
            a household is **renting** or **buying**.
            """
        )

        with st.container(border=True):
            st.plotly_chart(
                composite_rent_to_income(summary),
                use_container_width=True,
            )
            
        with st.container(border=True):
            st.markdown(
                """
                ### Key insight
                Earlier chapters showed that home prices have pulled far ahead of incomes, pushing ownership burden sharply upward.  
                This chart adds another dimension: rent burden hasn't moved much at all.

                Together, these trends reveal that:
                - The affordability crisis is not uniform.
                - For renters, costs have grown slowly and predictably relative to income.
                - For buyers, costs have surged far faster than incomes can keep up with.

                **Bottom Line**:
                Renting remains more closely coupled to income, but the leap to homeownership has become increasingly unattainable.
                """
            )

    # ----- CHAPTER 5 -----
    with tab5:
        st.subheader("5. 2023 Metro Snapshot")

        st.markdown(
            """
            This final chapter provides a **recent snapshot** of affordability conditions.
            """
        )

        fig = metro_snapshot_bar(summary)

        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.markdown(
            """
            ### What you can see here

            - PTI levels for all metros in the most recent year  
            - Which metros are currently the **least affordable**  
            - Which metros remain relatively **more attainable**  
            - How these map into our affordability bands
            """
            )

except Exception as e:
    import streamlit as st
    st.error(f"Error loading Story: {str(e)}")
    import traceback
    with st.expander("Error Details"):
        st.code(traceback.format_exc())
finally:
    # Restore original working directory (only if we changed it)
    # Since we don't use os.chdir anymore, this is just for safety
    try:
        if original_cwd and os.getcwd() != original_cwd:
            os.chdir(original_cwd)
    except Exception:
        pass  # Ignore errors when restoring directory

