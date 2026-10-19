from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coordinated_braking_simulation import simulate_coordinated_braking

output = Path("results") / "stage50"
output.mkdir(parents=True, exist_ok=True)

settings = dict(
    initial_speed_kmh=100.0,
    initial_soc=0.60,
    abs_controller="predictive_pi",
    actuator_enabled=True,
    actuator_response_time=0.05,
    braking_mode="adaptive",
    tire_model="enhanced",
    initialization_mode="grip_based",
    prediction_time=0.030,
    pi_kp=60.0,
    pi_ki=10.0,
)

roads = ["dry", "wet", "snow"]
results = [
    simulate_coordinated_braking(road=road, **settings)
    for road in roads
]

metrics = [
    ("stop_distance", "Stopping Distance", "Distance (m)",
     "stopping_distance.png"),
    ("stop_time", "Braking Time", "Time (s)",
     "braking_time.png"),
    ("recovered_energy_kwh", "Recovered Battery Energy",
     "Energy (kWh)", "recovered_energy.png"),
]

for key, title, ylabel, filename in metrics:
    values = [result[key] for result in results]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar([road.title() for road in roads], values)

    ax.set_title(f"EV Regenerative Braking - {title}")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Road Surface")
    ax.set_ylim(0, max(values) * 1.18)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.4f}",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    destination = output / filename
    fig.savefig(destination, dpi=200)
    plt.close(fig)

    print(f"Saved: {destination}")

print("Stage 50: All three engineering graphs generated.")
