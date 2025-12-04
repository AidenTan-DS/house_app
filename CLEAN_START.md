# Clean Start Instructions

If you're experiencing stability issues with the application, follow these steps:

## 1. Clear All Caches

```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null

# Clear Streamlit session cache (if exists)
rm -rf .streamlit/cache 2>/dev/null
```

## 2. Verify File Structure

Ensure you have the following structure:
- `app.py` (root) - Main entry point
- `pages/intro.py`
- `pages/design1.py`
- `pages/design2.py`
- `pages/design3.py`
- `pages/story.py`

**Important**: Old `app.py` files in subdirectories should NOT be executed directly.

## 3. Start Fresh

```bash
# Navigate to project root
cd "/Users/yeyeyeyeyeyeyeye/Desktop/DATA511 project"

# Run the main application
streamlit run app.py
```

## 4. If Issues Persist

Check the error message and refer to `TROUBLESHOOTING.md` for specific solutions.

