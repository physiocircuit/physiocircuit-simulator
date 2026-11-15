import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Configuración de interfaz inmersiva
st.set_page_config(
    page_title="PhysioCircuit Studio | Cybernetic Control Systems",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS para presentación tipo cockpit médico
st.markdown("""
<style>
    .cyber-card {
        background-color: #0f172a;
        color: #f8fafc;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #334155;
    }
    .node-box {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .node-ok { background-color: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .node-warn { background-color: #fef9c3; color: #854d0e; border: 1px solid #fde047; }
    .node-fail { background-color: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
</style>
""", unsafe_allow_html=True)

# Encabezado
st.title("⚡ PhysioCircuit: Clinical Control Systems Simulator")
st.caption("Cybernetic modeling based on Modell et al. (2015), Set Point Relativity (Kuang, 2023), and Dynamic Homeostatic Tendency (Billman, 2020).")

# 1. Parámetros del Sistema en la Barra Lateral
st.sidebar.header("🕹️ Circuit Configuration")

circuit_mode = st.sidebar.selectbox(
    "Select Biological Circuit",
    [
        "Core Body Temperature (Thermoregulation)",
        "Mean Arterial Pressure (Baroreceptor Reflex)",
        "Plasma Glucose Regulation"
    ]
)

if circuit_mode == "Core Body Temperature (Thermoregulation)":
    base_sp = 37.0
    unit = "°C"
    var_name = "Core Temperature"
    sensor_name = "Hypothalamic Thermoreceptors"
    controller_name = "Preoptic Anterior Hypothalamus"
    effector_name = "Vasomotor Tone & Sweating/Shivering"
    effector_unit = "W/m²"
    y_limits = (33.0, 42.5)
    k_default = 1.2
    stress_label = "Thermal Stress (°C Eq.)"
    adaptive_name = "Pyrogen Set Point Reset (Fever)"
    adaptive_val = 1.8
elif circuit_mode == "Mean Arterial Pressure (Baroreceptor Reflex)":
    base_sp = 93.3
    unit = "mmHg"
    var_name = "Mean Arterial Pressure"
    sensor_name = "Carotid & Aortic Baroreceptors"
    controller_name = "Medullary Cardiovascular Center"
    effector_name = "Cardiac Output & Vascular Resistance"
    effector_unit = "% baseline"
    y_limits = (45.0, 160.0)
    k_default = 1.0
    stress_label = "Orthostatic / Volume Loss (mmHg Eq.)"
    adaptive_name = "Exercise Dynamic Pressor Reset"
    adaptive_val = 20.0
else:
    base_sp = 90.0
    unit = "mg/dL"
    var_name = "Plasma Glucose"
    sensor_name = "Pancreatic Islet Glucosensors"
    controller_name = "Endocrine Pancreatic Network"
    effector_name = "Insulin vs. Glucagon Secretion"
    effector_unit = "µU/mL"
    y_limits = (40.0, 240.0)
    k_default = 0.9
    stress_label = "Carbohydrate Intake / Fasting (mg/dL Eq.)"
    adaptive_name = "Dawn Phenomenon / Cortisol Surge"
    adaptive_val = 30.0

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Control Loop Tuning")

controller_gain = st.sidebar.slider(
    "Controller Negative Feedback Gain (k)",
    min_value=0.1, max_value=3.0, value=float(k_default), step=0.1,
    help="Determines effector reaction magnitude per unit of detected error."
)

disturbance_strength = st.sidebar.slider(
    f"External Disturbance: {stress_label}",
    min_value=-25.0, max_value=25.0, value=10.0, step=1.0,
    help="Environmental or systemic challenge challenging stability."
)

st.sidebar.markdown("---")
st.sidebar.subheader("🩺 Clinical Pathophysiology")

adaptive_reset = st.sidebar.checkbox(
    f"Activate {adaptive_name}",
    help="Kuang (2023): Demonstrates that set points are relative and dynamically adapt to context."
)

sensor_failure = st.sidebar.checkbox(
    "Simulate Acute Sensor Failure (Open-Loop Defect)",
    help="Modell et al. (2015): Afferent limb disconnected. Error detector registers total absence of signal."
)

effector_fatigue = st.sidebar.checkbox(
    "Simulate Effector Exhaustion / Failure",
    help="Billman (2020): Effector capacity depleted, leading to regulatory collapse."
)
