import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- PAGE SETUP ---
st.set_page_config(page_title="Banking Sector Screener", layout="wide")

st.title("🏦 Indian Banking Sector Screener (2020–2025)")
st.caption("Auto-updating financial and operational data sourced from BSE.")

# --- FETCHING DATA ---
@st.cache_data
def fetch_bse_data(stock_code):
    try:
        url = f"https://www.bseindia.com/corporates/results.aspx?Code={stock_code}&Company=&qtr=109.50"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate financial tables
        tables = soup.find_all("table")
        if not tables:
            return pd.DataFrame(), f"No data found for BSE code {stock_code}."

        dataframes = []
        for table in tables:
            try:
                df = pd.read_html(str(table))[0]
                if df.shape[1] > 2:
                    dataframes.append(df)
            except:
                continue

        if not dataframes:
            return pd.DataFrame(), f"No readable tables found for {stock_code}."
        
        final_df = pd.concat(dataframes)
        return final_df, "Success"
    except Exception as e:
        return pd.DataFrame(), str(e)

# --- BANKING STOCKS LIST ---
bank_stocks = {
    "HDFC Bank": "500180",
    "ICICI Bank": "532174",
    "Axis Bank": "532215",
    "Kotak Mahindra Bank": "500247",
    "IndusInd Bank": "532187"
}

selected_bank = st.selectbox("Select a Bank:", list(bank_stocks.keys()))

if st.button("Fetch Data"):
    with st.spinner(f"Fetching {selected_bank} financials..."):
        df, msg = fetch_bse_data(bank_stocks[selected_bank])

    if not df.empty:
        st.success("Data successfully extracted!")
        st.dataframe(df, use_container_width=True)
    else:
        st.error(msg)

st.markdown("---")
st.caption("Data auto-updated from BSE India • Built with ❤️ using Streamlit.")
