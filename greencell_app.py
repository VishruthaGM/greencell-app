import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="GreenCell Analyzer", layout="wide")

# ===== Custom Theme =====
st.markdown("""
<style>
.main {background-color: #ecfdf5;}
.stButton>button {background-color: #15803d; color: white; font-size: 16px; font-weight: bold;}
.big-font {font-size:22px !important; font-weight:bold;}
.battery-bar {height:25px; border-radius:5px; background-color:#d1fae5;}
</style>
""", unsafe_allow_html=True)

st.title("🌿 GreenCell")
st.subheader("AI-Powered Battery Health & Reusability System")

# ===== Database Simulation =====
if "database" not in st.session_state:
    st.session_state.database = pd.DataFrame(columns=[
        "Battery ID","OCV","Load Voltage","Current",
        "Internal Resistance","Temperature",
        "Health Score","Classification","Timestamp"
    ])

# ===== LAYER 1: Smart Battery Testing Terminal =====
st.header("🔋 Battery Testing Terminal (Simulated Device)")

if st.button("Insert & Scan Battery"):
    st.info("Battery inserted... scanning in progress ⚡")
    
    progress_bar = st.progress(0)
    battery_bar = st.empty()  # For battery animation
    
    # Sensor values placeholders
    ocv, load_v, current, resistance, temp = 0,0,0,0,0
    
    for i in range(101):
        time.sleep(0.02)
        progress_bar.progress(i)
        
        # Simulate sensor readings
        ocv = round(random.uniform(0.8, 1.6), 2)
        load_v = round(random.uniform(0.7, 1.5), 2)
        current = round(random.uniform(0.1, 2.0), 2)
        resistance = round(random.uniform(0.05, 0.5), 2)
        temp = round(random.uniform(25, 55), 2)
        
        # Live metrics display
        col1, col2, col3 = st.columns(3)
        col1.metric("OCV (V)", ocv)
        col2.metric("Load Voltage (V)", load_v)
        col3.metric("Temperature (°C)", temp)
        col4, col5 = st.columns(2)
        col4.metric("Current (A)", current)
        col5.metric("Internal Resistance (Ω)", resistance)
        
        # Battery fill animation
        fill_width = i  # percentage
        battery_bar.markdown(f"""
        <div class="battery-bar">
            <div style="width:{fill_width}%; height:100%; background-color:#16a34a; border-radius:5px;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Health Score & Classification
    health_score = int((ocv * 40) + ((1/resistance) * 10) - (temp * 0.5))
    if health_score > 70:
        classification = "Reusable 🟢"
        class_color = "#16a34a"
    elif health_score > 40:
        classification = "Recyclable 🟡"
        class_color = "#facc15"
    else:
        classification = "Hazardous 🔴"
        class_color = "#dc2626"
    
    st.markdown("### 🔵 Battery Health Score")
    st.progress(min(max(health_score,0),100))
    st.markdown(f"<div class='big-font' style='color:{class_color}'>Score: {health_score}/100</div>", unsafe_allow_html=True)
    
    if classification.startswith("Hazardous"):
        st.error("⚠️ Hazardous Battery Detected!")
    else:
        st.success(f"Final Classification: {classification}")
    
    # ===== LAYER 2: Simulated Cloud Upload =====
    st.info("Uploading data to cloud ☁️")
    upload_progress = st.progress(0)
    for j in range(101):
        time.sleep(0.01)
        upload_progress.progress(j)
    
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
    st.success("Data uploaded successfully! ✅")

# ===== LAYER 3: Cloud Dashboard =====
st.header("☁️ Cloud Analytics Dashboard")

df = st.session_state.database

if not df.empty:
    colA, colB = st.columns([2,1])
    
    with colA:
        st.dataframe(df, use_container_width=True)
    
    with colB:
        st.markdown("### ♻ Classification Breakdown")
        fig, ax = plt.subplots(figsize=(4,4))
        colors = ["#16a34a", "#facc15", "#dc2626"]
        df["Classification"].value_counts().plot.pie(
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
            ax=ax
        )
        ax.set_ylabel("")
        ax.legend(df["Classification"].value_counts().index, loc="best")
        st.pyplot(fig)
    
    total = len(df)
    reusable = len(df[df["Classification"].str.contains("Reusable")])
    recyclable = len(df[df["Classification"].str.contains("Recyclable")])
    hazardous = len(df[df["Classification"].str.contains("Hazardous")])
    co2_saved = reusable * 0.5
    
    # Metrics with colors
    def metric_color(value, max_val):
        if value/ max_val > 0.7: return "#16a34a"
        elif value/ max_val > 0.4: return "#facc15"
        else: return "#dc2626"
    
    st.markdown("### 🌍 Sustainability Impact")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Batteries", total)
    col2.metric("Reusable", reusable)
    col3.metric("Recyclable", recyclable)
    col4.metric("Hazardous", hazardous)
    st.write(f"Estimated CO₂ Saved: {co2_saved} kg")
    
    # Trend graph with color-coded line
    st.markdown("### 📈 Battery Health Trend")
    fig2, ax2 = plt.subplots(figsize=(6,3))
    scores = df["Health Score"].tolist()
    times = df["Timestamp"].tolist()
    colors = ["#16a34a" if s>70 else "#facc15" if s>40 else "#dc2626" for s in scores]
    for i in range(len(scores)-1):
        ax2.plot(times[i:i+2], scores[i:i+2], color=colors[i], marker='o')
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("Health Score")
    ax2.set_title("Battery Health Score Over Time")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)
    
else:
    st.info("No batteries tested yet.")
