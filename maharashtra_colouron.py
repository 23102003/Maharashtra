import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Maharashtra Brand Analysis", layout="wide")

# ---------------------------------------------------------
# 1. DATA & CACHING
# ---------------------------------------------------------
@st.cache_data
def get_data():
    data = {
        "District": [
            'AKOLA', 'BULDHANA','WASHIM', 'AURANGABAD', 'BEED', 'JALNA', 'LATUR', 'OSMANABAD',
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
    mah['district'] = mah['district'].str.upper().replace({
        'CHHATRAPATI SAMBHAJINAGAR': 'AURANGABAD', 
        'DHARASHIV': 'OSMANABAD'
    })
    mah['district_upper'] = mah['district']
    mah['district_upper'] = mah['district'].str.upper()
    return mah

# ---------------------------------------------------------
# 2. PROCESSING
# ---------------------------------------------------------
df = get_data()
maharashtra_districts = get_geojson()

st.title("📊 Maharashtra District wise Market Mapping")
target_brand = st.sidebar.selectbox("Select Target Brand", ["Colouron+", "JSW_Radiance", "TATA_Prisma", "Tata_Liner", "TATA_Durashine", "JSW_CC_Liner", "Everglow", "Others"])

brand_cols = ["Colouron+", "JSW_Radiance", "TATA_Prisma", "Tata_Liner", "TATA_Durashine", "JSW_CC_Liner", "Everglow", "Others"]
df['Market_Size'] = df[brand_cols].sum(axis=1)
share_col_name = f'{target_brand} % share'
df[share_col_name] = np.where(df['Market_Size'] == 0, 0, (df[target_brand] / df['Market_Size']) * 100)
df[share_col_name] = df[share_col_name].round(0).astype(int)
# ---------------------------------------------------------
# 3. HOVER LOGIC
# ---------------------------------------------------------
distributor_lookup = {
    'AKOLA': 'Hussain', 'BULDHANA': 'Hussain', 'WASHIM': 'Hussain',
    'AURANGABAD': 'Prince Steel', 'BEED': 'NA',
    'JALNA': 'NA', 'LATUR': 'Prince Steel', 'OSMANABAD': 'NA',
    'HINGOLI': 'NA', 'NANDED': 'NA', 'PARBHANI': 'NA',
    'KOLHAPUR': 'KD Oswal', 'RATNAGIRI': ['KD', 'Yogi'], 'SANGLI': 'Yogi',
    'SATARA': 'Laxmi', 'SINDHUDURG': ['KD', 'Yogi'],
    'SOLAPUR': ['Manmohan', 'Laxmi', 'Yogi'], 'MUMBAI': ['Arihant', 'Khyati'],
    'MUMBAI SUBURBAN': ['Arihant', 'Khyati'], 'PALGHAR': ['Arihant', 'Khyati'],
    'RAIGARH': ['Arihant', 'Khyati'], 'THANE': ['Arihant', 'Khyati'],
    'BHANDARA': ['Yogesh', 'Arvind'], 'CHANDRAPUR': ['Yogesh', 'Arvind'],
    'AMRAVATI': ['Yogesh', 'Arvind'], 'GADCHIROLI': ['Yogesh', 'Arvind'],
    'GONDIA': ['Yogesh', 'Arvind'], 'NAGPUR': ['Yogesh', 'Arvind'],
    'WARDHA': ['Yogesh', 'Arvind'], 'YAVATMAL': ['Yogesh', 'Arvind'],
    'DHULE': ['Manmohan', 'National'], 'JALGAON': ['Manmohan', 'National'],
    'NANDURBAR': ['Manmohan', 'National'], 'NASHIK': 'Manmohan Ispat',
    'PUNE': 'Manmohan Ispat', 'AHMEDNAGAR': 'Jai Associates'
}

# Map this list into your main dataframe
df['Distributors_List'] = df['District'].map(distributor_lookup)


def create_tooltip(row):
    tip = f"<b>{row['District']}</b><br>"
    tip += f"Total Market: {row['Market_Size']} MT<br><br>"
    share = int(row[share_col_name]) if pd.notna(row[share_col_name]) else 0
    tip += f"<b>{target_brand}: {row[target_brand]} MT ({share}%)</b><br><br>"
    tip += "<b>Competition:</b><br>"
    for b in brand_cols:
        if b != target_brand and row[b] > 0:
            b_sh = int((row[b]/row['Market_Size'])*100) if row['Market_Size'] > 0 else 0
            tip += f"{b}: {row[b]} MT ({b_sh}%)<br>"
    tip += "<br><b>Distributors:</b><br>"
    dist_data = row.get('Distributors_List', 'NA')
    
    if isinstance(dist_data, list):
        # If it's a list, loop through and put each on a new line
        for d in dist_data:
            tip += f"{d}<br>"
    elif pd.notna(dist_data) and dist_data != 'NA':
        # If it's a single string
        tip += f"{dist_data}<br>"
    else:
        tip += "NA<br>"
    return tip

df['hover_text'] = df.apply(create_tooltip, axis=1)

def get_m_color(size):
    if size <= 50: return "#dbeafe"
    elif size <= 150: return "#93c5fd"
    elif size <= 300: return "#3b82f6"
    else: return "#1e40af"

def get_s_color(share):
    if share < 25: return "#d32f2f"
    elif share < 50: return "#f57c00"
    elif share < 75: return "#8bc34a"
    else: return "#1b5e20"

df['market_color'] = df['Market_Size'].apply(get_m_color)
df['share_color'] = df[share_col_name].apply(get_s_color)

merged = maharashtra_districts.merge(df, left_on='district_upper', right_on='District', how='left')

cluster_map = {
    'AKOLA': 'Akola', 'BULDHANA': 'Akola', 'WASHIM': 'Akola', 'AMRAVATI': 'Nagpur', 'YAVATMAL': 'Nagpur',
    'AURANGABAD': 'Aurangabad', 'BEED': 'Aurangabad',
    'JALNA': 'Aurangabad', 'LATUR': 'Aurangabad', 'OSMANABAD': 'Aurangabad',
    'HINGOLI': 'Aurangabad', 'NANDED': 'Aurangabad', 'PARBHANI': 'Aurangabad',
    'KOLHAPUR': 'Kolhapur', 'RATNAGIRI': 'Kolhapur', 'SANGLI': 'Kolhapur', 'SATARA': 'Kolhapur',
    'SINDHUDURG': 'Kolhapur', 'SOLAPUR': 'Kolhapur',
    'MUMBAI': 'Mumbai', 'MUMBAI SUBURBAN': 'Mumbai', 'PALGHAR': 'Mumbai', 'RAIGARH': 'Mumbai', 'THANE': 'Mumbai',
    'BHANDARA': 'Nagpur', 'CHANDRAPUR': 'Nagpur', 'GADCHIROLI': 'Nagpur', 'GONDIA': 'Nagpur', 'NAGPUR': 'Nagpur', 'WARDHA': 'Nagpur',
    'DHULE': 'Nashik', 'JALGAON': 'Nashik', 'NANDURBAR': 'Nashik', 'NASHIK': 'Nashik',
    'PUNE': 'Pune', 'AHMEDNAGAR': 'Pune'
}
merged['cluster'] = merged['district_upper'].map(cluster_map)
clusters = merged.dissolve(by='cluster')

# ---------------------------------------------------------
# 4. INTERACTIVE VISUALIZATION
# ---------------------------------------------------------
st.subheader(f"{target_brand} Market Distribution")

fig = go.Figure()

# A. DISTRICT POLYGONS
for _, row in merged.iterrows():
    if row.geometry:
        if row.geometry.geom_type == 'Polygon':
            polys = [row.geometry]
        else:
            polys = row.geometry.geoms
        for poly in polys:
            x, y = poly.exterior.xy
            fig.add_trace(go.Scatter(
                x=list(x), y=list(y),
                fill="toself",
                fillcolor=row['market_color'] if pd.notna(row['market_color']) else 'whitesmoke',
                line=dict(color="#1e293b", width=0.5),
                hoveron='fills',
                text=row['hover_text'],
                hoverinfo='text',
                showlegend=False
            ))

# B. CLUSTER OUTLINES
for _, row in clusters.iterrows():
    if row.geometry.geom_type == 'Polygon':
        polys = [row.geometry]
    else:
        polys = row.geometry.geoms
    for poly in polys:
        x, y = poly.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y),
            line=dict(color="#1e293b", width=2.5),
            hoverinfo='skip',
            showlegend=False,
            mode='lines'
        ))

# C. LABELS AND BOXES (USING ANNOTATIONS FOR TOP LAYER RENDERING)
annotations = []
for _, row in merged.iterrows():
    centroid = row.geometry.centroid
    is_hub = row['district_upper'] == str(row['cluster']).upper()
    share_val = f"{int(row[share_col_name])}%" if pd.notna(row[share_col_name]) else "0%"
    
    # 1. District Name Annotation
    # Calculate coordinates first based on the Hub status
    target_x = centroid.x
    # Use a higher offset if it's a hub (0.15) vs a normal district (0.1)
    target_y = centroid.y + 0.15 if is_hub else centroid.y + 0.1
    
    # Define the display name logic
    display_name = row['district'].upper() if is_hub else row['district']
    
    annotations.append(dict(
        x=target_x, 
        y=target_y,
        text=display_name,
        showarrow=False,
        font=dict(
            size=13 if is_hub else 10, 
            color="black", 
            family="Arial Black" if is_hub else "Arial"
        ),
        xref="x", 
        yref="y"
    ))
    
    # 2. Share % with Rounded Box Annotation
    annotations.append(dict(
        x=centroid.x, y=centroid.y - 0.1,
        text=f"<b>{share_val}</b>",
        showarrow=False,
        font=dict(size=13, color="white"),
        bgcolor=row['share_color'],
        bordercolor="black",
        borderwidth=1,
        borderpad=3,  # Adjusts the "roundness" feel and padding
        xref="x", yref="y"
    ))

annotations.append(dict(
    x=74.74, y=19.3,
    text="<b>AHMEDNAGAR</b>",
    showarrow=False,
    font=dict(size=10, color="black", family="Arial"),
    xref="x", yref="y"
))

# --- TOTAL MARKET BOX (Top Right) ---
# total_mkt_size = df['Market_Size'].sum()

# fig.add_annotation(
#     x=0.99, y=0.99,
#     xref="paper", yref="paper",
#     text=f"<b>Total Premium Market</b><br><span style='font-size:20px;color:#1e40af;'>{total_mkt_size} MT</span>",
#     showarrow=False,
#     align="right",
#     font=dict(size=14, color="Black", family="Arial Black"),
#     bgcolor="rgba(255,255,255,0.8)",
# )
# --- TOTAL MARKET BOX (Top Right) ---
# --- TOTAL MARKET BOX (Bottom Right to avoid overlap) ---
total_mkt_size = df['Market_Size'].sum()
total_brand_vol = df[target_brand].sum()
total_brand_pct = (total_brand_vol / total_mkt_size * 100) if total_mkt_size > 0 else 0

fig.add_annotation(
    x=0.99,   # Keep it on the right side
    y=0.01,   # Move it to the bottom (0 is bottom, 1 is top)
    xref="paper", 
    yref="paper",
    text=(
        f"<b>Total Premium Market</b><br>"
        f"<b><span style='font-size:20px;color:#1e40af;'>{total_mkt_size} MT</span></b><br><br>"
        f"<b>{target_brand} Share</b><br>"
        f"<b><span style='font-size:18px;color:#1b5e20;'>{total_brand_vol} MT ({total_brand_pct:.0f}%)</span></b>"
    ),
    showarrow=False,
    align="right",
    font=dict(size=14, color="Black", family="Arial Black"),
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="black",
    borderwidth=1,
    borderpad=10
)

# 1. Market Size Legend (Circles/Squares)
market_ranges = [
    ('0–50 MT', '#dbeafe'), ('50–0 MT', '#93c5fd'), 
    ('150–300 MT', '#3b82f6'), ('300-650 MT', '#1e40af')
]

for label, color in market_ranges:
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers',
        marker=dict(size=10, color=color, symbol='square'),
        legendgroup="Market", legendgrouptitle_text="Market Size (MT)",
        name=label, showlegend=True
    ))

# 2. Share % Legend
share_ranges = [
    ('> 75%', '#1b5e20'), ('50–75%', '#8bc34a'), 
    ('25–50%', '#f57c00'), ('< 25%', '#d32f2f')
]

for label, color in share_ranges:
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers',
        marker=dict(size=10, color=color, symbol='square'),
        legendgroup="Share", legendgrouptitle_text=f"{target_brand} Share %",
        name=label, showlegend=True
    ))

# Final Layout Update
fig.update_layout(
    annotations=annotations,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
    plot_bgcolor='white',
    margin=dict(l=0, r=0, t=0, b=0),
    height=600,
    showlegend=True,
    legend=dict(
        x=0.01,
        y=0.99,
        # Move it here:
        grouptitlefont=dict(color="black"), 
        bgcolor="rgba(255,255,255,0.8)", 
        bordercolor="Black",
        borderwidth=0,
        font=dict(size=12, color="black"), 
        title_font_family="Arial Black",
        itemsizing='constant'
    )
)

st.plotly_chart(fig, use_container_width=True)

# # ---------------------------------------------------------
# # 5. TABLES (Unchanged)
# # ---------------------------------------------------------
# st.divider()
# t1, t2 = st.tabs([f"--- Districts with High {target_brand} Share (50%+) ---", f"--- Competitive Analysis: Low {target_brand} Share States ---"])

# with t1:
#     high_share_table = df[df[share_col_name] >= 50][['District', share_col_name, target_brand, 'Market_Size']].sort_values(by=share_col_name, ascending=False).reset_index(drop=True)
#     high_share_table.columns = ['District',share_col_name, f'{target_brand} (MT)', 'Total Market (MT)']
#     st.dataframe(high_share_table, use_container_width=True)

# with t2:
#     comp_cols = ["TATA_Prisma", "Tata_Liner", "TATA_Durashine", "Others"]
#     low_share_df = df[df[share_col_name] < 50].copy()
#     low_share_df['Top Competitor'] = low_share_df[comp_cols].idxmax(axis=1)
#     low_share_df['Comp Vol (MT)'] = low_share_df[comp_cols].max(axis=1)
#     low_share_df['Comp Share %'] = np.where(
#         low_share_df['Market_Size'] == 0, 0, (low_share_df['Comp Vol (MT)'] / low_share_df['Market_Size']) * 100
#     ).round(0).astype(int)
#     low_share_table = low_share_df[['District', f'{target_brand} % share', 'Top Competitor', 'Comp Share %', 'Comp Vol (MT)', 'Market_Size']].sort_values(by=share_col_name).reset_index(drop=True)
#     st.dataframe(low_share_table, use_container_width=True)

# ---------------------------------------------------------
# 6. DYNAMIC KEY FOCUS AREAS (FINAL FORMATTING)
# ---------------------------------------------------------
st.divider()
st.subheader(f"📍 Key Focus Areas: {target_brand} Share < 50%")

# 1. Filter and Sort
focus_df = merged[merged[share_col_name] < 50].copy()
focus_df = focus_df.sort_values(by=['cluster', share_col_name], ascending=[True, True])

# 2. Format columns
focus_df['Share_Display'] = focus_df.apply(lambda x: f"{int(x[target_brand])} MT ({int(x[share_col_name])}%)", axis=1)
focus_df['Market_Size_Display'] = focus_df['Market_Size'].apply(lambda x: f"{int(x)} MT")

# 3. Prepare display dataframe
display_df = focus_df[['cluster', 'district', 'Share_Display', 'Market_Size_Display']].copy()
display_df.columns = ['Cluster', 'Districts', f'{target_brand} Share', 'Total Market']
display_df['Districts'] = display_df['Districts'].str.title()

# 4. Track cluster changes
is_new_cluster = ~display_df['Cluster'].duplicated()
display_df['Cluster'] = np.where(display_df['Cluster'].duplicated(), "", display_df['Cluster'])

# 5. Styling to kill Index and White Spaces
def style_final_table(st_df):
    styled = st_df.style.set_table_styles([
        {
            'selector': '', 
            'props': [
                ('border-collapse', 'collapse !important'), 
                ('border-spacing', '0 !important'),
                ('width', 'auto'),
                ('margin-left', '0'),
                ('margin-right', 'auto')
            ]
        },
        {
            'selector': 'th',
            'props': [
                ('background-color', '#b8cce4'), 
                ('color', 'black'), 
                ('border', '1px solid black'), 
                ('font-weight', 'bold'), 
                ('padding', '2px 5px')
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('padding', '2px 10px'), 
                ('color', 'black'), 
                ('border-left', '1px solid black'), 
                ('border-right', '1px solid black'), 
                ('border-bottom', 'none'), 
                ('border-top', 'none'),
                ('margin', '0'),
                ('border-collapse', 'collapse')
            ]
        }
    ]).hide(axis="index") # CRITICAL: This removes the numbered column

    # Apply top border only when cluster changes
    for i, row_is_new in enumerate(is_new_cluster):
        if row_is_new:
            styled.set_table_styles({
                display_df.index[i]: [{'selector': 'td', 'props': [('border-top', '1px solid black')]}]
            }, overwrite=False, axis=1)
    
    # Bottom border for the last row
    styled.set_table_styles({
        display_df.index[-1]: [{'selector': 'td', 'props': [('border-bottom', '1px solid black')]}]
    }, overwrite=False, axis=1)
    
    return styled
    
# st.table(style_final_table(display_df))
st.markdown(style_final_table(display_df).to_html(), unsafe_allow_html=True)
