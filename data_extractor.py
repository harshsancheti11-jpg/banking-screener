import pandas as pd
import requests

def get_bank_data(bse_code):
    """Fetch recent financial KPIs from BSE site."""
    url = f"https://www.bseindia.com/corporates/Comp_Results.aspx?Code={bse_code}&ID=finresults"
    tables = pd.read_html(url)
    
    # Try to find P&L table
    for table in tables:
        if 'Total Income' in str(table.columns) or 'Total Income' in str(table.values):
            df = table
            break
    else:
        return None
    
    df.columns = [str(c).strip() for c in df.columns]
    df = df.head(10)
    return df
