import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Entropy Calculator", layout="wide")
st.title("Entropy & the Second Law of Thermodynamics 🌡️")
st.markdown("Interactive tool to calculate work, heat, and entropy change for different thermodynamic processes.")

# -----------------------------
# User Inputs
# -----------------------------
st.sidebar.header("Process Parameters")
process_type = st.sidebar.selectbox("Select Process Type:", 
                                    ["Isothermal", "Isobaric", "Isochoric", "Adiabatic"])

n = st.sidebar.number_input("Number of moles (n)", min_value=0.1, value=1.0, step=0.1)

R = 8.314  # J/mol·K

T_i = st.sidebar.number_input("Initial Temperature T_i (K)", min_value=0.0, value=300.0)
T_f = st.sidebar.number_input("Final Temperature T_f (K)", min_value=0.0, value=400.0)

V_i = st.sidebar.number_input("Initial Volume V_i (m³)", min_value=0.0, value=0.01)
V_f = st.sidebar.number_input("Final Volume V_f (m³)", min_value=0.0, value=0.02)

C_v = st.sidebar.number_input("C_v (J/mol·K)", min_value=0.0, value=20.8)
C_p = st.sidebar.number_input("C_p (J/mol·K)", min_value=0.0, value=29.1)

# -----------------------------
# Process Info Text
# -----------------------------
process_info = {
    "Isothermal": """**Isothermal Process**  
- Temperature remains constant (T = constant)  
- Work done: W = nRT ln(V_f / V_i)  
- Heat transfer: Q = W  
- Entropy change: ΔS = nR ln(V_f / V_i)  
- Entropy increases if expansion, decreases if compression  
- Q ≠ 0, ΔS ≠ 0""",

    "Isobaric": """**Isobaric Process**  
- Pressure remains constant (P = constant)  
- Work done: W = P ΔV  
- Heat transfer: Q = n C_p ΔT  
- Entropy change: ΔS = n C_p ln(T_f / T_i)  
- Volume changes linearly with temperature  
- Q ≠ 0, ΔS ≠ 0""",

    "Isochoric": """**Isochoric Process**  
- Volume remains constant (V = constant)  
- Work done: W = 0  
- Heat transfer: Q = n C_v ΔT  
- Entropy change: ΔS = n C_v ln(T_f / T_i)  
- No work is done  
- Q ≠ 0, ΔS ≠ 0""",

    "Adiabatic": """**Adiabatic Process**  
- No heat transfer (Q = 0)  
- Work done: W = n C_v (T_i - T_f)  
- Entropy change: ΔS = 0 (**Isentropic**)  
- Temperature and volume change according to adiabatic relations  
- Q = 0, ΔS = 0"""
}

# Display process info
st.subheader("Process Info")
st.markdown(process_info[process_type])

# -----------------------------
# Calculations
# -----------------------------
W = Q = Delta_S = None

if st.button("Calculate"):
    if process_type == "Isothermal":
        W = n * R * T_i * np.log(V_f / V_i)
        Q = W
        Delta_S = n * R * np.log(V_f / V_i)
    elif process_type == "Isobaric":
        W = 0  # Placeholder, actual W = P ΔV if P known
        Q = n * C_p * (T_f - T_i)
        Delta_S = n * C_p * np.log(T_f / T_i)
    elif process_type == "Isochoric":
        W = 0
        Q = n * C_v * (T_f - T_i)
        Delta_S = n * C_v * np.log(T_f / T_i)
    elif process_type == "Adiabatic":
        Q = 0
        W = n * C_v * (T_i - T_f)
        Delta_S = 0

    # -----------------------------
    # Display Results
    # -----------------------------
    st.subheader("Results")
    st.write(f"Process Type: **{process_type}**")
    st.write(f"Work (W): {W:.2f} J")
    st.write(f"Heat (Q): {Q:.2f} J")
    st.write(f"Entropy Change (ΔS): {Delta_S:.2f} J/K")

    # -----------------------------
    # T-S Diagram
    # -----------------------------
    st.subheader("T-S Diagram")

    if Delta_S != 0:
        S_vals = np.linspace(0, Delta_S, 100)
    else:
        S_vals = [0,0]

    T_vals = np.linspace(T_i, T_f, len(S_vals))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_vals, y=T_vals, mode='lines+markers', name='Process'))
    fig.update_layout(
        xaxis_title="Entropy (J/K)",
        yaxis_title="Temperature (K)",
        title=f"{process_type} Process T-S Diagram"
    )
    st.plotly_chart(fig, use_container_width=True)
