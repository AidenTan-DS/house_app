# Troubleshooting Guide

## Common Issues and Solutions

### Issue: Streamlit errors about missing files in subdirectories

**Error**: `Unable to create Page. The file home.py could not be found.`

**Cause**: Streamlit may be trying to auto-discover pages in subdirectories, or there's a cache issue.

**Solution**:
1. Clear Streamlit cache:
   ```bash
   rm -rf ~/.streamlit/cache
   ```

2. Restart the Streamlit server:
   - Stop the current server (Ctrl+C)
   - Run `streamlit run app.py` from the root directory

3. Ensure you're running from the correct directory:
   ```bash
   cd "/Users/yeyeyeyeyeyeyeye/Desktop/DATA511 project"
   streamlit run app.py
   ```

### Issue: Module import conflicts

**Error**: `ImportError: cannot import name 'X' from 'Y'`

**Cause**: Multiple directories have modules with the same name (e.g., `charts.py`).

**Solution**: The app already handles this with module cache clearing. If issues persist:
1. Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
2. Restart the application

### Issue: Design 3 shows only text without interactive components

**Cause**: Data loading failed, causing `st.stop()` to be called after the intro text.

**Solution**: The app now checks data loading before displaying intro text. Check:
- Data file exists: `design3/Amber_design3/data/`
- File permissions are correct
- No import errors in the console

### Issue: Navigation buttons not highlighting current page

**Cause**: CSS `:has()` selector may not be fully supported in all browsers.

**Solution**: The app uses CSS that should work in modern browsers. If issues persist, clear browser cache.

## Application Structure

The main entry point is **`app.py`** in the root directory. All pages are accessed through:
- `pages/intro.py` - Introduction page
- `pages/design1.py` - Interactive Map Explorer (wraps `desgin1/app.py`)
- `pages/design2.py` - Time Series Comparison (wraps `design2/design2.py`)
- `pages/design3.py` - Price Affordability Finder (wraps `design3/Amber_design3/app.py`)
- `pages/story.py` - Housing Affordability Story (wraps `story/app.py`)

**Important**: Do NOT run `streamlit run` on subdirectory `app.py` files. Always use the root `app.py`.

