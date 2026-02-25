import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GreenCell Analyzer", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f0fdf4;}
    .stButton>button {
        background-color: #16a34a;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 GreenCell")
st.subheader("Smart Battery Health & Reusability Analyzer")

if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "Battery ID","OCV","Load Voltage","Current",
        "Internal Resistance","Temperature","Classification","Timestamp"
    ])

st.header("🔍 Battery Testing Terminal")

if st.button("Insert & Scan Battery"):
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress.progress(i+1)

    ocv = round(random.uniform(0.8, 1.6), 2)
    load_v = round(random.uniform(0.7, 1.5), 2)
    current = round(random.uniform(0.1, 2.0), 2)
    resistance = round(random.uniform(0.05, 0.5), 2)
    temp = round(random.uniform(25, 55), 2)

    if temp > 45 or ocv < 1.0:
        classification = "Hazardous 🔴"
    elif ocv > 1.3 and resistance < 0.2:
        classification = "Reusable 🟢"
    else:
        classification = "Recyclable 🟡"

    st.subheader("📊 Test Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Open Circuit Voltage (V)", ocv)
    col2.metric("Load Voltage (V)", load_v)
    col3.metric("Temperature (°C)", temp)

    col4, col5 = st.columns(2)
    col4.metric("Current (A)", current)
    col5.metric("Internal Resistance (Ω)", resistance)

    st.success(f"Final Classification: {classification}")

    new_entry = {
        "Battery ID": f"BAT-{random.randint(1000,9999)}",
        "OCV": ocv,
        "Load Voltage": load_v,
        "Current": current,
        "Internal Resistance": resistance,
        "Temperature": temp,
        "Classification": classification,
        "Timestamp": datetime.now()
    }

    st.session_state.database = pd.concat(
        [st.session_state.database, pd.DataFrame([new_entry])],
        ignore_index=True
    )

st.header("☁️ Cloud Analytics Dashboard")

df = st.session_state.database

if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df["Classification"].value_counts())

    total = len(df)
    reusable = len(df[df["Classification"].str.contains("Reusable")])
    co2_saved = reusable * 0.5

    st.markdown("### 🌍 Sustainability Impact")
    st.write(f"Total Batteries Tested: {total}")
    st.write(f"Estimated CO₂ Saved by Reuse: {co2_saved} kg")
else:
    st.info("No batteries tested yet.")
