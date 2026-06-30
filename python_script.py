import pandas as pd
import math

today = pd.Timestamp.now()
two_years_ago = today - pd.DateOffset(years=2)
date_range = pd.date_range(start=two_years_ago, end=today, freq='MS')
dates_list = [d.strftime('%Y-%m-%d') for d in date_range]

destinations_list = ['PADD1_NY', 'ARA_Rotterdam', 'Mexico_Tuxpan', 'Brazil_Santos', 'WAF_Lagos', 'Singapore']
components = ['Straight-run Naphtha', 'Reformate', 'Alkylate', 'Butane']

market_dynamics = {
    'PADD1_NY':      {'base': 88.50, 'wave_speed': 2.0, 'offset': 0.0, 'volatility': 4.5, 'freight': 0.51},
    'ARA_Rotterdam': {'base': 86.00, 'wave_speed': 1.8, 'offset': 1.5, 'volatility': 5.2, 'freight': 1.33},
    'Mexico_Tuxpan': {'base': 92.00, 'wave_speed': 2.2, 'offset': 0.7, 'volatility': 3.0, 'freight': 0.12},
    'Brazil_Santos': {'base': 93.50, 'wave_speed': 1.5, 'offset': 2.3, 'volatility': 6.0, 'freight': 1.23},
    'WAF_Lagos':     {'base': 92.75, 'wave_speed': 2.0, 'offset': 3.1, 'volatility': 4.0, 'freight': 1.47},
    'Singapore':     {'base': 87.00, 'wave_speed': 2.5, 'offset': 4.2, 'volatility': 5.5, 'freight': 2.81}
}

master_rows = []

# Compile everything into a single denormalized layout
for dest in destinations_list:
    cfg = market_dynamics[dest]
    for i, date_str in enumerate(dates_list):
        # 1. Market Price calculations
        localized_wave = math.sin((i * cfg['wave_speed']) / 2.0 + cfg['offset']) * cfg['volatility']
        local_drift = ((i + int(cfg['offset'])) % 4) * 0.85
        market_price = round(cfg['base'] + localized_wave + local_drift, 2)
        
        # 2. Shifting recipe blend calculations
        wave = math.sin(i / 3.0)
        ref_frac = round(0.45 + (wave * 0.05), 4)
        alk_frac = round(0.32 - (wave * 0.04), 4)
        but_frac = round(0.07 + (wave * 0.01), 4)
        nap_frac = round(1.0 - (ref_frac + alk_frac + but_frac), 4)
        fractions = [nap_frac, ref_frac, alk_frac, but_frac]
        blend_cost = round(78.45 + (wave * 1.5), 2)
        
        # 3. Write individual rows for each component
        for comp, frac in zip(components, fractions):
            master_rows.append([
                date_str, dest, market_price, cfg['freight'], comp, frac, blend_cost
            ])

df_master_model = pd.DataFrame(master_rows, columns=[
    'Date', 'Destination', 'Market_Spot_Price_bbl', 'Freight_Cost_bbl', 'Component', 'Volume_Fraction', 'Optimized_Blend_Cost_bbl'
])