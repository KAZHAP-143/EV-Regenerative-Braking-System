# EV Regenerative Braking System Simulation

### Python | Vehicle Dynamics | Electric Vehicles | Mechatronics Engineering

An interactive engineering simulation of an electric vehicle's regenerative braking system, developed using Python, NumPy, Streamlit, and Plotly.

## Project Overview

This project models the longitudinal braking behavior of an electric vehicle, including regenerative braking, friction braking, tire-road traction limits, and battery state-of-charge protection.

The objective is to investigate how braking demand, road conditions, vehicle speed, and battery charge level influence stopping performance and recovered electrical energy.

## Key Features

- Longitudinal vehicle dynamics simulation
- Regenerative and friction braking force distribution
- Dry-road and wet-road traction modeling
- Battery SOC protection and charging power limitation
- Electric motor torque constraints
- Aerodynamic drag and rolling resistance
- Interactive Streamlit dashboard
- Animated 3D vehicle visualization using Plotly
- Energy conservation analysis
- Automated engineering validation tests

## Mathematical Model

**Vehicle kinetic energy**

\[
E_k = \frac{1}{2}mv^2
\]

**Tire-road traction limit**

\[
F_{\max} = \mu mg
\]

**Longitudinal deceleration**

\[
a = \frac{F_{\text{braking}} + F_{\text{drag}} + F_{\text{rolling}}}{m}
\]

**Regenerative charging power**

\[
P_{\text{battery}} = F_{\text{regen}}v\eta
\]

The simulation uses numerical time stepping to calculate vehicle speed, stopping distance, recovered energy, and battery SOC.

## Engineering Validation

The model includes automated tests for:

1. Vehicle stopping behavior
2. Nonnegative vehicle speed
3. Dry-road versus wet-road stopping distance
4. Regenerative braking inhibition at full battery SOC
5. Numerical energy conservation

### Example Simulation Results

| Test | Result |
|---|---|
| Dry road, 4,500 N braking | 120.04 m stopping distance |
| Wet road, 4,500 N braking | 120.04 m stopping distance |
| Dry road, 10,000 N braking | 56.07 m stopping distance |
| Wet road, 10,000 N braking | 83.35 m stopping distance |
| Recovered energy at 60% SOC | 0.0920 kWh |
| Recovered energy at 100% SOC | 0 kWh |

These results demonstrate the implemented traction-limiting and battery-protection behavior.

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- Streamlit
- Plotly
- Python unittest

## Installation

Clone the repository and enter the project directory.

Create and activate a Python virtual environment, then install the project dependencies:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the interactive dashboard:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Run the automated tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

## Model Limitations

This is an educational engineering simulation, not a production-ready vehicle braking controller.

The current model uses simplified longitudinal dynamics and does not include wheel-slip dynamics, detailed ABS control, battery thermal behavior, or experimentally calibrated motor and tire characteristics.

## Future Development

- Advanced regenerative braking control strategies
- Battery thermal protection
- Wheel-slip and ABS modeling
- Improved 3D vehicle visualization
- Parameter sensitivity analysis
- Comparison with experimental vehicle data

## Project Category

Mechatronics Engineering | Automotive Engineering | Electric Vehicle Systems | Modeling and Simulation

## Project Screenshots

### Interactive EV Dashboard
![EV Dashboard](images/dashboard.png)

### Braking Performance Graphs
![Braking Graphs](images/braking_graphs.png)

### 3D Vehicle Visualization
![3D Vehicle](images/vehicle_3d.png)
