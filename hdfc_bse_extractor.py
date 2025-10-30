import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_bse_data(stock_code="500180"):
    """
    Fetches 5-year financial and key ratio data from BSE for given stock code.
    HDFC Bank’s BSE code: 500180
    """
    base_url = f"https://www.bseindia.com/corporates/results.aspx?Code={stock_code}&Company=HDFC%20Bank%20Ltd.&qtr=109.50"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch BSE page, status {response.status_code}")

    soup = BeautifulSoup(response.text, "lxml")

    # find all tables
    tables = soup.find_all("table")

    if not tables:
        print("No tables found. The structure may have changed.")
        return None

    data_frames = []
    for i, table in enumerate(tables):
        df = pd.read_html(str(table))[0]
        df = df.dropna(how="all")
        df.columns = [col.strip() for col in df.columns]
        data_frames.append(df)

    # Combine all tables into one Excel
    with pd.ExcelWriter("HDFC_Bank_BSE_Data.xlsx", engine="openpyxl") as writer:
        for idx, df in enumerate(data_frames):
            sheet_name = f"Sheet_{idx+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("✅ Data extracted and saved to 'HDFC_Bank_BSE_Data.xlsx' at", datetime.now())

if __name__ == "__main__":
    fetch_bse_data()
