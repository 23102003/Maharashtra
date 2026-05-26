import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Regional Brand Analysis", layout="wide")

# ---------------------------------------------------------
# 1. DATA & CACHING
# ---------------------------------------------------------
@st.cache_data
def get_state_data(state_name):
    # MAHARASHTRA DATA
    if state_name == "Maharashtra":
        data = {
            "District": [
            'AKOLA', 'BULDHANA','WASHIM', 'AURANGABAD', 'BEED', 'JALNA', 'LATUR', 'OSMANABAD',
            'HINGOLI', 'NANDED','PARBHANI', 'KOLHAPUR', 'RATNAGIRI', 'SANGLI', 'SATARA', 'SINDHUDURG',
            'SOLAPUR','MUMBAI', 'MUMBAI SUBURBAN', 'PALGHAR', 'RAIGARH','THANE',
            'BHANDARA', 'CHANDRAPUR', 'AMRAVATI', 'GADCHIROLI', 'GONDIA', 'NAGPUR', 'WARDHA',
            'YAVATMAL', 'DHULE', 'JALGAON', 'NANDURBAR', 'NASHIK', 'PUNE', 'AHMEDNAGAR'
        ],      
        "Indradhanush": [30,50,30,250,50,50,400,25,25,275,25,500,50,650,150,0,200,400,0,600,1000,950,10,30,30,15,15,1202,10,30,100,300,50,350,1250,250],
        "AM/NS": [150,100,50,550,300,550,575,55,75,200,75,100,0,500,700,0,500,700,500,50,50,150,40,70,700,80,50,200,500,50,200,500,50,300,3500,100],
        "Nepal": [0]*36,
        "Colorshine": [0]*36,
        "Supreme": [0]*36,
        "Rhino": [0]*36,
        "Geo Roofing": [0]*36,
        "Manaksia": [0]*36,  
        "Jindal Rangeen": [0]*36,    
        "Jindal Prajapati": [0]*36,  
        "Latim": [0]*36,
        "Dyna": [0]*36, 
        "APL Navrang": [0]*36,
        "Shyam Metallics":       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,0,0,0,0,0,0,0,0,0],
        "Kamdhenu":              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,50,0,0,0,0,0,0,0,0,0],
         "Others":       [60,30,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,50,20,50,100,500,50,50,0,0,0,0,0,0], }
       
    
    # GUJARAT DATA (Placeholder - Replace with your actual data)
    elif state_name == "Gujarat":
        data = {
            "District": [
                'AHMADABAD', 'ANAND', 'GANDHINAGAR', 'KHEDA', 'AMRELI', 'BHAVNAGAR', 'BOTAD', 'GIR SOMNATH', 'JUNAGADH', 'PORBANDAR',
                'JAMNAGAR', 'KACHCHH', 'MORBI', 'ARVALLI', 'BANAS KANTHA', 'MAHESANA', 'PATAN', 'SABAR KANTHA', 'DEVBHUMI DWARKA', 'RAJKOT','SURENDRANAGAR',
                'DANG', 'NAVSARI', 'SURAT', 'TAPI', 'VALSAD', 'BHARUCH', 'CHHOTAUDEPUR', 'DOHAD', 'MAHISAGAR', 'NARMADA', 'PANCH MAHALS', 'VADODARA'
            ],
            "Indradhanush": [600, 40, 0, 40, 0, 50, 50, 0, 50, 50, 10, 100, 20, 50, 90, 300, 40, 50, 0, 200, 100, 0, 0, 300, 0, 100, 40, 0, 50, 50, 0, 20, 300],
            "AM/NS": [2400, 150, 200, 100, 80, 110, 40, 60, 120, 25, 300, 110, 150, 5, 50, 100, 20, 40, 0, 800, 100, 2, 4, 500, 2, 200, 80, 5, 40, 25, 1, 60, 170],
            "Nepal": [0]*33,
            "colorshine": [0]*33,
            "Supreme": [0]*33,
            "Rhino": [0]*33,
            "Geo Roofing": [0]*33,
            "Manaksia":  [40,40,40,0,0,0,0,0,0,0,30,30,30,0,0,0,0,0,0,0,0,10,10,0,20,0,5,0,10,0,0,0,20],
            "Latim": [0]*33,
            "Kamdhenu": [0]*33,
            "Jindal Prajapati": [0]*33,  
            "Dyna": [0]*33, 
            "APL Navrang": [0]*33,
            "Shyam Metallics":         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10],
            "Jindal Rangeen":         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,5,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,15],
            "Others":         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,10,10,0,25,100], }

           
    elif state_name == "Punjab":
        data = {
            "District": [
                'AMRITSAR', 'GURDASPUR', 'HOSHIARPUR', 'JALANDHAR', 'KAPURTHALA', 
                'PATHANKOT', 'SHAHID BHAGAT SINGH NAGAR', 'TARN TARAN', 'BARNALA', 
                'FATEHGARH SAHIB', 'LUDHIANA', 'MALER KOTLA', 'MANSA', 'PATIALA', 
                'RUPNAGAR', 'S.A.S NAGAR', 'SANGRUR', 'BATHINDA', 'FARIDKOT', 
                'FAZILKA', 'FIROZPUR', 'MOGA', 'SRI MUKTSAR SAHIB'
            ],
            "Indradhanush": [0, 0, 0, 500, 20, 60, 0, 60, 60, 380, 550, 10, 10, 10, 0, 0, 0, 10, 10, 10, 20, 10, 10],
            "AM/NS": [10, 0, 10, 100, 15, 10, 5, 10, 0, 20, 100, 10, 5, 5, 0, 5, 5, 10, 0, 10, 5, 5, 5],
            "Jindal Prajapati": [10, 0, 5, 20, 5, 5, 5, 0, 0, 40, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Manaksia": [0, 0, 0, 50, 5, 10, 5, 0, 0, 70, 80, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 10],
            "Latim": [0, 0, 0, 10, 0, 5, 0, 5, 0, 10, 10, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Kamdhenu": [0, 0, 0, 20, 10, 5, 5, 10, 5, 20, 50, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 10, 0],
            "Nepal": [0]*23,
            "colorshine": [0]*23,
            "Jindal Rangeen": [0]*23, 
            "APL Navrang": [0]*23,  
            "Supreme": [0]*23,
            "Rhino": [0]*23,
            "Dyna": [0]*23,  
            "Geo Roofing": [0]*23,
            "Shyam Metallics": [0]*23,
            "Others": [0]*23
        }
    elif state_name == "Jammu and Kashmir":
        data = {
            "District": [
                'DODA', 'JAMMU', 'KATHUA', 'KISHTWAR', 'PUNCH', 
                'RAJAURI', 'RAMBAN', 'RIASI', 'SAMBA', 'UDHAMPUR', 
                'SHUPIYAN', 'ANANTNAG', 'BANDIPURA', 'BARAMULA', 'BADGAM', 
                'GANDERBAL', 'KUPWARA', 'KULGAM', 'PULWAMA', 'SRINAGAR'
            ],
           "Indradhanush": [0, 30, 0, 0, 0, 0, 0, 0, 0, 20, 0, 20, 20, 20, 0, 0, 0, 0, 0, 40],
            "Manaksia": [0, 30, 0, 0, 20, 0, 0, 0, 0, 20, 0, 50, 30, 20, 0, 0, 0, 0, 0, 60],
            "Latim": [0, 20, 0, 0, 0, 0, 0, 0, 10, 0, 0, 30, 20, 10, 0, 0, 10, 0, 10, 40],
            "Kamdhenu": [0, 20, 20, 0, 0, 10, 0, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20],
            "Shyam Metallics": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 0, 0, 0, 0, 0, 40],
            "AM/NS": [10, 40, 30, 10, 10, 0, 0, 10, 20, 20, 30, 100, 30, 100, 50, 30, 40, 30, 40, 200],
            "Jindal Rangeen": [0, 20, 10, 10, 10, 10, 10, 10, 20, 20, 0, 20, 0, 20, 10, 0, 0, 0, 0, 20],            
            "Nepal": [0]*20,
            "colorshine": [0]*20,
            "Supreme": [0]*20,
            "Rhino": [0]*20,
            "Geo Roofing": [0]*20,
            "APL Navrang": [0]*20,  
            "Jindal Prajapati": [0]*20,  
            "Dyna": [0]*20,  
            "Others": [0]*20
        }
    elif state_name == "Uttar Pradesh":
        data = {
            "District": [
                'AGRA', 'ALIGARH', 'ETAH', 'FIROZABAD', 'HATHRAS', 'KASGANJ', 'MAINPURI', 'MATHURA',
                'AMROHA', 'BAREILLY', 'BIJNOR', 'BUDAUN', 'PILIBHIT', 'RAMPUR', 'SAMBHAL', 'SHAHJAHANPUR',
                'BAGHPAT', 'BULANDSHAHR', 'GAUTAM BUDDHA NAGAR', 'GHAZIABAD', 'HAPUR', 'MEERUT', 'MUZAFFARNAGAR',
                'SAHARANPUR', 'SHAMLI', 'MORADABAD', 'AYODHYA', 'AZAMGARH', 'BAHRAICH', 'BALLIA', 'BASTI',
                'DEORIA', 'GONDA', 'GORAKHPUR', 'KUSHINAGAR', 'MAHRAJGANJ', 'MAU', 'SHRAWASTI',
                'SIDDHARTHNAGAR', 'SULTANPUR', 'AURAIYA', 'BANDA', 'CHITRAKOOT', 'ETAWAH', 'FARRUKHABAD',
                'JALAUN', 'JHANSI', 'KANNAUJ', 'KANPUR DEHAT', 'KANPUR NAGAR', 'LALITPUR', 'MAHOBA',
                'BARA BANKI', 'HARDOI', 'KHERI', 'LUCKNOW', 'RAE BARELI', 'SITAPUR', 'UNNAO', 'BHADOHI',
                'CHANDAULI', 'FATEHPUR', 'GHAZIPUR', 'JAUNPUR', 'KAUSHAMBI', 'MIRZAPUR', 'PRAYAGRAJ',
                'SONBHADRA', 'VARANASI'
            ],  
   
            "Indradhanush": [
                60, 5, 6, 40, 15, 3, 2, 40, 5, 10, 6, 5, 2, 2, 3, 10, 8, 7, 80, 325,
                3, 18, 47, 5, 3, 3, 3, 5, 3, 8, 10, 12, 7, 17, 5, 4, 7, 4, 7, 4,
                17, 12, 12, 8, 20, 25, 75, 9, 9, 35, 45, 10, 25, 20, 13, 25, 25, 6,     18, 10,
                12, 15, 13, 10, 16, 27, 16, 21, 50
            ],

           "AM/NS": [
                20, 0, 2, 10, 5, 0, 0, 10, 0, 3, 0, 0, 0, 0, 0, 3, 2, 2, 23, 105,
                0, 6, 12, 0, 0, 0, 3, 4, 5, 12, 2, 3, 5, 18, 2, 2, 3, 2, 2, 2,
                15, 14, 10, 9, 20, 26, 50, 25, 12, 20, 30, 14, 20, 16, 16, 20, 30, 4, 6, 9,
                7, 6, 7, 6, 3, 6, 15, 6, 16
            ],

            "Dyna": [
                60, 4, 6, 30, 15, 3, 2, 30, 4, 10, 5, 4, 2, 1, 0, 10, 7, 6, 70, 315,
                3, 18, 36, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
           "Manaksia": [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                40, 0, 0, 100, 0, 60, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            "Latim": [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 12, 0
            ],
           "APL Navrang": [
                90, 9, 12, 40, 30, 6, 2, 40, 9, 20, 10, 9, 3, 1, 5, 21, 15, 13, 108, 530,
                6, 36, 74, 9, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
           "Jindal Rangeen": [
                40, 5, 6, 20, 15, 3, 2, 20, 5, 10, 6, 5, 2, 2, 3, 10, 8, 7, 40, 215,
                3, 18, 37, 5, 3, 3, 8, 10, 6, 13, 13, 5, 7, 30, 7, 7, 15, 5, 6, 10,
                2, 3, 4, 10, 5, 8, 20, 5, 7, 17, 13, 5, 4, 4, 4, 17, 12, 5, 4, 7,
                10, 3, 6, 11, 4, 4, 50, 10, 65
            ],
            "Nepal": [0]*69,
            "colorshine": [0]*69,
            "Supreme": [0]*69,
            "Rhino": [0]*69,
            "Geo Roofing": [0]*69,
            "Kamdhenu": [0]*69,
            "Jindal Prajapati": [0]*69,
            "Shyam Metallics": [0]*69,
            "Others": [
                130, 7, 8, 70, 20, 5, 0, 70, 8, 16, 8, 7, 2, 0, 5, 16, 10, 10, 150,      620, 5, 24, 50, 7, 5, 5, 24, 22, 16, 26, 18, 16, 20, 108, 19, 15, 12, 13, 12, 13, 35,
                25, 25, 16, 40, 16, 135, 16, 16, 50, 70, 20, 50, 40, 25, 50, 100, 15, 40, 22, 18, 16, 30, 17, 16, 25, 90, 8, 120
            ],
        }
    elif state_name == "Haryana":
        data = {
            "District": [
                'FARIDABAD', 'GURUGRAM', 'MAHENDRAGARH', 'NUH', 'PALWAL', 'REWARI', 
                'BHIWANI', 'FATEHABAD', 'HISAR', 'JIND', 'SIRSA', 'AMBALA', 'KAITHAL', 
                'KURUKSHETRA', 'PANCHKULA', 'YAMUNANAGAR', 'CHARKI DADRI', 'JHAJJAR', 
                'KARNAL', 'PANIPAT', 'ROHTAK', 'SONIPAT'
            ],

            "Indradhanush": [90, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],   
            "AM/NS": [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Jindal Rangeen": [100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Nepal": [0]*22,
            "Colorshine": [0]*22,
            "Rhino": [0]*22,
            "Supreme": [0]*22,
            "Geo Roofing": [0]*22,
            "Dyna": [0]*22,
            "APL Navrang": [0]*22,
            "Jindal Prajapati": [0]*22,
            "Manaksia": [0]*22,
            "Latim": [0]*22,
            "Kamdhenu": [0]*22,
            "Shyam Metallics": [200, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Others": [350, 0, 0, 0, 0, 0, 0, 0, 200, 0, 0, 0, 200, 0, 0, 0, 0, 30, 60, 20, 0, 0],

        }

    elif state_name == "Himachal Pradesh":
        data = {
            "District": [
                'BILASPUR','CHAMBA','HAMIRPUR','KANGRA','KULLU','LAHUL & SPITI','MANDI','UNA','KINNAUR','SHIMLA','SIRMAUR','SOLAN'
            ],
            "Indradhanush": [0, 0, 0, 0, 0, 0, 30, 20, 0, 0, 0, 30],
            "Kamdhenu": [20, 10, 10, 20, 10, 10, 20, 10, 0, 20, 10, 0],
            "Shyam Metallics": [0, 0, 0, 25, 0, 0, 25, 0, 0, 0, 0, 0],
            "AM/NS": [20, 0, 30, 0, 10, 0, 20, 0, 20, 10, 10, 50],
            "Jindal Rangeen": [25, 0, 25, 0, 0, 0, 0, 25, 0, 0, 0, 25],
            "Nepal": [0]*12,
            "Dyna": [0]*12,
            "APL Navrang": [0]*12,
            "Jindal Prajapati": [0]*12,
            "colorshine": [0]*12,
            "Supreme": [0]*12,
            "Rhino": [0]*12,
            "Geo Roofing": [0]*12,
            "Manaksia": [0]*12,
            "Latim": [0]*12,
            "Others": [0]*12
        }
    elif state_name == "Uttarakhand":
        data = {
            "District": [
                'CHAMOLI', 'DEHRADUN', 'HARIDWAR', 'PAURI GARHWAL', 'RUDRA PRAYAG', 
                'TEHRI GARHWAL', 'UTTAR KASHI', 'ALMORA', 'BAGESHWAR', 'CHAMPAWAT', 
                'NAINITAL', 'PITHORAGARH', 'UDHAM SINGH NAGAR'
            ],
            "Indradhanush": [0]*13,
            "AM/NS": [0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100],
            "Shyam Metallics": [0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "APL Navrang": [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Jindal Rangeen": [0, 50, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60],
            "Nepal": [0]*13,
            "Dyna": [0]*13,
            "Jindal Prajapati": [0]*13,
            "colorshine": [0]*13,
            "Supreme": [0]*13,
            "Kamdhenu": [0]*13,
            "Rhino": [0]*13,
            "Geo Roofing": [0]*13,
            "Manaksia": [0, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150],
            "Latim": [0]*13,
            "Others": [0]*13
        }
    
    return pd.DataFrame(data)

@st.cache_data
def get_geojson(state_name):
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/INDIA/INDIA_DISTRICTS.geojson"
    india = gpd.read_file(url)
    state_gdf = india[india['state'].str.upper() == state_name.upper()].copy()
    
    # Unified naming fixes
    state_gdf['district'] = state_gdf['district'].str.upper().replace({
        'CHHATRAPATI SAMBHAJINAGAR': 'AURANGABAD', 
        'DHARASHIV': 'OSMANABAD',
        'DANGS': 'DANG',
        'DAHOD': 'DOHAD',
        'SAS NAGAR (SAHIBZADA AJIT SINGH NAGAR)':'S.A.S NAGAR',
        'BIL>SPUR':'BILASPUR',
        'HAM|RPUR':'HAMIRPUR',
        'K>NGRA':'KANGRA',
        'DEHRAD@N':'DEHRADUN',
        'HARIDW>R':'HARIDWAR',
        'PAURI GARHW>L':'PAURI GARHWAL',
        'RUDRAPRAY>G':'RUDRA PRAYAG',
        'TEHRI GARHW>L':'TEHRI GARHWAL',
        'UTTARK>SHI':'UTTAR KASHI',
        'B>GESHWAR':'BAGESHWAR',
        'CHAMP>WAT':'CHAMPAWAT', 
        'NAINIT>L':'NAINITAL',
        'PITHOR>GARH':'PITHORAGARH'
    })
    state_gdf['district_upper'] = state_gdf['district'].str.upper()
    return state_gdf

# ---------------------------------------------------------
# 2. SELECTION & PROCESSING
# ---------------------------------------------------------
# Sidebar Selections
target_state = st.sidebar.selectbox("Select State", ["Uttarakhand","Himachal Pradesh","Haryana","Uttar Pradesh","Jammu and Kashmir","Punjab","Gujarat", "Maharashtra"])
target_brand = st.sidebar.selectbox("Select Target Brand", ["Indradhanush", "AM/NS", 
                                                            "Nepal", "Kamdhenu", "Jindal Rangeen","Jindal Prajapati","APL Navrang",
                                                            "Colorshine","Supreme","Rhino","Geo Roofing","Manaksia","Latim","Dyna","Shyam Metallics", "Others"])

df = get_state_data(target_state)
state_districts = get_geojson(target_state)

st.title(f" {target_state} District wise Market Mapping")

brand_cols = ["Indradhanush", "AM/NS", "Nepal", "Kamdhenu", "Jindal Rangeen","Jindal Prajapati","APL Navrang","Colorshine","Supreme","Rhino","Geo Roofing","Manaksia","Latim","Dyna","Shyam Metallics", "Others"]
available_cols = [col for col in brand_cols if col in df.columns]
df['Market_Size'] = df[available_cols].sum(axis=1)
share_col_name = f'{target_brand} % share'
df[share_col_name] = np.where(df['Market_Size'] == 0, 0, (df[target_brand] / df['Market_Size']) * 100)
df[share_col_name] = df[share_col_name].round(0).astype(int)

# ---------------------------------------------------------
# 3. CLUSTERING LOGIC (State Sensitive)
# ---------------------------------------------------------
# 1. State-wise Distributor Mapping
state_distributor_configs = {
    "Maharashtra": {
       
    },
    "Gujarat": {
        'AHMEDABAD': 'Distributor A', 
        'SURAT': ['Distributor B', 'Distributor C'],
        'RAJKOT': 'Distributor D'
        # Add your Gujarat distributor list here...
    },
    "Punjab": {
        'AMRITSAR': 'Distributor A'
        # Add your Punjab distributor list here...
    },
    "Jammu and Kashmir": {
        'JAMMU': 'Distributor A'
        # Add your Jammu and Kashmir distributor list here...
    },
    "Uttar Pradesh": {
        'AGRA': 'Distributor A'
        # Add your Jammu and Kashmir distributor list here...
    },
    "Haryana": {
        'FARIDABAD': 'Distributor A'
        # Add your Jammu and Kashmir distributor list here...
    },
    "Himachal Pradesh": {
        'BILASPUR': 'Distributor A'
    },
    "Uttarakhand": {
        'BAGESHWAR': 'Distributor A'
    }  
}

# 2. Get the specific lookup for the selected state
current_distributor_lookup = state_distributor_configs.get(target_state, {})

# 3. Map it to the dataframe
df['Distributors_List'] = df['District'].map(current_distributor_lookup)

# 4. Tooltip Function (remains the same as it uses the mapped column)

def create_tooltip(row):

    tip = f"<b>{row['District']}</b><br>"
    tip += f"Total Market: {row['Market_Size']} MT<br><br>"

    share = int(row[share_col_name]) if pd.notna(row[share_col_name]) else 0

    tip += f"<b>{target_brand}: {row[target_brand]} MT ({share}%)</b><br><br>"

    tip += "<b>Competition:</b><br>"

    for b in brand_cols:

        # Skip missing columns safely
        if b not in row.index:
            continue

        # Skip target brand
        if b != target_brand:

            value = row[b]

            # Handle NaN safely
            if pd.notna(value) and value > 0:

                b_sh = int((value / row['Market_Size']) * 100) if row['Market_Size'] > 0 else 0

                tip += f"{b}: {value} MT ({b_sh}%)<br>"

    tip += "<br><b>Distributors:</b><br>"

    dist_data = row.get('Distributors_List', 'NA')

    if isinstance(dist_data, list):

        for d in dist_data:
            tip += f"{d}<br>"

    elif pd.notna(dist_data) and dist_data != 'NA':

        tip += f"{dist_data}<br>"

    else:

        tip += "NA<br>"

    return tip

df['hover_text'] = df.apply(create_tooltip, axis=1)

# 1. Define the dynamic ranges
state_ranges = {
    "Maharashtra": [
        (50, '0–50 MT', '#dbeafe'),
        (150, '50–150 MT', '#93c5fd'),
        (300, '150–300 MT', '#3b82f6'),
        (float('inf'), '300+ MT', '#1e40af')
    ],
    "Gujarat": [
        (50, '0–50 MT', '#dbeafe'),
        (150, '50–150 MT', '#93c5fd'),
        (300, '150–300 MT', '#3b82f6'),
        (float('inf'), '300+ MT', '#1e40af')
    ],
    "Punjab": [
        (25, '0–25 MT', '#dbeafe'),
        (100, '25–100 MT', '#93c5fd'),
        (200, '100–200 MT', '#3b82f6'),
        (float('inf'), '200+ MT', '#1e40af')
    ],
    "Jammu and Kashmir": [
        (50, '0–50 MT', '#dbeafe'),
        (150, '50–150 MT', '#93c5fd'),
        (300, '150–300 MT', '#3b82f6'),
        (float('inf'), '300+ MT', '#1e40af')
    ],
    "Uttar Pradesh": [
        (50, '0–50 MT', '#dbeafe'),
        (100, '50–100 MT', '#93c5fd'),
        (300, '100–300 MT', '#3b82f6'),
        (float('inf'), '300+ MT', '#1e40af')
    ],
    "Haryana": [
        (50, '0–50 MT', '#dbeafe'),
        (100, '50–100 MT', '#93c5fd'),
        (900, '100–900 MT', '#3b82f6'),
        (float('inf'), '900+ MT', '#1e40af')
    ],
    "Himachal Pradesh": [
        (25, '0–25 MT', '#dbeafe'),
        (100, '25–100 MT', '#93c5fd'),
        (200, '100–200 MT', '#3b82f6'),
        (float('inf'), '200+ MT', '#1e40af')
    ],
    "Uttarakhand": [
        (25, '0–25 MT', '#dbeafe'),
        (50, '25–50 MT', '#93c5fd'),
        (100, '50–100 MT', '#3b82f6'),
        (float('inf'), '100+ MT', '#1e40af')
    ]
}

# 2. Updated color function
def get_m_color(size, state_name):
    ranges = state_ranges.get(state_name, state_ranges["Maharashtra"])
    for threshold, label, color in ranges:
        if size <= threshold:
            return color
    return "#1e40af"

def get_s_color(share):
    if pd.isna(share): return "gray"
    if share < 25: return "#d32f2f"
    elif share < 50: return "#f57c00"
    elif share < 75: return "#8bc34a"
    else: return "#1b5e20"

df['market_color'] = df['Market_Size'].apply(lambda x: get_m_color(x, target_state))
df['share_color'] = df[share_col_name].apply(get_s_color)

merged = state_districts.merge(df, left_on='district_upper', right_on='District', how='left')

# You can define a dictionary for Gujarat Clusters here
cluster_config = {
    "Maharashtra": {
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
    },
    "Gujarat": {
        'AHMADABAD': 'Ahmadabad', 'ANAND': 'Ahmadabad', 'GANDHINAGAR': 'Ahmadabad', 
        'KHEDA': 'Ahmadabad', 'AMRELI': 'Bhavnagar', 'BHAVNAGAR': 'Bhavnagar', 
        'BOTAD': 'Bhavnagar', 'GIR SOMNATH': 'Bhavnagar', 'JUNAGADH': 'Bhavnagar', 
        'PORBANDAR': 'Bhavnagar', 'JAMNAGAR': 'Kachchh', 'KACHCHH': 'Kachchh', 
        'MORBI': 'Kachchh', 'ARVALLI': 'Mahesana', 'BANAS KANTHA': 'Mahesana', 
        'MAHESANA': 'Mahesana', 'PATAN': 'Mahesana', 'SABAR KANTHA': 'Mahesana', 
        'DEVBHUMI DWARKA': 'Rajkot', 'RAJKOT': 'Rajkot', 'SURENDRANAGAR': 'Rajkot', 
        'DANG': 'Surat', 'NAVSARI': 'Surat', 'SURAT': 'Surat', 'TAPI': 'Surat', 
        'VALSAD': 'Surat', 'BHARUCH': 'Vadodara', 'CHHOTAUDEPUR': 'Vadodara', 
        'DOHAD': 'Vadodara', 'MAHISAGAR': 'Vadodara', 'NARMADA': 'Vadodara', 
        'PANCH MAHALS': 'Vadodara', 'VADODARA': 'Vadodara'
    },
    "Punjab": {
        'AMRITSAR':'Amritsar', 'GURDASPUR':'Amritsar', 'HOSHIARPUR':'Amritsar', 
        'JALANDHAR':'Amritsar', 'KAPURTHALA':'Amritsar', 
        'PATHANKOT':'Amritsar', 'SHAHID BHAGAT SINGH NAGAR':'Amritsar', 'TARN TARAN':'Amritsar',
        'BARNALA':'Chandigarh', 'FATEHGARH SAHIB':'Chandigarh', 'LUDHIANA':'Chandigarh',
        'MALER KOTLA':'Chandigarh', 'MANSA':'Chandigarh', 'PATIALA':'Chandigarh', 
        'RUPNAGAR':'Chandigarh', 'S.A.S NAGAR':'Chandigarh', 'SANGRUR':'Chandigarh',
        'BATHINDA':'Faridkot', 'FARIDKOT':'Faridkot', 
        'FAZILKA':'Faridkot', 'FIROZPUR':'Faridkot', 'MOGA':'Faridkot', 'SRI MUKTSAR SAHIB':'Faridkot'
    },
    "Jammu and Kashmir": {
        'DODA': 'Jammu', 'JAMMU': 'Jammu', 'KATHUA': 'Jammu', 'KISHTWAR': 'Jammu', 'PUNCH': 'Jammu',
        'RAJAURI': 'Jammu', 'RAMBAN': 'Jammu', 'RIASI': 'Jammu', 'SAMBA': 'Jammu', 'UDHAMPUR': 'Jammu',
        'SHUPIYAN': 'Srinagar', 'ANANTNAG': 'Srinagar', 'BANDIPURA': 'Srinagar', 'BARAMULA': 'Srinagar', 'BADGAM': 'Srinagar',
        'GANDERBAL': 'Srinagar', 'KUPWARA': 'Srinagar', 'KULGAM': 'Srinagar', 'PULWAMA': 'Srinagar', 'SRINAGAR': 'Srinagar'
    },
    "Uttar Pradesh": {
        'AGRA': 'Agra', 'ALIGARH': 'Agra', 'ETAH': 'Agra', 'FIROZABAD': 'Agra', 'HATHRAS': 'Agra', 'KASGANJ': 'Agra', 'MAINPURI': 'Agra', 'MATHURA': 'Agra',
        'AMROHA': 'Bareilly', 'BAREILLY': 'Bareilly', 'BIJNOR': 'Bareilly', 'BUDAUN': 'Bareilly', 'PILIBHIT': 'Bareilly', 'RAMPUR': 'Bareilly', 'SAMBHAL': 'Bareilly', 'SHAHJAHANPUR': 'Bareilly',
        'BAGHPAT': 'Ghaziabad', 'BULANDSHAHR': 'Ghaziabad', 'GAUTAM BUDDHA NAGAR': 'Ghaziabad', 'GHAZIABAD': 'Ghaziabad', 'HAPUR': 'Ghaziabad', 'MEERUT': 'Ghaziabad', 'MUZAFFARNAGAR': 'Ghaziabad', 'SAHARANPUR': 'Ghaziabad', 'SHAMLI': 'Ghaziabad', 'MORADABAD': 'Ghaziabad',
        'AYODHYA': 'Gorakhpur', 'AZAMGARH': 'Gorakhpur', 'BAHRAICH': 'Gorakhpur', 'BALLIA': 'Gorakhpur', 'BASTI': 'Gorakhpur', 'DEORIA': 'Gorakhpur', 'GONDA': 'Gorakhpur', 'GORAKHPUR': 'Gorakhpur', 'KUSHINAGAR': 'Gorakhpur', 'MAHRAJGANJ': 'Gorakhpur', 'MAU': 'Gorakhpur', 'SHRAWASTI': 'Gorakhpur', 'SIDDHARTHNAGAR': 'Gorakhpur', 'SULTANPUR': 'Gorakhpur',
        'AURAIYA': 'Kanpur', 'BANDA': 'Kanpur', 'CHITRAKOOT': 'Kanpur', 'ETAWAH': 'Kanpur', 'FARRUKHABAD': 'Kanpur', 'JALAUN': 'Kanpur', 'JHANSI': 'Kanpur', 'KANNAUJ': 'Kanpur', 'KANPUR DEHAT': 'Kanpur', 'KANPUR NAGAR': 'Kanpur', 'LALITPUR': 'Kanpur', 'MAHOBA': 'Kanpur',
        'BARA BANKI': 'Lucknow', 'HARDOI': 'Lucknow', 'KHERI': 'Lucknow', 'LUCKNOW': 'Lucknow', 'RAE BARELI': 'Lucknow', 'SITAPUR': 'Lucknow', 'UNNAO': 'Lucknow',
        'BHADOHI': 'Varanasi', 'CHANDAULI': 'Varanasi', 'FATEHPUR': 'Varanasi', 'GHAZIPUR': 'Varanasi', 'JAUNPUR': 'Varanasi', 'KAUSHAMBI': 'Varanasi', 'MIRZAPUR': 'Varanasi', 'PRAYAGRAJ': 'Varanasi', 'SONBHADRA': 'Varanasi', 'VARANASI': 'Varanasi'
    },
    "Haryana": {
        'FARIDABAD': 'Faridabad', 'GURUGRAM': 'Faridabad', 'MAHENDRAGARH': 'Faridabad', 'NUH': 'Faridabad', 'PALWAL': 'Faridabad', 'REWARI': 'Faridabad',
        'BHIWANI': 'Hisar', 'FATEHABAD': 'Hisar', 'HISAR': 'Hisar', 'JIND': 'Hisar', 'SIRSA': 'Hisar',
        'AMBALA': 'Kurukshetra', 'KAITHAL': 'Kurukshetra', 'KURUKSHETRA': 'Kurukshetra', 'PANCHKULA': 'Kurukshetra', 'YAMUNANAGAR': 'Kurukshetra',
        'CHARKI DADRI': 'Rohtak', 'JHAJJAR': 'Rohtak', 'KARNAL': 'Rohtak', 'PANIPAT': 'Rohtak', 'ROHTAK': 'Rohtak', 'SONIPAT': 'Rohtak'
    },
    "Himachal Pradesh": {
        'BILASPUR':'Mandi','CHAMBA':'Mandi','HAMIRPUR':'Mandi','KANGRA':'Mandi','KULLU':'Mandi',
        'LAHUL & SPITI':'Mandi','MANDI':'Mandi','UNA':'Mandi',
        'KINNAUR':'Solan','SHIMLA':'Solan','SIRMAUR':'Solan','SOLAN':'Solan'
    },
    "Uttarakhand": {
        'CHAMOLI':'Garhwal', 'DEHRADUN':'Garhwal', 'HARIDWAR':'Garhwal', 'PAURI GARHWAL':'Garhwal',
        'RUDRA PRAYAG':'Garhwal', 'TEHRI GARHWAL':'Garhwal', 'UTTAR KASHI':'Garhwal',
        'ALMORA':'Kumaon', 'BAGESHWAR':'Kumaon', 'CHAMPAWAT':'Kumaon', 
        'NAINITAL':'Kumaon', 'PITHORAGARH':'Kumaon', 'UDHAM SINGH NAGAR':'Kumaon'
    }
}

# current_cluster_map = cluster_config.get(target_state, {})
# merged['cluster'] = merged['district_upper'].map(current_cluster_map)
# clusters = merged.dissolve(by='cluster')
current_cluster_map = cluster_config.get(target_state, {})

# Now apply the map
merged['cluster'] = merged['district_upper'].map(current_cluster_map)
merged = merged[merged.geometry.notnull()]

# 2. Fix invalid geometries (self-intersections)
merged['geometry'] = merged.geometry.buffer(0)

# 3. Ensure everything is a GeoDataFrame again
merged = gpd.GeoDataFrame(merged, geometry='geometry')

clusters = merged.dissolve(by='cluster')


# ---------------------------------------------------------

# (The rest of your script follows here, using 'state_districts' instead of 'maharashtra_districts' 
# and 'current_cluster_map' instead of the hardcoded 'cluster_map')
# ---------------------------------------------------------
# 4. INTERACTIVE VISUALIZATION
# ---------------------------------------------------------
st.subheader(f"{target_brand} Market Distribution")

fig = go.Figure()

# A. DISTRICT POLYGONS
for _, row in merged.iterrows():
    if row.geometry:
        geom = row.geometry
        polys = [geom] if geom.geom_type == 'Polygon' else geom.geoms
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
    geom = row.geometry
    polys = [geom] if geom.geom_type == 'Polygon' else geom.geoms
    for poly in polys:
        x, y = poly.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y),
            line=dict(color="#1e293b", width=2.5),
            hoverinfo='skip',
            showlegend=False,
            mode='lines'
        ))

# C. LABELS AND BOXES
annotations = []
for _, row in merged.iterrows():
    if row.geometry:
        centroid = row.geometry.centroid
        # Robust hub check
        is_hub = str(row['district_upper']).upper() == str(row['cluster']).upper()
        share_val = f"{int(row[share_col_name])}%" if pd.notna(row[share_col_name]) else "0%"
        
        # 1. District Name
        annotations.append(dict(
            x=centroid.x, y=centroid.y + (0.15 if is_hub else 0.1),
            text=row['district'].upper() if is_hub else row['district'].title(),
            showarrow=False,
            font=dict(size=13 if is_hub else 10, color="black", family="Arial Black" if is_hub else "Arial"),
            xref="x", yref="y"
        ))
        
        state_y_offsets = {
            "Maharashtra": -0.1,
            "Gujarat": -0.05,
            "Punjab": 0,
            "Jammu and Kashmir": 0,
            "Uttar Pradesh": -0.05,
            "Haryana":0,
            "Himachal Pradesh":0,
            "Uttarakhand":0   
        }
        # Get the offset for the current state, default to -0.1 if not found
        current_offset = state_y_offsets.get(target_state, -0.1)
        
        # 2. Share % Box
        annotations.append(dict(
            x=centroid.x, 
            y=centroid.y + current_offset, # Using the state-specific offset
            text=f"<b>{share_val}</b>",
            showarrow=False,
            font=dict(size=13, color="white"),
            bgcolor=row['share_color'] if pd.notna(row['share_color']) else 'gray',
            bordercolor="black", borderwidth=1, borderpad=3,
            xref="x", yref="y"
        ))

# Manual Fix for Maharashtra only
if target_state == "Punjab":
    annotations.append(dict(
        x=76.77, y=30.57, text="<b>CHANDIGARH</b>",
        showarrow=False, font=dict(size=13, color="black", family="Arial Black"),
        xref="x", yref="y"
    ))

if target_state == "Uttar Pradesh":
    annotations.append(dict(
        x=78.7, y=26.4, text="<b>KANPUR</b>",
        showarrow=False, font=dict(size=13, color="black", family="Arial Black"),
        xref="x", yref="y"
    ))

if target_state == "Uttarakhand":
    annotations.append(dict(
        x=78.78, y=30.15, text="<b>GARHWAL</b>",
        showarrow=False, font=dict(size=13, color="black", family="Arial Black"),
        xref="x", yref="y"
    ))
if target_state == "Uttarakhand":
    annotations.append(dict(
        x=79.75, y=29.55, text="<b>KUMAON</b>",
        showarrow=False, font=dict(size=13, color="black", family="Arial Black"),
        xref="x", yref="y"
    ))

# --- TOTAL MARKET BOX (Merged into annotations to prevent error) ---
total_mkt_size = df['Market_Size'].sum()
total_brand_vol = df[target_brand].sum()
total_brand_pct = (total_brand_vol / total_mkt_size * 100) if total_mkt_size > 0 else 0

annotations.append(dict(
    x=0.99, y=0.01, xref="paper", yref="paper",
    text=(
        f"<b>Total Mass Market</b><br>"
        f"<b><span style='font-size:20px;color:#1e40af;'>{total_mkt_size} MT</span></b><br><br>"
        f"<b>JSW {target_brand} Share</b><br>"
        f"<b><span style='font-size:18px;color:#1b5e20;'>{total_brand_vol} MT ({total_brand_pct:.0f}%)</span></b>"
    ),
    showarrow=False, align="right",
    font=dict(size=14, color="Black", family="Arial Black"),
    bgcolor="rgba(255,255,255,0.9)", bordercolor="black", borderwidth=1, borderpad=10
))

# 1. Legends
current_ranges = state_ranges.get(target_state, state_ranges["Maharashtra"])
for _, label, color in current_ranges:
    fig.add_trace(go.Scatter(
        x=[None], y=[None], 
        mode='markers', 
        marker=dict(size=10, color=color, symbol='square'),
        legendgroup="Market", 
        legendgrouptitle_text="Market Size (MT)", 
        name=label
    ))

for label, color in [('> 75%', '#1b5e20'), ('50–75%', '#8bc34a'), ('25–50%', '#f57c00'), ('< 25%', '#d32f2f')]:
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=color, symbol='square'),
                             legendgroup="Share", legendgrouptitle_text=f"{target_brand} %", name=label))

fig.update_layout(
    annotations=annotations,
    dragmode=False, # Disables panning/dragging
    xaxis=dict(fixedrange=True, visible=False), # Disables zooming on X
    yaxis=dict(fixedrange=True, visible=False, scaleanchor="x", scaleratio=1), # Disables zooming on Y
    plot_bgcolor='white',
    margin=dict(l=0, r=0, t=0, b=0),
    height=800 if target_state=="Uttar Pradesh" else 600,
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
        itemsizing='constant')
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
# st.divider()
# st.subheader(f"📍 Key Focus Areas: {target_brand} Share < 50%")

# # 1. Filter and Sort
# focus_df = merged[merged[share_col_name] < 50].copy()
# focus_df = focus_df.sort_values(by=['cluster', share_col_name], ascending=[True, True])

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
                ('padding', '2px 5px'), 
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

# if not focus_df.empty:
#     # 2. Format columns
#     focus_df['Share_Display'] = focus_df.apply(lambda x: f"{int(x[target_brand])} MT ({int(x[share_col_name])}%)", axis=1)
#     focus_df['Market_Size_Display'] = focus_df['Market_Size'].apply(lambda x: f"{int(x)} MT")
    
#     # 3. Prepare display dataframe
#     display_df = focus_df[['cluster', 'district', 'Share_Display', 'Market_Size_Display']].copy()
#     display_df.columns = ['Cluster', 'Districts', f'{target_brand} Share', 'Total Market']
#     display_df['Districts'] = display_df['Districts'].str.title()
    
#     # 4. Track cluster changes
#     is_new_cluster = ~display_df['Cluster'].duplicated()
#     display_df['Cluster'] = np.where(display_df['Cluster'].duplicated(), "", display_df['Cluster'])
    
    
        
#     # st.table(style_final_table(display_df))
#     st.markdown(style_final_table(display_df).to_html(), unsafe_allow_html=True)

# else:
#     # Show empty table with headers only
#     st.info(f"✨ All districts have more than 50%+ share in {target_brand}.")
# ---------------------------------------------------------
# 6. DYNAMIC KEY FOCUS AREAS (FINAL FORMATTING)
# ---------------------------------------------------------
st.divider()
st.subheader(f"📍 Key Focus Areas: {target_brand} Share < 50%")

focus_df = merged[merged[share_col_name] < 50].copy()

if not focus_df.empty:
    # 1. Calculate Aggregates
    cluster_stats = focus_df.groupby('cluster').agg({
        target_brand: 'sum',
        'Market_Size': 'sum'
    }).reset_index()

    cluster_stats['Cluster_Share'] = np.where(
        cluster_stats['Market_Size'] == 0, 0, 
        (cluster_stats[target_brand] / cluster_stats['Market_Size']) * 100
    ).round(0).astype(int)

    # 2. Sort the main dataframe
    focus_df = focus_df.sort_values(by=['cluster', share_col_name], ascending=[True, True])
    
    # 3. Format district columns
    focus_df['Share_Display'] = focus_df.apply(lambda x: f"{int(x[target_brand])} MT ({int(x[share_col_name])}%)", axis=1)
    focus_df['Market_Size_Display'] = focus_df['Market_Size'].apply(lambda x: f"{int(x)} MT")

    # 4. Prepare Display Dataframe
    display_df = focus_df[['cluster', 'district', 'Share_Display', 'Market_Size_Display']].copy()
    display_df.columns = ['Cluster', 'Districts', f'{target_brand} Share', 'Total Market']
    display_df['Districts'] = display_df['Districts'].str.title()

   # --- UPDATED POSITIONING LOGIC ---
    new_labels = []
    cluster_group_counts = display_df['Cluster'].value_counts()
    current_counts = {} 

    for idx, row in display_df.iterrows():
        c_name = row['Cluster']
        current_counts[c_name] = current_counts.get(c_name, 0) + 1
        
        # Get stats for this cluster (calculated from focus_df only)
        stats = cluster_stats[cluster_stats['cluster'] == c_name].iloc[0]
        
        # Line 1: Cluster Name (Total Market Size)
        line1 = (
            f"<b>{c_name} "
            f"<span style='color:#1e40af;'>({int(stats['Market_Size'])} MT)</span></b>"
        )
        
        # Line 2: JSW - Brand Volume (Share %)
        line2 = (
            f"<span style='font-size:14px; color:#1e40af;'>"
            f"<b>JSW - {int(stats[target_brand])} MT ({stats['Cluster_Share']}%)</b>"
            f"</span>"
        )
        
        total_in_cluster = cluster_group_counts[c_name]

        if total_in_cluster == 1:
            # Single district: Combine both lines in one cell
            new_labels.append(f"{line1}<br>{line2}")
        else:
            # Multiple districts: Split across first and second row
            if current_counts[c_name] == 1:
                new_labels.append(line1)
            elif current_counts[c_name] == 2:
                new_labels.append(line2)
            else:
                new_labels.append("")

    display_df['Cluster'] = new_labels
    # ---------------------------------------------------------
    # Create the horizontal border tracker
    # We need a fresh copy of the original cluster column to detect changes for borders
    is_new_cluster = ~focus_df['cluster'].duplicated()

    # Display
    st.markdown(style_final_table(display_df).to_html(), unsafe_allow_html=True)

else:
    st.info(f"✨ All districts have more than 50%+ share in {target_brand}.")
