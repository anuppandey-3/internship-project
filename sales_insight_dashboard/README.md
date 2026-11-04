# Retail Sales Insight Dashboard

This internship project analyzes a retail sales dataset and presents the results in an interactive dashboard.

## Overview

The project uses a CSV dataset containing invoice-level information such as:
- Invoice ID
- Customer ID
- Product name
- Category
- Quantity
- Unit price
- Total sales
- Date

The dashboard helps identify:
- Best-performing product categories
- Monthly revenue patterns
- Top-selling products
- Sales distribution by product and category

## Features

- Sidebar filters for category and date range
- KPI cards for sales overview
- Revenue trend charts
- Category performance insights
- Product ranking panel
- Detailed records table

## Run locally

1. Create a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app
   ```bash
   streamlit run app.py
   ```

The app will open in your default browser.
