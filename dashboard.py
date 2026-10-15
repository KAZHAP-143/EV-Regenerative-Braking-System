
from vehicle_3d import create_vehicle_3d
import streamlit as st
from vehicle_dynamics import simulate
import pandas as pd
st.set_page_config(
    page_title="EV Regenerative Braking",
    page_icon="🚗",
    layout="wide"
)

st.title("EV Regenerative Braking System")
st.subheader("Interactive Vehicle Simulation")

st.sidebar.header("Vehicle Controls")

speed = st.sidebar.slider(
    "Initial Speed (km/h)", 0, 150, 100
)

braking_force = st.sidebar.slider(
    "Braking Force (N)", 1000, 12000, 4500
)

road = st.sidebar.selectbox(
    "Road Condition",
    ["Dry Road", "Wet Road"]
)

battery_soc = st.sidebar.slider(
    "Battery SOC (%)", 0, 100, 60
)

st.header("Vehicle Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Initial Speed", f"{speed} km/h")
col2.metric("Requested Braking Force", f"{braking_force} N")
col3.metric("Battery SOC", f"{battery_soc}%")

st.info(f"Selected Road Condition: {road}")

st.caption(
    "Dashboard interface initialized. "
    "Simulation calculations will be connected next."
)
# Run vehicle simulation
mu = 0.85 if road == "Dry Road" else 0.45

result = simulate(
    mu=mu,
    initial_speed_kmh=speed,
    brake_force=braking_force,
    initial_soc=battery_soc / 100
)

st.header("Simulation Results")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Stopping Time",
    f"{result['stop_time']:.2f} s"
)

col2.metric(
    "Stopping Distance",
    f"{result['distance']:.2f} m"
)

col3.metric(
    "Recovered Energy",
    f"{result['energy_kwh']:.4f} kWh"
)

# Speed graph
chart_data = pd.DataFrame({
    "Time (s)": result["time"],
    "Speed (km/h)": result["speed"]
})

st.subheader("Vehicle Speed During Braking")

st.line_chart(
    chart_data.set_index("Time (s)")
)

# Braking force distribution
st.subheader("Regenerative vs Friction Braking")

braking_data = pd.DataFrame({
    "Time (s)": result["time"],
    "Regenerative Braking (N)": result["regen_force"],
    "Friction Braking (N)": result["friction_force"]
})

st.line_chart(braking_data.set_index("Time (s)"))

# Battery state of charge
st.subheader("Battery State of Charge")

soc_data = pd.DataFrame({
    "Time (s)": result["time"],
    "Battery SOC (%)": result["soc"]
})

st.line_chart(soc_data.set_index("Time (s)"))

# Battery charging power
st.subheader("Regenerative Charging Power")

power_data = pd.DataFrame({
    "Time (s)": result["time"],
    "Charging Power (kW)": result["battery_power_kw"]
})

st.line_chart(power_data.set_index("Time (s)"))

# Stage 11: Animated braking simulation

import time

st.header("Live Braking Simulation")

if st.button("▶ Start Simulation"):

    speed_display = st.empty()
    soc_display = st.empty()
    regen_display = st.empty()
    progress_display = st.progress(0)

    total_steps = len(result["time"])

    # Playback of previously calculated simulation data
    for i in range(total_steps):

        speed_display.metric(
            "Vehicle Speed",
            f"{result['speed'][i]:.1f} km/h"
        )

        soc_display.metric(
            "Battery SOC",
            f"{result['soc'][i]:.3f}%"
        )

        regen_display.metric(
            "Regenerative Braking Force",
            f"{result['regen_force'][i]:.0f} N"
        )

        progress = int(
            (i + 1) / total_steps * 100
        )

        progress_display.progress(progress)

        time.sleep(0.01)

    st.success("Vehicle stopped successfully!")
st.header("3D Vehicle Visualization")


st.write("Watch the electric vehicle brake and stop.")

if st.button("▶ Animate 3D Vehicle"):
    vehicle_display = st.empty()

    total_steps = len(result["time"])
    frame_step = max(1, total_steps // 60)

    for i in list(range(0, total_steps, frame_step)) + [total_steps - 1]:
        # Estimate vehicle position from stopping-distance history
        position = float(result["distance_history"][i])

        fig = create_vehicle_3d(position=position)

        vehicle_display.plotly_chart(
    fig,
    use_container_width=True,
    key=f"vehicle_3d_frame_{i}"
)
              

        time.sleep(0.05)

    st.success("3D vehicle stopped!")

st.header("Energy Conservation Validation")

initial_speed_ms = speed / 3.6
initial_energy_kwh = (
    0.5 * 1500 * initial_speed_ms**2 / 3_600_000
)

energy_components = {
    "Recovered Battery Energy": result["energy_kwh"],
    "Friction Brake Heat": result["friction_energy_kwh"],
    "Aerodynamic Loss": result["drag_energy_kwh"],
    "Rolling Resistance Loss": result["rolling_energy_kwh"],
    "Motor Conversion Loss": result["motor_loss_energy_kwh"],
}

total_accounted_energy = sum(energy_components.values())
energy_error = initial_energy_kwh - total_accounted_energy

st.metric("Initial Kinetic Energy", f"{initial_energy_kwh:.5f} kWh")
st.metric("Total Accounted Energy", f"{total_accounted_energy:.5f} kWh")
st.metric("Energy Balance Error", f"{energy_error:.8f} kWh")

energy_df = pd.DataFrame({
    "Energy Component": list(energy_components.keys()),
    "Energy (kWh)": list(energy_components.values())
})

st.bar_chart(energy_df.set_index("Energy Component"))

if abs(energy_error) < 0.00001:
    st.success("Energy conservation test passed!")
else:
    st.warning("Energy balance requires further investigation.")
