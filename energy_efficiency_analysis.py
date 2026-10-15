
from vehicle_dynamics import simulate
import matplotlib.pyplot as plt

# Vehicle mass must match vehicle_dynamics.py
vehicle_mass = 1500  # kg

speeds = [20, 40, 60, 80, 100, 120]
efficiencies = []

for speed in speeds:
    result = simulate(
        mu=0.85,
        initial_speed_kmh=speed,
        brake_force=4500,
        initial_soc=0.60,
        battery_temperature=25
    )

    speed_ms = speed / 3.6

    initial_kinetic_energy = (
        0.5 * vehicle_mass * speed_ms**2
    )

    recovered_energy = result["energy_kwh"] * 3_600_000

    efficiency = (
        100 * recovered_energy / initial_kinetic_energy
    )

    efficiencies.append(efficiency)

    print(f"{speed} km/h: {efficiency:.2f}%")

plt.figure(figsize=(9, 5))
plt.plot(speeds, efficiencies, marker="o")
plt.xlabel("Initial Vehicle Speed (km/h)")
plt.ylabel("Energy Recovery (%)")
plt.title("Regenerative Braking Energy Recovery Efficiency")
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "energy_efficiency_graph.png",
    dpi=300,
    bbox_inches="tight"
)

print("Energy efficiency graph saved successfully!")
