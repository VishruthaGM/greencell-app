import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from streamlit_lottie import st_lottie
import requests

# =========================
# Helper: load Lottie animation
# =========================
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# =========================
# Page Configuration
# =========================
st.set_page_config(page_title="💚 GreenCell Dashboard", layout="wide", page_icon="💚")
st.markdown("""
<style>
/* Card styling */
.card {
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px #ddd;
    margin-bottom: 15px;
    background-color: #fff;
}
h1 {
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Intro Page (like Netflix landing)
# =========================
intro_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_touohxv0.json") # battery animation
st_lottie(intro_animation, height=300, key="intro")

st.markdown("<h1>💚 GreenCell: Smart Battery Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### Sustainable e-waste & smart city monitoring")

st.button("Enter Dashboard")  # Wait for user click

# =========================
# Simulate Battery Data
# =========================
num_batteries = 50
data = {
    'Battery_ID': [f'BAT{i+1}' for i in range(num_batteries)],
    'Open_Circuit_Voltage': np.round(np.random.uniform(1.2, 1.6, num_batteries), 2),
    'Load_Voltage': np.round(np.random.uniform(1.1, 1.55, num_batteries), 2),
    'Current': np.round(np.random.uniform(0.05, 0.5, num_batteries), 2),
    'Temperature': np.round(np.random.uniform(20, 40, num_batteries), 1)
}
df = pd.DataFrame(data)
df['Internal_Resistance'] = np.round((df['Open_Circuit_Voltage'] - df['Load_Voltage']) / df['Current'], 2)

# =========================
# Classification
# =========================
def classify_aa(row):
    if row['Temperature'] > 40 or row['Internal_Resistance'] > 1.0 or row['Open_Circuit_Voltage'] < 1.3:
        return 'Hazardous'
    elif row['Internal_Resistance'] <= 0.5 and row['Open_Circuit_Voltage'] >= 1.5:
        return 'Reusable'
    else:
        return 'Recyclable'

df['Status'] = df.apply(classify_aa, axis=1)

# =========================
# Layout: Summary Cards in Grid
# =========================
total = len(df)
reusable = len(df[df['Status']=='Reusable'])
recyclable = len(df[df['Status']=='Recyclable'])
hazardous = len(df[df['Status']=='Hazardous'])

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    for col, title, value, color in zip(
        [col1, col2, col3, col4],
        ["Total Batteries", "Reusable", "Recyclable", "Hazardous"],
        [total, reusable, recyclable, hazardous],
        ["#000", "green", "orange", "red"]
    ):
        col.markdown(f"""
        <div class="card" style="text-align:center">
            <h3 style="color:{color}">{title}</h3>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# Grid Layout for Charts & Table
# =========================
with st.container():
    chart_col1, chart_col2 = st.columns([2,1])
    
    # Pie Chart
    fig = px.pie(df, names='Status',
                 color='Status', color_discrete_map={'Reusable':'green','Recyclable':'orange','Hazardous':'red'},
                 title="Battery Status Distribution")
    chart_col1.plotly_chart(fig, use_container_width=True)
    
    # Battery Table with icons
    status_colors = {'Reusable':'💚', 'Recyclable':'🟡', 'Hazardous':'🔴'}
    display_df = df.copy()
    display_df['Status'] = display_df['Status'].map(lambda x: f"{status_colors[x]} {x}")
    chart_col2.dataframe(display_df, height=500)

# =========================
# Analytics Cards (Voltage / Resistance / Temp)
# =========================
with st.container():
    col_v, col_r, col_t = st.columns(3)
    col_v.bar_chart(df['Open_Circuit_Voltage'])
    col_r.bar_chart(df['Internal_Resistance'])
    col_t.bar_chart(df['Temperature'])

# =========================
# Hazardous Alert
# =========================
if hazardous > 0:
    st.warning(f"⚠️ {hazardous} hazardous batteries detected! Handle with care!")
