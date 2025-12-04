import streamlit as st

# Page configuration
st.set_page_config(
    page_title="House & Browse - Housing Affordability Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
