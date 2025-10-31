import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Banking KPI Screener", layout="wide")

# Load data
@st.cache_data
@st.cache_data
def load_data():
    df = pd.read_csv("data/bank_kpi_data.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()  # clean column names
    return df

df = load_data()

df = load_data()

st.title("🏦 Indian Banking KPI Screener (2020–2025)")

# Sidebar filters
st.sidebar.header("🔍 Filter")
banks = st.sidebar.multiselect("Select Banks", sorted(df["bank_name"].unique()), default=["HDFC Bank"])
df["year"] = df["year"].astype(str)
years = st.sidebar.multiselect(
    "Select Years",
    sorted(df["year"].unique(), reverse=True),
    default=["2021", "2020"]
)

metric = st.sidebar.selectbox("Select Metric", [
    "deposits","casa_ratio","aum","gnpa","nnpa","pat","nim","roa",
    "cost_to_income","capital_adequacy_ratio","liquidity_coverage_ratio",
    "retail_mix","wholesale_mix","cost_of_funds","credit_cost"
])

# Filtered data
filtered = df[(df["bank_name"].isin(banks)) & (df["year"].isin(years))]

# Display table
st.subheader("📊 KPI Data")
st.dataframe(filtered.set_index(["bank_name", "year"]))

# Plot metric over time
if not filtered.empty:
    fig = px.line(filtered, x="fiscal_year", y=metric, color="bank_name", markers=True,
                  title=f"{metric.replace('_',' ').title()} Trend")
    fig.update_layout(xaxis_title="Fiscal Year", yaxis_title=metric.replace('_',' ').title())
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected filters.")

st.caption("Data source: Annual Reports, Investor Presentations, and BSE Filings")
