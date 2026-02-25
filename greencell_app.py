import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="💚 GreenCell Interactive Dashboard", layout="wide", page_icon="💚")
st.title("💚 GreenCell: Interactive Battery Health Analyzer")

# =========================
# Initialize session state
# =========================
if "tested_batteries" not in st.session_state:
    st.session_state.tested_batteries = pd.DataFrame(columns=[
        "Battery_ID", "Open_Circuit_Voltage", "Load_Voltage",
        "Current", "Temperature", "Internal_Resistance", "Status"
    ])
if "battery_count" not in st.session_state:
    st.session_state.battery_count = 0

# =========================
# Function: simulate a battery
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
# Layout: Add Battery Button + Progress Bar
# =========================
st.subheader("Process a New Battery")
if st.button("Add Battery"):
    progress = st.progress(0)
    for i in range(0, 101, 20):
        time.sleep(0.2)  # simulate measurement delay
        progress.progress(i)
    
    new_battery = simulate_battery()
    st.session_state.tested_batteries = pd.concat([
        st.session_state.tested_batteries,
        pd.DataFrame([new_battery])
    ])
    st.success(f"✅ {new_battery['Battery_ID']} processed and added!")

# =========================
# Display Summary Cards
# =========================
tested_df = st.session_state.tested_batteries
total = len(tested_df)
reusable = len(tested_df[tested_df['Status']=="Reusable"])
recyclable = len(tested_df[tested_df['Status']=="Recyclable"])
hazardous = len(tested_df[tested_df['Status']=="Hazardous"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Batteries", total)
col2.metric("Reusable 💚", reusable, f"{reusable/total*100:.1f}%" if total>0 else "0%")
col3.metric("Recyclable 🟡", recyclable, f"{recyclable/total*100:.1f}%" if total>0 else "0%")
col4.metric("Hazardous 🔴", hazardous, f"{hazardous/total*100:.1f}%" if total>0 else "0%")

st.markdown("---")

# =========================
# Pie Chart: Status Distribution
# =========================
if total > 0:
    fig = px.pie(
        tested_df, names="Status",
        color="Status",
        color_discrete_map={"Reusable":"green","Recyclable":"orange","Hazardous":"red"},
        title="Battery Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# Battery Table with Icons
# =========================
if total > 0:
    icon_map = {"Reusable":"🔋","Recyclable":"🔋","Hazardous":"⚠️"}  # use battery/alert icons
    display_df = tested_df.copy()
    display_df["Status"] = display_df["Status"].map(lambda x: f"{icon_map[x]} {x}")
    st.subheader("Battery Details")
    st.dataframe(display_df)

# =========================
# Analytics: Voltage / Resistance / Temperature
# =========================
if total > 0:
    st.subheader("Battery Analytics")
    col_v, col_r, col_t = st.columns(3)
    col_v.bar_chart(tested_df['Open_Circuit_Voltage'], height=200)
    col_r.bar_chart(tested_df['Internal_Resistance'], height=200)
    col_t.bar_chart(tested_df['Temperature'], height=200)

# =========================
# Hazardous Alert
# =========================
if hazardous > 0:
    st.warning(f"⚠️ {hazardous} hazardous batteries detected! Handle with care!")
