import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch

# Set page config
st.set_page_config(page_title="Maharashtra Brand Analysis", layout="wide")

# ---------------------------------------------------------
# 1. DATA & CACHING
# ---------------------------------------------------------
@st.cache_data
def get_data():
    data = {
        "District": [
            'AKOLA', 'BULDHANA','WASHIM', 'CHHATRAPATI SAMBHAJINAGAR', 'BEED', 'JALNA', 'LATUR', 'DHARASHIV',
            'HINGOLI', 'NANDED','PARBHANI', 'KOLHAPUR', 'RATNAGIRI', 'SANGLI', 'SATARA', 'SINDHUDURG',
            'SOLAPUR','MUMBAI', 'MUMBAI SUBURBAN', 'PALGHAR', 'RAIGARH','THANE',
            'BHANDARA', 'CHANDRAPUR', 'AMRAVATI', 'GADCHIROLI', 'GONDIA', 'NAGPUR', 'WARDHA',
            'YAVATMAL', 'DHULE', 'JALGAON', 'NANDURBAR', 'NASHIK', 'PUNE', 'AHMEDNAGAR'
        ],
        "Colouron+": [5, 0, 0, 25, 0, 0, 15, 0, 0, 0, 0, 150, 75, 100, 75, 75, 0, 150, 0, 325, 500, 450, 5, 5, 5, 0, 10, 163, 0, 0, 0, 20, 0, 75, 250, 50],
        "Everglow": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "JSW_Radiance": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0],
        "TATA_Prisma": [5, 0, 0, 25, 15, 10, 15, 0, 10, 3, 0, 25, 10, 25, 10, 10, 5, 50, 15, 25, 15, 25, 2, 0, 5, 0, 5, 10, 0, 0, 0, 15, 0, 40, 125, 20],
        "Tata_Liner": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "TATA_Durashine": [15, 5, 5, 150, 35, 10, 50, 10, 50, 7, 10, 100, 25, 75, 25, 15, 25, 100, 35, 75, 75, 75, 0, 0, 10, 0, 0, 150, 0, 0, 25, 50, 15, 75, 150, 50],
        "JSW_CC_Liner": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Others": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 50, 0, 0, 0, 25, 0, 25, 0, 25, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 25, 100, 0]
    }
    return pd.DataFrame(data)

@st.cache_data
def get_geojson():
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/INDIA/INDIA_DISTRICTS.geojson"
    india = gpd.read_file(url)
    mah = india[india['state'].str.upper() == 'MAHARASHTRA'].copy()
    mah['district_upper'] = mah['district'].str.upper()
    return mah

# ---------------------------------------------------------
# 2. PROCESSING
# ---------------------------------------------------------
df = get_data()
maharashtra_districts = get_geojson()

st.title("📊 Maharashtra Performance Dashboard")
target_brand = st.sidebar.selectbox("Select Target Brand", ["Colouron+", "JSW_Radiance", "TATA_Prisma", "Tata_Liner", "TATA_Durashine", "JSW_CC_Liner", "Everglow", "Others"])

brand_cols = ["Colouron+", "JSW_Radiance", "TATA_Prisma", "Tata_Liner", "TATA_Durashine", "JSW_CC_Liner", "Everglow", "Others"]
df['Market_Size'] = df[brand_cols].sum(axis=1)
share_col_name = f'{target_brand} % share'
df[share_col_name] = np.where(df['Market_Size'] == 0, 0, (df[target_brand] / df['Market_Size']) * 100)
df[share_col_name] = df[share_col_name].round(0).astype(int)

# Colors
def get_market_color(size):
    if size <= 50: return "#dbeafe"
    elif size <= 150: return "#93c5fd"
    elif size <= 300: return "#3b82f6"
    else: return "#1e40af"

def get_share_color(share):
    if share < 25: return "#d32f2f"
    elif share < 50: return "#f57c00"
    elif share < 75: return "#8bc34a"
    else: return "#1b5e20"

df['market_color'] = df['Market_Size'].apply(get_market_color)
df['share_color'] = df[share_col_name].apply(get_share_color)

# Merge
merged = maharashtra_districts.merge(df, left_on='district_upper', right_on='District', how='left')

# ---------------------------------------------------------
# 3. VISUALIZATION
# ---------------------------------------------------------
st.subheader(f"{target_brand} Market Distribution")

cluster_map = {
    'AKOLA': 'Akola', 'BULDHANA': 'Akola', 'WASHIM': 'Akola', 'AMRAVATI': 'Nagpur', 'YAVATMAL': 'Nagpur',
    'CHHATRAPATI SAMBHAJINAGAR': 'Chhatrapati Sambhajinagar', 'BEED': 'Chhatrapati Sambhajinagar',
    'JALNA': 'Chhatrapati Sambhajinagar', 'LATUR': 'Chhatrapati Sambhajinagar', 'DHARASHIV': 'Chhatrapati Sambhajinagar',
    'HINGOLI': 'Chhatrapati Sambhajinagar', 'NANDED': 'Chhatrapati Sambhajinagar', 'PARBHANI': 'Chhatrapati Sambhajinagar',
    'KOLHAPUR': 'Kolhapur', 'RATNAGIRI': 'Kolhapur', 'SANGLI': 'Kolhapur', 'SATARA': 'Kolhapur',
    'SINDHUDURG': 'Kolhapur', 'SOLAPUR': 'Kolhapur',
    'MUMBAI': 'Mumbai', 'MUMBAI SUBURBAN': 'Mumbai', 'PALGHAR': 'Mumbai', 'RAIGARH': 'Mumbai', 'THANE': 'Mumbai',
    'BHANDARA': 'Nagpur', 'CHANDRAPUR': 'Nagpur', 'GADCHIROLI': 'Nagpur', 'GONDIA': 'Nagpur', 'NAGPUR': 'Nagpur', 'WARDHA': 'Nagpur',
    'DHULE': 'Nashik', 'JALGAON': 'Nashik', 'NANDURBAR': 'Nashik', 'NASHIK': 'Nashik',
    'PUNE': 'Pune', 'AHMEDNAGAR': 'Pune'
}
# Apply cluster map to the merged dataframe for plotting
merged['cluster'] = merged['district_upper'].map(cluster_map)
clusters = merged.dissolve(by='cluster')

# 4. PLOTTING
fig, ax = plt.subplots(figsize=(15, 12))

# Plot Districts
for idx, row in merged.iterrows():
    color = row['market_color'] if pd.notna(row['market_color']) else 'whitesmoke'
    gpd.GeoSeries(row.geometry).plot(ax=ax, color=color, edgecolor='gray', linewidth=0.4)

# Plot Cluster Outlines
clusters.geometry.boundary.plot(ax=ax, color='black', linewidth=2.0)

# Add Labels, Bubbles, and Cluster Highlights
for idx, row in merged.iterrows():
    if row.geometry is not None and not row.geometry.is_empty:
        centroid = row.geometry.centroid
        dist_name = row['district']
        cluster_name = str(row['cluster'])

        # CHECK: Is this district the "Capital/Name-bearer" of the cluster?
        if dist_name.upper() == cluster_name.upper():
            # HIGHLIGHT STYLE for Cluster Hubs
            ax.text(centroid.x, centroid.y + 0.12, dist_name.upper(),
                    fontsize=13, ha='center', color='black', fontweight='bold',
                    alpha=0.8, zorder=10)
        else:
            # REGULAR STYLE for other districts
            ax.text(centroid.x, centroid.y + 0.08, dist_name,
                    fontsize=8, ha='center', color='black')

        # Share % Bubble
        share_val = f"{int(row[share_col_name])}%" if pd.notna(row[share_col_name]) else "0%"
        ax.text(centroid.x, centroid.y - 0.05, share_val, fontsize=11, ha='center', va='center',
                color='white', fontweight='black',
                bbox=dict(facecolor=row['share_color'], edgecolor='black', boxstyle='round,pad=0.6'))


# --- LEGEND SECTION ---
market_legend_elements = [
    Patch(facecolor='#dbeafe', label='0–50 MT'),
    Patch(facecolor='#93c5fd', label='50–150 MT'),
    Patch(facecolor='#3b82f6', label='150–300 MT'),
    Patch(facecolor='#1e40af', label='300-650 MT')
]
legend1 = ax.legend(handles=market_legend_elements,
                    title="Market Size (MT)",
                    loc="upper left",
                    bbox_to_anchor=(0.005, 0.98),
                    frameon=False)
ax.add_artist(legend1)

share_legend_elements = [
    Patch(facecolor='#1b5e20', label='> 75%'),
    Patch(facecolor='#8bc34a', label='50–75%'),
    Patch(facecolor='#f57c00', label='25–50%'),
    Patch(facecolor='#d32f2f', label='< 25%')
]

ax.legend(handles=share_legend_elements,
          title=f"{target_brand} Share %",
          loc="upper left",
          bbox_to_anchor=(0.005, 0.85),
          frameon=False,
          markerfirst=True,
          alignment="left")

ax.axis('off')
st.pyplot(fig)


# ---------------------------------------------------------
# 4. TABLES
# ---------------------------------------------------------
st.divider()
t1, t2 = st.tabs([f"--- Districts with High {target_brand} Share (50%+) ---", f"--- Competitive Analysis: Low {target_brand} Share States ---"])

with t1:
    high_share_table = df[df[share_col_name] >= 50][['District', share_col_name, target_brand, 'Market_Size']].sort_values(by=share_col_name, ascending=False).reset_index(drop=True)
    high_share_table.columns = ['District',share_col_name, f'{target_brand} (MT)', 'Total Market (MT)']
    st.dataframe(high_share_table.sort_values(share_col_name, ascending=False), use_container_width=True)

with t2:
    comp_cols = ["TATA_Prisma", "Tata_Liner", "TATA_Durashine", "Others"]
    low_share_df = df[df[share_col_name] < 50].copy()
    low_share_df['Top Competitor'] = low_share_df[comp_cols].idxmax(axis=1)
    low_share_df['Comp Vol (MT)'] = low_share_df[comp_cols].max(axis=1)
    low_share_df['Comp Share %'] = np.where(
    low_share_df['Market_Size'] == 0,0,(low_share_df['Comp Vol (MT)'] / low_share_df['Market_Size']) * 100).round(0).astype(int)
    low_share_table = low_share_df[
    ['District', f'{target_brand} % share', 'Top Competitor', 'Comp Share %', 'Comp Vol (MT)', 'Market_Size']].sort_values(by=share_col_name).reset_index(drop=True)
    st.dataframe(low_share_table[['District',  f'{target_brand} % share', 'Top Competitor', 'Comp Share %', 'Comp Vol (MT)', 'Market_Size']], use_container_width=True)
