import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PhysioCircuit Lab", layout="wide", page_icon="⚡")

st.title("⚡ PhysioCircuit: Clinical Control Systems Simulator")
st.markdown("""
*Based on the 5-component negative feedback control theory (Modell et al., 2015; Billman, 2020).*
Experiment with feedback gains, set point relativity, and acute sensor failures in real time.
""")

st.sidebar.header("🕹️ System Calibration Controls")

system_mode = st.sidebar.selectbox(
    "Select Physiological Circuit",
    ["Core Body Temperature (Thermoregulation)", "Mean Arterial Pressure (Baroreceptor Reflex)", "Blood Glucose Regulation"]
)

if system_mode == "Core Body Temperature (Thermoregulation)":
    default_sp = 37.0
    unit = "°C"
    var_name = "Core Temperature"
    y_min, y_max = 34.0, 41.0
elif system_mode == "Mean Arterial Pressure (Baroreceptor Reflex)":
    default_sp = 93.0
    unit = "mmHg"
    var_name = "Mean Arterial Pressure (MAP)"
    y_min, y_max = 50.0, 150.0
else:
    default_sp = 90.0
    unit = "mg/dL"
    var_name = "Plasma Glucose"
    y_min, y_max = 40.0, 220.0

set_point = st.sidebar.slider(f"Target Set Point ({unit})", min_value=float(y_min + 5), max_value=float(y_max - 5), value=float(default_sp), step=0.5)
controller_gain = st.sidebar.slider("Negative Feedback Controller Gain (k)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
sensor_failure = st.sidebar.checkbox("Simulate Acute Sensor Failure (Open-Loop Pathology)")
perturbation_strength = st.sidebar.slider("External Environmental Disturbance", min_value=-15.0, max_value=15.0, value=5.0, step=1.0)

# Simulation loop (Euler numerical method)
time = np.linspace(0, 50, 200)
dt = time[1] - time[0]
regulated_var = np.zeros_like(time)
regulated_var[0] = set_point

for i in range(1, len(time)):
    current_val = regulated_var[i-1]
    sensed_val = 0.0 if sensor_failure else current_val
    error = set_point - sensed_val
    response = controller_gain * error
    ext_disturbance = perturbation_strength if (time[i] > 10 and time[i] < 35) else 0.0
    d_val = -0.5 * (current_val - set_point) + response + ext_disturbance
    regulated_var[i] = current_val + d_val * dt

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(time, regulated_var, color="#0066CC", lw=2.5, label=f"{var_name} ({unit})")
    ax.axhline(set_point, color="#DC2626", linestyle="--", lw=1.5, label=f"Set Point ({set_point} {unit})")
    ax.axvspan(10, 35, color="#F3F4F6", alpha=0.7, label="External Disturbance Window")
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time (Arbitrary Minutes)", fontsize=11)
    ax.set_ylabel(f"Regulated Variable ({unit})", fontsize=11)
    ax.set_title(f"Dynamic Response Curve: {var_name}", fontsize=13, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")
    st.pyplot(fig)

with col2:
    st.subheader("📋 Real-Time Diagnostic Telemetry")
    current_error = set_point - (0.0 if sensor_failure else regulated_var[-1])
    st.metric("Regulated Variable (End Value)", f"{regulated_var[-1]:.2f} {unit}")
    st.metric("Set Point", f"{set_point:.1f} {unit}")
    st.metric("Detected System Error", f"{current_error:.2f} {unit}")
    
    if sensor_failure:
        st.error("⚠️ CRITICAL ALERT: Sensor open-loop failure active. Effector unable to read physiological variable.")
    elif abs(current_error) < 0.5:
        st.success("✅ OPTIMAL HOMEOSTASIS: Controller effectively neutralizing environmental disturbances.")
    else:
        st.warning("⚡ COMPENSATORY DRIFT: Error detector registering steady-state offset.")
