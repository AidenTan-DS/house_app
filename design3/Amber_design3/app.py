# Placeholder file to prevent Streamlit auto-discovery file not found errors
# This file should not be executed directly - use pages/design3.py instead

import streamlit as st
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Navigation Help",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Get the project root and main app path
project_root = Path(__file__).parent.parent.parent
main_app_path = project_root / "app.py"
design3_page_path = project_root / "pages" / "design3.py"

# Display friendly message
st.info("ℹ️ **Streamlit Limitation**")

st.markdown("""
### Please use single-click navigation

Due to Streamlit's limitations, this file cannot be accessed by double-clicking.  
Please use the navigation menu in the main application to access pages.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Go to Main Application", use_container_width=True, type="primary"):
        try:
            if main_app_path.exists():
                st.switch_page(str(main_app_path))
            else:
                st.error("Please run `streamlit run app.py` from the project root.")
        except Exception:
            st.info("Please run `streamlit run app.py` from the project root directory.")

with col2:
    if st.button("💰 Go to Price Affordability Finder", use_container_width=True):
        try:
            if design3_page_path.exists():
                st.switch_page(str(design3_page_path))
            else:
                st.info("Please access through the main application.")
        except Exception:
            st.info("Please access this page through the main application navigation menu.")

st.markdown("---")
st.info("""
**How to use this application:**
1. Run `streamlit run app.py` from the project root directory
2. Use the navigation menu at the top (single-click) to access different pages
3. Click on "Price Affordability Finder" to view Design 3
""")

