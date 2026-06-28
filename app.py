import streamlit as st

from src.model import (
    train_model,
    predict_water_output,
    get_system_status
)

st.set_page_config(
    page_title="AquaMind AI",
    page_icon="🌊",
    layout="centered"
)

# ============================
# Header
# ============================

st.title("AquaMind AI")

st.markdown(
    """
    **AI-powered performance prediction for solar desalination systems.**

    AquaMind AI estimates water production using environmental inputs and a
    machine learning model trained on simulated desalination data.
    """
)

st.divider()

# ============================
# Sidebar
# ============================

st.sidebar.header("Input Conditions")

temperature = st.sidebar.slider(
    "Temperature (°C)",
    min_value=20,
    max_value=60,
    value=35
)

humidity = st.sidebar.slider(
    "Humidity (%)",
    min_value=20,
    max_value=100,
    value=60
)

solar_intensity = st.sidebar.slider(
    "Solar Intensity (W/m²)",
    min_value=200,
    max_value=1200,
    value=800
)

salinity = st.sidebar.slider(
    "Salinity (ppt)",
    min_value=20,
    max_value=50,
    value=35
)

# ============================
# Machine Learning
# ============================

model, accuracy = train_model()

prediction = predict_water_output(
    model,
    temperature,
    humidity,
    solar_intensity,
    salinity
)

performance_index = (prediction / solar_intensity) * 100

status, status_level = get_system_status(prediction)

# ============================
# Results
# ============================

st.subheader("Prediction Results")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Predicted Water Production",
        value=f"{prediction:.2f} L/day"
    )

with col2:
    st.metric(
        label="Performance Index",
        value=f"{performance_index:.2f}%"
    )

# ============================
# Status
# ============================

st.subheader("Production Potential")

if status_level == "success":
    st.success(f"{status}")

elif status_level == "warning":
    st.warning(f"{status}")

else:
    st.error(f"{status}")

st.divider()

# ============================
# Input Summary
# ============================

st.subheader("Input Summary")

st.write(f"Temperature: **{temperature} °C**")
st.write(f"Humidity: **{humidity}%**")
st.write(f"Solar Intensity: **{solar_intensity} W/m²**")
st.write(f"Salinity: **{salinity} ppt**")

# ============================
# AI Insights
# ============================

st.subheader("AI Insights")

st.info(
    "AI-generated insights, explainable AI (XAI), and design optimization "
    "features will be introduced in Version 6."
)

# ============================
# Model Information
# ============================

st.subheader("Model Information")

st.write("Algorithm: **Linear Regression**")
st.write(f"Model Accuracy: **{accuracy * 100:.2f}%**")