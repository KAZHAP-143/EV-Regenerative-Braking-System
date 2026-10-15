
from vehicle_dynamics import simulate
import matplotlib.pyplot as plt

# Run braking simulation
result = simulate(
    mu=0.85,
    initial_speed_kmh=100,
    brake_force=4500,
    initial_soc=0.60,
    battery_temperature=25
)

# Energy distribution in kWh
energy_values = [
    result["energy_kwh"],
    result["friction_energy_kwh"],
    result["drag_energy_kwh"],
    result["rolling_energy_kwh"],
    result["motor_loss_energy_kwh"]
]

labels = [
    "Battery Recovery",
    "Friction Braking",
    "Aerodynamic Drag",
    "Rolling Resistance",
    "Motor Losses"
]

# Check energy balance
total_energy = sum(energy_values)

print("Energy Breakdown")
for label, value in zip(labels, energy_values):
    print(f"{label}: {value:.4f} kWh")

print(f"Total accounted energy: {total_energy:.4f} kWh")

# Verify against initial vehicle kinetic energy
vehicle_mass = 1500  # Must match vehicle_dynamics.py
initial_speed_ms = 100 / 3.6

initial_energy_kwh = (
    0.5 * vehicle_mass * initial_speed_ms**2
) / 3_600_000

energy_balance_error = (
    initial_energy_kwh - total_energy
)

print(f"Initial kinetic energy: {initial_energy_kwh:.4f} kWh")
print(f"Energy balance error: {energy_balance_error:.6f} kWh")

# Create pie chart
plt.figure(figsize=(9, 7))
plt.pie(
    energy_values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("EV Braking Energy Distribution at 100 km/h")
plt.tight_layout()

plt.savefig(
    "energy_loss_breakdown.png",
    dpi=300,
    bbox_inches="tight"
)

print("Energy loss graph saved successfully!")
