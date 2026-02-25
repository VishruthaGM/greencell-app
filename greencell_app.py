import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="💚 GreenCell Real-Time Dashboard", layout="wide")
st.title("💚 GreenCell: Smart Battery Health Real-Time Simulation")

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
# Initialize empty dataframe for tested batteries
tested_df = pd.DataFrame(columns=df.columns)

st.subheader("Real-Time Battery Testing Simulation")
placeholder_table = st.empty()
placeholder_summary = st.empty()
placeholder_chart = st.empty()
placeholder_alert = st.empty()

# =========================
# Simulate real-time testing
# =========================
for i in range(len(df)):
    battery = df.iloc[i:i+1]
    tested_df = pd.concat([tested_df, battery])

    # Update summary
    total = len(tested_df)
    reusable = len(tested_df[tested_df['Status']=='Reusable'])
    recyclable = len(tested_df[tested_df['Status']=='Recyclable'])
    hazardous = len(tested_df[tested_df['Status']=='Hazardous'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tested", total)
    col2.metric("Reusable 💚", reusable, f"{reusable/total*100:.1f}%")
    col3.metric("Recyclable 🟡", recyclable, f"{recyclable/total*100:.1f}%")
    col4.metric("Hazardous 🔴", hazardous, f"{hazardous/total*100:.1f}%")

    # Update pie chart
    fig = px.pie(tested_df, names='Status',
                 color='Status', color_discrete_map={'Reusable':'green','Recyclable':'yellow','Hazardous':'red'},
                 title='Battery Status Distribution')
    placeholder_chart.plotly_chart(fig, use_container_width=True)

    # Update table
    status_colors = {'Reusable':'💚', 'Recyclable':'🟡', 'Hazardous':'🔴'}
    display_df = tested_df.copy()
    display_df['Status'] = display_df['Status'].map(lambda x: f"{status_colors[x]} {x}")
    placeholder_table.dataframe(display_df)

    # Hazard alert
    if hazardous > 0:
        placeholder_alert.warning(f"⚠️ {hazardous} hazardous batteries detected! Handle with care!")
    else:
        placeholder_alert.empty()

    # Pause to simulate testing time
    time.sleep(0.5)
