import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GreenCell Analyzer", layout="wide")

# ===== Custom Theme ====
st.markdown("""
<style>
.main {
    background-color: #ecfdf5;
}
.stButton>button {
    background-color: #15803d;
    color: white;
    font-size: 16px;
    font-weight: bold;
}
.big-font {
    font-size:22px !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 GreenCell")
st.subheader("AI-Powered Battery Health & Reusability System")

# ===== Database =====
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "Battery ID","OCV","Load Voltage","Current",
        "Internal Resistance","Temperature",
        "Health Score","Classification","Timestamp"
    ])

st.header("🔋 Battery Testing Terminal")

if st.button("Insert & Scan Battery"):
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.015)
        progress.progress(i+1)

    ocv = round(random.uniform(0.8, 1.6), 2)
    load_v = round(random.uniform(0.7, 1.5), 2)
    current = round(random.uniform(0.1, 2.0), 2)
    resistance = round(random.uniform(0.05, 0.5), 2)
    temp = round(random.uniform(25, 55), 2)

    # Health Score Formula
    health_score = int((ocv * 40) + ((1/resistance) * 10) - (temp * 0.5))

    if health_score > 70:
        classification = "Reusable 🟢"
    elif health_score > 40:
        classification = "Recyclable 🟡"
    else:
        classification = "Hazardous 🔴"

    st.subheader("📊 Live Test Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("OCV (V)", ocv)
    col2.metric("Load Voltage (V)", load_v)
    col3.metric("Temperature (°C)", temp)

    col4, col5 = st.columns(2)
    col4.metric("Current (A)", current)
    col5.metric("Internal Resistance (Ω)", resistance)

    st.markdown("### 🔵 Battery Health Score")
    st.progress(min(max(health_score,0),100))
    st.markdown(f"<div class='big-font'>Score: {health_score}/100</div>", unsafe_allow_html=True)

    st.success(f"Final Classification: {classification}")

    new_entry = {
        "Battery ID": f"BAT-{random.randint(1000,9999)}",
        "OCV": ocv,
        "Load Voltage": load_v,
        "Current": current,
        "Internal Resistance": resistance,
        "Temperature": temp,
        "Health Score": health_score,
        "Classification": classification,
        "Timestamp": datetime.now()
    }

    st.session_state.database = pd.concat(
        [st.session_state.database, pd.DataFrame([new_entry])],
        ignore_index=True
    )

# ===== Dashboard =====
st.header("☁️ Cloud Analytics Dashboard")

df = st.session_state.database

if not df.empty:

    colA, colB = st.columns([2,1])

    with colA:
        st.dataframe(df, use_container_width=True)

    with colB:
        st.markdown("### ♻ Classification Breakdown")
        st.pyplot(df["Classification"].value_counts().plot.pie(
            autopct="%1.1f%%",
            figsize=(4,4)
        ).figure)

    total = len(df)
    reusable = len(df[df["Classification"].str.contains("Reusable")])
    co2_saved = reusable * 0.5

    st.markdown("### 🌍 Sustainability Impact")
    st.write(f"Total Batteries Tested: {total}")
    st.write(f"Reusable Batteries: {reusable}")
    st.write(f"Estimated CO₂ Saved: {co2_saved} kg")

else:
    st.info("No batteries tested yet.")
