from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Retail Sales Dashboard", page_icon="📊", layout="wide")

DATA_PATH = Path(__file__).resolve().parent / "data" / "sales_data.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)
    df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce").fillna(0)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Revenue"] = df["Total_Sales"]
    return df


@st.cache_data
def get_summary_text(df: pd.DataFrame) -> str:
    total_revenue = df["Revenue"].sum()
    best_category = df.groupby("Category")["Revenue"].sum().idxmax()
    best_product = df.groupby("Product_Name")["Revenue"].sum().idxmax()
    peak_month = df.groupby("Month")["Revenue"].sum().idxmax()
    average_order = df["Revenue"].mean()
    return (
        f"The dataset shows total sales of ${total_revenue:,.2f}. "
        f"{best_category} leads in category revenue, while {best_product} is the top-selling product. "
        f"The strongest month is {peak_month} with an average order value of ${average_order:,.2f}."
    )


def filter_data(df: pd.DataFrame):
    with st.sidebar:
        st.header("Filters")
        categories = sorted(df["Category"].dropna().unique())
        selected_categories = st.multiselect(
            "Select categories",
            options=categories,
            default=categories,
        )
        min_date = st.date_input(
            "Start date",
            value=df["Date"].min().date(),
            min_value=df["Date"].min().date(),
            max_value=df["Date"].max().date(),
        )
        max_date = st.date_input(
            "End date",
            value=df["Date"].max().date(),
            min_value=df["Date"].min().date(),
            max_value=df["Date"].max().date(),
        )
        if min_date > max_date:
            st.warning("Start date cannot be later than end date. Adjusting the range.")
            min_date, max_date = max_date, min_date

        selected_product = st.selectbox(
            "Focus product",
            options=["All"] + sorted(df["Product_Name"].dropna().unique().tolist()),
        )

    filtered_df = df[
        df["Category"].isin(selected_categories)
    ].copy()
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= min_date)
        & (filtered_df["Date"].dt.date <= max_date)
    ]

    if selected_product != "All":
        filtered_df = filtered_df[filtered_df["Product_Name"] == selected_product]

    return filtered_df


def build_metric_cards(df: pd.DataFrame):
    total_revenue = df["Revenue"].sum()
    total_orders = df["Invoice_ID"].nunique()
    avg_order_value = df["Revenue"].mean()
    total_quantity = df["Quantity"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Orders", f"{total_orders:,}")
    col3.metric("Avg. Order Value", f"${avg_order_value:,.2f}")
    col4.metric("Units Sold", f"{total_quantity:,.0f}")


def main():
    df = load_data()
    filtered_df = filter_data(df)

    st.title("Retail Sales Insight Dashboard")
    st.caption("Internship project based on invoice-level sales data")

    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust the filters on the sidebar.")
        return

    build_metric_cards(filtered_df)

    st.subheader("Business Summary")
    st.write(get_summary_text(filtered_df))

    category_chart = (
        filtered_df.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    )
    category_fig = px.bar(
        category_chart,
        x="Category",
        y="Revenue",
        title="Revenue by Category",
        color="Category",
        template="plotly_white",
    )
    category_fig.update_layout(showlegend=False)

    monthly_chart = (
        filtered_df.groupby("Month", as_index=False)["Revenue"].sum().sort_values("Month")
    )
    monthly_fig = px.line(
        monthly_chart,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Sales Trend",
        template="plotly_white",
    )

    top_products = (
        filtered_df.groupby("Product_Name", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False).head(10)
    )
    top_products_fig = px.bar(
        top_products,
        x="Product_Name",
        y="Revenue",
        title="Top 10 Products by Revenue",
        color="Product_Name",
        template="plotly_white",
    )
    top_products_fig.update_layout(showlegend=False)

    left_col, right_col = st.columns(2)
    with left_col:
        st.plotly_chart(category_fig, use_container_width=True)
    with right_col:
        st.plotly_chart(monthly_fig, use_container_width=True)

    st.plotly_chart(top_products_fig, use_container_width=True)

    st.subheader("Detailed Sales Records")
    display_df = filtered_df[[
        "Invoice_ID",
        "Customer_ID",
        "Product_Name",
        "Category",
        "Quantity",
        "Price",
        "Total_Sales",
        "Date",
    ]].copy()
    display_df = display_df.sort_values("Date", ascending=False)
    st.dataframe(display_df, use_container_width=True)


if __name__ == "__main__":
    main()
