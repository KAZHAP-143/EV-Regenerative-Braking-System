
from vehicle_3d import create_vehicle_3d
import streamlit as st
from vehicle_dynamics import simulate
import pandas as pd
from abs_vehicle_simulation import simulate_abs
from coordinated_braking_simulation import simulate_coordinated_braking

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
battery_temperature = st.sidebar.slider(
    "Battery Temperature (°C)",
    -20,
    60,
    25
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
    initial_soc=battery_soc / 100,
    battery_temperature=battery_temperature
)

# Energy recovery efficiency
vehicle_mass = 1500  # Must match vehicle_dynamics.py
initial_speed_ms = speed / 3.6

initial_kinetic_energy_kwh = (
    0.5 * vehicle_mass * initial_speed_ms**2
) / 3_600_000

recovered_energy_kwh = result["energy_kwh"]

recovery_efficiency = (
    100 * recovered_energy_kwh / initial_kinetic_energy_kwh
    if initial_kinetic_energy_kwh > 0
    else 0.0
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

st.metric(
    "Energy Recovery Efficiency",
    f"{recovery_efficiency:.2f}%"
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

import plotly.express as px

st.subheader("Energy Distribution")

fig = px.pie(
    energy_df,
    names="Energy Component",
    values="Energy (kWh)",
    title="Braking Energy Distribution",
    hole=0.35
)

st.plotly_chart(
    fig,
    use_container_width=True
)

if abs(energy_error) < 0.00001:
    st.success("Energy conservation test passed!")
else:
    st.warning("Energy balance requires further investigation.")

# ABS performance analysis
st.divider()

st.header("Anti-lock Braking System (ABS) Analysis")

st.caption(
    "Simplified quarter-car ABS simulation. "
    "Results are illustrative and not experimentally validated."
)

abs_road = st.selectbox(
    "ABS Road Condition",
    ["Dry Road", "Wet Road"],
    key="abs_road_condition"
)

abs_road_type = "dry" if abs_road == "Dry Road" else "wet"

if st.button("Run ABS Comparison"):
    with st.spinner("Running ABS simulations..."):
        abs_on = simulate_abs(
            road=abs_road_type,
            abs_enabled=True
        )

        
    abs_off = simulate_abs(
        road=abs_road_type,
        abs_enabled=False
    )

    st.subheader("ABS Braking Performance")
    st.subheader("Battery Operating Conditions")

    battery_soc_input = st.slider(
        "Initial Battery SOC (%)",
        min_value=0,
        max_value=100,
        value=60,
        step=5
    )

    battery_temperature_input = st.slider(
        "Battery Temperature (°C)",
        min_value=-10,
        max_value=60,
        value=25,
        step=5
    )
    coordinated_result = simulate_coordinated_braking(
        road=abs_road_type,
        abs_enabled=True,
        initial_soc=battery_soc_input / 100.0,
        battery_temperature=battery_temperature_input
    )

    st.metric(
        "Recovered Battery Energy — ABS ON",
        f"{coordinated_result['recovered_energy_kwh'] * 1000:.2f} Wh"
    )
    coordinated_result_off = simulate_coordinated_braking(
        road=abs_road_type,
        abs_enabled=False,
        initial_soc=battery_soc_input / 100.0,
        battery_temperature=battery_temperature_input
    )

    st.metric(
        "Recovered Battery Energy — ABS OFF",
        f"{coordinated_result_off['recovered_energy_kwh'] * 1000:.2f} Wh"
    )


     # Initial vehicle kinetic energy
    vehicle_mass = 1500.0
    initial_speed = 100.0 / 3.6

    initial_kinetic_energy_kwh = (
        0.5 * vehicle_mass * initial_speed**2
    ) / 3_600_000

    recovery_efficiency_on = (
        coordinated_result["recovered_energy_kwh"]
        / initial_kinetic_energy_kwh
    ) * 100

    recovery_efficiency_off = (
        coordinated_result_off["recovered_energy_kwh"]
        / initial_kinetic_energy_kwh
    ) * 100

    efficiency_col1, efficiency_col2 = st.columns(2)

    efficiency_col1.metric(
        "Energy Recovery — ABS ON",
        f"{recovery_efficiency_on:.2f}%"
    )

    efficiency_col2.metric(
        "Energy Recovery — ABS OFF",
        f"{recovery_efficiency_off:.2f}%"
    )   
    st.subheader("Regenerative Energy Comparison")

    energy_comparison = {
        "ABS Mode": ["ABS ON", "ABS OFF"],
        "Recovered Energy (Wh)": [
            coordinated_result["recovered_energy_kwh"] * 1000,
            coordinated_result_off["recovered_energy_kwh"] * 1000
        ]
    }

    st.bar_chart(
        energy_comparison,
        x="ABS Mode",
        y="Recovered Energy (Wh)"
    )



    col1, col2 = st.columns(2)

    col1.metric(
        "Stopping Distance — ABS ON",
        f"{abs_on['stop_distance']:.2f} m"
    )


    col2.metric(
        "Stopping Distance — ABS OFF",
        f"{abs_off['stop_distance']:.2f} m"
    )

    distance_reduction = (
        abs_off["stop_distance"] - abs_on["stop_distance"]
    )

    st.metric(
        "Stopping Distance Reduction",
        f"{distance_reduction:.2f} m"
    )

    slip_data = pd.DataFrame({
        "Time (s)": abs_on["history"]["time"],
        "Wheel Slip (%)": [
            slip * 100
            for slip in abs_on["history"]["slip"]
        ]
    })

    st.subheader("Wheel Slip — ABS ON")

    st.line_chart(
        slip_data.set_index("Time (s)")
    )

    # Compare ABS ON and ABS OFF wheel slip
    st.subheader("Wheel Slip Comparison — ABS ON vs OFF")

    abs_on_df = pd.DataFrame({
        "Time (s)": abs_on["history"]["time"],
        "ABS ON (%)": [
            slip * 100
            for slip in abs_on["history"]["slip"]
        ]
    })

    abs_off_df = pd.DataFrame({
        "Time (s)": abs_off["history"]["time"],
        "ABS OFF (%)": [
            slip * 100
            for slip in abs_off["history"]["slip"]
        ]
    })

    comparison_df = pd.merge_asof(
        abs_on_df.sort_values("Time (s)"),
        abs_off_df.sort_values("Time (s)"),
        on="Time (s)",
        direction="nearest"
    )

    st.line_chart(
        comparison_df.set_index("Time (s)")
    )

    st.success("ABS comparison completed!")
