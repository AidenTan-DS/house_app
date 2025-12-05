import streamlit as st

# Page configuration
st.set_page_config(
    page_title="House & Browse - Housing Affordability Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add CSS to align navigation bar to the right with text margins
st.markdown("""
<style>
    /* Match navigation container to block-container dimensions for alignment */
    [data-testid="stNavigation"] {
        max-width: min(1440px, 100%) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    
    /* Right-align navigation items */
    [data-testid="stNavigation"] nav,
    [data-testid="stNavigation"] > nav,
    [data-testid="stNavigation"] nav > div,
    [data-testid="stNavigation"] nav > ul {
        display: flex !important;
        justify-content: flex-end !important;
        width: 100% !important;
        margin-left: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Define pages for navigation
pages = [
    st.Page("pages/intro.py", title="Intro", icon="🏠"),
    st.Page("pages/design1.py", title="Interactive Map Explorer", icon="🗺️"),
    st.Page("pages/design2.py", title="Time Series Comparison", icon="📊"),
    st.Page("pages/design3.py", title="Price Affordability Finder", icon="💰"),
    st.Page("pages/story.py", title="Housing Affordability Story", icon="📖"),
]

# Create navigation at the top
pg = st.navigation(pages, position="top")
pg.run()
