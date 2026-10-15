
import matplotlib.pyplot as plt
from abs_vehicle_simulation import simulate_abs

scenarios = [
    ("Dry - ABS ON", "dry", True),
    ("Dry - ABS OFF", "dry", False),
    ("Wet - ABS ON", "wet", True),
    ("Wet - ABS OFF", "wet", False),
]

labels = []
distances = []

for label, road, abs_enabled in scenarios:
    result = simulate_abs(
        road=road,
        abs_enabled=abs_enabled
    )

    labels.append(label)
    distances.append(result["stop_distance"])

plt.figure(figsize=(10, 6))

bars = plt.bar(labels, distances)

for bar, distance in zip(bars, distances):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        distance + 2,
        f"{distance:.2f} m",
        ha="center"
    )

plt.ylabel("Stopping Distance (m)")
plt.title("ABS Braking Performance Comparison")
plt.ylim(0, max(distances) * 1.15)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "images/abs_stopping_distance_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("ABS comparison graph saved successfully!")
