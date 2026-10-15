
from vehicle_dynamics import simulate
import matplotlib.pyplot as plt

speeds = [20, 40, 60, 80, 100, 120]
recovered_energy = []

for speed in speeds:
    result = simulate(
        mu=0.85,
        initial_speed_kmh=speed,
        brake_force=4500,
        initial_soc=0.60,
        battery_temperature=25
    )

    recovered_energy.append(result["energy_kwh"])

plt.figure(figsize=(9, 5))
plt.plot(speeds, recovered_energy, marker="o")
plt.xlabel("Initial Vehicle Speed (km/h)")
plt.ylabel("Recovered Energy (kWh)")
plt.title("Regenerative Braking Energy Recovery vs Speed")
plt.grid(True)
plt.tight_layout()
plt.savefig("performance_graph.png", dpi=300, bbox_inches="tight")
print("Graph saved successfully!")

# Compare dry and wet road braking performance
dry_distances = []
wet_distances = []

for speed in speeds:
    dry = simulate(
        mu=0.85,
        initial_speed_kmh=speed,
        brake_force=10000,
        initial_soc=0.60,
        battery_temperature=25
    )

    wet = simulate(
        mu=0.55,
        initial_speed_kmh=speed,
        brake_force=10000,
        initial_soc=0.60,
        battery_temperature=25
    )

    dry_distances.append(dry["distance"])
    wet_distances.append(wet["distance"])

plt.figure(figsize=(9, 5))
plt.plot(speeds, dry_distances, marker="o", label="Dry road")
plt.plot(speeds, wet_distances, marker="s", label="Wet road")

plt.xlabel("Initial Vehicle Speed (km/h)")
plt.ylabel("Stopping Distance (m)")
plt.title("Braking Distance: Dry vs Wet Road")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "road_condition_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("Road comparison graph saved successfully!")
