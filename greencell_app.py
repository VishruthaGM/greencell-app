import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="💚 GreenCell Battery Dashboard", layout="wide", page_icon="💚")
st.title("💚 GreenCell: Interactive Battery Health Analyzer")

# =========================
# Session state initialization
# =========================
if "tested_batteries" not in st.session_state:
    st.session_state.tested_batteries = pd.DataFrame(columns=[
        "Battery_ID", "Open_Circuit_Voltage", "Load_Voltage",
        "Current", "Temperature", "Internal_Resistance", "Status"
    ])
if "battery_count" not in st.session_state:
    st.session_state.battery_count = 0

# =========================
# Simulate a battery measurement
# =========================
def simulate_battery():
    st.session_state.battery_count += 1
    battery_id = f"BAT{st.session_state.battery_count}"
    ocv = np.round(np.random.uniform(1.2, 1.6), 2)
    lv = np.round(np.random.uniform(1.1, ocv), 2)
    current = np.round(np.random.uniform(0.05, 0.5), 2)
    temp = np.round(np.random.uniform(20, 40), 1)
    resistance = np.round((ocv - lv)/current, 2)
    
    # Classification
    if temp > 40 or resistance > 1.0 or ocv < 1.3:
        status = "Hazardous"
    elif resistance <= 0.5 and ocv >= 1.5:
        status = "Reusable"
    else:
        status = "Recyclable"
    
    return {
        "Battery_ID": battery_id,
        "Open_Circuit_Voltage": ocv,
        "Load_Voltage": lv,
        "Current": current,
        "Temperature": temp,
        "Internal_Resistance": resistance,
        "Status": status
    }

# =========================
# Add Battery Button + Progress
# =========================
st.subheader("Process a New Battery")
if st.button("Add Battery"):
    progress = st.progress(0)
    for i in range(0, 101, 25):
        time.sleep(0.2)
        progress.progress(i)
    
    new_battery = simulate_battery()
    st.session_state.tested_batteries = pd.concat([
        st.session_state.tested_batteries,
        pd.DataFrame([new_battery])
    ])
    st.success(f"✅ {new_battery['Battery_ID']} processed and added!")

# =========================
# Prepare Data
# =========================
df = st.session_state.tested_batteries
total = len(df)
if total > 0:
    reusable = len(df[df['Status']=="Reusable"])
    recyclable = len(df[df['Status']=="Recyclable"])
    hazardous = len(df[df['Status']=="Hazardous"])
else:
    reusable = recyclable = hazardous = 0

# =========================
# Summary Cards
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Batteries", total)
col2.metric("Reusable 💚", reusable, f"{reusable/total*100:.1f}%" if total>0 else "0%")
col3.metric("Recyclable 🟡", recyclable, f"{recyclable/total*100:.1f}%" if total>0 else "0%")
col4.metric("Hazardous 🔴", hazardous, f"{hazardous/total*100:.1f}%" if total>0 else "0%")

st.markdown("---")

# =========================
# Battery Status Pie Chart
# =========================
if total > 0:
    fig_pie = go.Figure(go.Pie(
        labels=df["Status"],
        values=[reusable, recyclable, hazardous],
        marker=dict(colors=["green","orange","red"]),
        hole=0.4
    ))
    fig_pie.update_layout(title_text="Battery Status Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# Battery Meter-Style Charts
# =========================
if total > 0:
    st.subheader("Battery Meters")
    # Voltage meter
    fig_voltage = go.Figure()
    for idx, row in df.iterrows():
        color = {"Reusable":"green","Recyclable":"orange","Hazardous":"red"}[row["Status"]]
        fig_voltage.add_trace(go.Bar(
            x=[row["Battery_ID"]],
            y=[row["Open_Circuit_Voltage"]],
            marker_color=color,
            text=[f"OCV: {row['Open_Circuit_Voltage']}V"],
            textposition='outside',
            name=row["Battery_ID"]
        ))
    fig_voltage.update_layout(
        title="Open Circuit Voltage (V)",
        yaxis=dict(range=[0,2]),
        showlegend=False
    )
    
    # Internal Resistance meter
    fig_resistance = go.Figure()
    for idx, row in df.iterrows():
        color = {"Reusable":"green","Recyclable":"orange","Hazardous":"red"}[row["Status"]]
        fig_resistance.add_trace(go.Bar(
            x=[row["Battery_ID"]],
            y=[row["Internal_Resistance"]],
            marker_color=color,
            text=[f"R: {row['Internal_Resistance']}Ω"],
            textposition='outside',
            name=row["Battery_ID"]
        ))
    fig_resistance.update_layout(
        title="Internal Resistance (Ω)",
        yaxis=dict(range=[0,2]),
        showlegend=False
    )
    
    # Temperature meter
    fig_temp = go.Figure()
    for idx, row in df.iterrows():
        color = {"Reusable":"green","Recyclable":"orange","Hazardous":"red"}[row["Status"]]
        fig_temp.add_trace(go.Bar(
            x=[row["Battery_ID"]],
            y=[row["Temperature"]],
            marker_color=color,
            text=[f"T: {row['Temperature']}°C"],
            textposition='outside',
            name=row["Battery_ID"]
        ))
    fig_temp.update_layout(
        title="Temperature (°C)",
        yaxis=dict(range=[0,50]),
        showlegend=False
    )
    
    # Display charts in 3 columns
    col1, col2, col3 = st.columns(3)
    col1.plotly_chart(fig_voltage, use_container_width=True)
    col2.plotly_chart(fig_resistance, use_container_width=True)
    col3.plotly_chart(fig_temp, use_container_width=True)

# =========================
# Battery Table
# =========================
if total > 0:
    st.subheader("Battery Details")
    icon_map = {"Reusable":"🔋","Recyclable":"🔋","Hazardous":"⚠️"}
    display_df = df.copy()
    display_df["Status"] = display_df["Status"].map(lambda x: f"{icon_map[x]} {x}")
    st.dataframe(display_df)

# =========================
# Hazard Alert
# =========================
if hazardous > 0:
    st.warning(f"⚠️ {hazardous} hazardous batteries detected! Handle with care!")
