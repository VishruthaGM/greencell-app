import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Simulate 50 AA/AAA batteries
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

# Classification function for AA/AAA batteries
def classify_aa(row):
    if row['Temperature'] > 40 or row['Internal_Resistance'] > 1.0 or row['Open_Circuit_Voltage'] < 1.3:
        return 'Hazardous'
    elif row['Internal_Resistance'] <= 0.5 and row['Open_Circuit_Voltage'] >= 1.5:
        return 'Reusable'
    else:
        return 'Recyclable'

df['Status'] = df.apply(classify_aa, axis=1)

# Streamlit Dashboard
st.title("💚 GreenCell: Battery Health Dashboard")
st.subheader("Battery Data")
st.dataframe(df)

st.subheader("Battery Status Distribution")
fig = px.pie(df, names='Status', title='Reusable / Recyclable / Hazardous Batteries')
st.plotly_chart(fig)

st.subheader("Batteries by Status")
status_option = st.selectbox("Select Status", ['All', 'Reusable', 'Recyclable', 'Hazardous'])
if status_option != 'All':
    st.dataframe(df[df['Status'] == status_option])
else:
    st.dataframe(df)
