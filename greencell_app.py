import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# Simulate AA/AAA Battery Data
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
# Classification Function
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
# Dashboard Layout
# =========================
st.set_page_config(page_title="💚 GreenCell Dashboard", layout="wide")
st.title("💚 GreenCell: Smart Battery Health Dashboard")

# Summary Cards
total = len(df)
reusable = len(df[df['Status']=='Reusable'])
recyclable = len(df[df['Status']=='Recyclable'])
hazardous = len(df[df['Status']=='Hazardous'])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Batteries", total)
col2.metric("Reusable 💚", reusable, f"{reusable/total*100:.1f}%")
col3.metric("Recyclable 🟡", recyclable, f"{recyclable/total*100:.1f}%")
col4.metric("Hazardous 🔴", hazardous, f"{hazardous/total*100:.1f}%")

st.markdown("---")

# =========================
# Pie Chart
# =========================
st.subheader("Battery Status Distribution")
fig = px.pie(df, names='Status', title='Reusable / Recyclable / Hazardous Batteries',
             color='Status', color_discrete_map={'Reusable':'green','Recyclable':'yellow','Hazardous':'red'})
st.plotly_chart(fig, use_container_width=True)

# =========================
# Detailed Table with Colored Status
# =========================
st.subheader("Battery Details")
status_colors = {'Reusable':'💚', 'Recyclable':'🟡', 'Hazardous':'🔴'}
df_display = df.copy()
df_display['Status'] = df_display['Status'].map(lambda x: f"{status_colors[x]} {x}")
st.dataframe(df_display)

# =========================
# Filter by Status
# =========================
st.subheader("Filter Batteries by Status")
status_option = st.selectbox("Select Status", ['All', 'Reusable', 'Recyclable', 'Hazardous'])
if status_option != 'All':
    st.dataframe(df[df['Status']==status_option])
else:
    st.dataframe(df)

# =========================
# Analytics: Voltage, Resistance, Temperature
# =========================
st.subheader("Battery Analytics")
col1, col2, col3 = st.columns(3)
col1.bar_chart(df['Open_Circuit_Voltage'])
col2.bar_chart(df['Internal_Resistance'])
col3.bar_chart(df['Temperature'])

# =========================
# Optional: Alerts for Hazardous Batteries
# =========================
if hazardous > 0:
    st.warning(f"⚠️ There are {hazardous} hazardous batteries. Handle with care!")
