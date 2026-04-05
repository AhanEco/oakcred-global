import wbgapi as wb
import pandas as pd
import os

# Define Indicators
INDICATORS = {
    'FP.CPI.TOTL.ZG': 'inflation',
    'DT.DOD.DECT.GN.ZS': 'external_debt_gni',
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth',
    'BX.KLT.DINV.WD.GD.ZS': 'fdi_net_inflows_gdp',
    'FI.RES.TOTL.CD': 'total_reserves',
    'BN.CAB.XOKA.GD.ZS': 'current_account_gdp'
}

# Define Economies (G20 + Significant EM)
ECONOMIES = [
    'ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'FRA', 'DEU', 'IND', 'IDN', 'ITA', 
    'JPN', 'KOR', 'MEX', 'RUS', 'SAU', 'ZAF', 'TUR', 'GBR', 'USA',
    'VNM', 'EGY', 'NGA', 'BGD', 'PAK', 'PHL', 'KEN', 'KEN', 'ETH'
]

def fetch_macro_data():
    print("Fetching World Bank Data...")
    
    # Fetch data as a DataFrame with series as columns
    # Source 2 is World Development Indicators
    df = wb.data.DataFrame(INDICATORS.keys(), economy=ECONOMIES, time=range(2015, 2024), columns='series')
    
    # Rename columns using our mapping
    df = df.rename(columns=INDICATORS)
    
    # Reset index to turn 'economy' and 'time' into columns
    df = df.reset_index()
    
    # Clean 'time' column (YR2015 -> 2015)
    df['year'] = df['time'].str.replace('YR', '').astype(int)
    df = df.drop(columns=['time'])
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/macro_data.csv', index=False)
    print(f"Data saved to data/macro_data.csv. Total records: {len(df)}")
    return df

if __name__ == "__main__":
    fetch_macro_data()
