import streamlit as st
import requests
import psutil
import time

st.title("Mobile Price Predictor")
st.write("Send 20 numeric features to the local API at http://127.0.0.1:5000/predict")

# System status panel
st.markdown("---")
st.header("System Status")
col1, col2 = st.columns(2)

# Refresh control
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = 0

with col2:
    if st.button("Refresh system stats"):
        st.session_state.last_refresh = time.time()

# Read system stats
bat = psutil.sensors_battery()
mem = psutil.virtual_memory()

with col1:
    if bat is None:
        st.info("Battery: not available")
    else:
        st.metric("Battery", f"{bat.percent}%")
        st.progress(int(bat.percent))

    st.metric("RAM usage", f"{mem.percent}%")
    st.write(f"Used: {mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB")
    st.progress(int(mem.percent))

st.markdown("---")

# Main predictor UI
cols = st.columns(4)
features = []
for i in range(20):
    value = cols[i % 4].number_input(f"F{i+1}", value=float(i+1))
    features.append(value)

if st.button("Predict"):
    try:
        r = requests.post("http://127.0.0.1:5000/predict", json={"features": features}, timeout=5)
        r.raise_for_status()
        st.success(f"Prediction: {r.json()}")
    except Exception as e:
        st.error(f"Request failed: {e}")
