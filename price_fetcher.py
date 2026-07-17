import datetime
import yfinance as yf
import pandas as pd

# 1. Dynamically anchor the start date to Jan 1st of 2 years ago
current_year = datetime.datetime.now().year
start_date = f"{current_year - 2}-01-01" 

print(f"Fetching historical WTI and RBOB daily prices starting exactly from: {start_date}...")

# 2. Fetch daily data starting from the anchor point
wti_raw = yf.Ticker("CL=F").history(start=start_date)['Close']
rbob_raw = yf.Ticker("RB=F").history(start=start_date)['Close']

df_daily = pd.DataFrame({
    'WTI_Crude': wti_raw, 
    'RBOB_Gasoline': rbob_raw * 42  # Convert gallons to barrels ($/bbl)
})

# Forward-fill weekend gaps to keep the timeline continuous
df_daily = df_daily.ffill().dropna().reset_index()
df_daily['Date'] = df_daily['Date'].dt.strftime('%Y-%m-%d')

output_path = r"C:\Users\filip\OneDrive\Desktop\Refinery_Optimizer_Project\live_prices.csv"
df_daily.to_csv(output_path, index=False)
print(f"Anchored daily database saved successfully to {output_path}!")