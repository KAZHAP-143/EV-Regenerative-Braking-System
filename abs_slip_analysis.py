
import matplotlib.pyplot as plt
from abs_vehicle_simulation import simulate_abs

# Run wet-road braking simulations
abs_on = simulate_abs(road="wet", abs_enabled=True)
abs_off = simulate_abs(road="wet", abs_enabled=False)

# Extract simulation histories
time_on = abs_on["history"]["time"]
slip_on = [s * 100 for s in abs_on["history"]["slip"]]

time_off = abs_off["history"]["time"]
slip_off = [s * 100 for s in abs_off["history"]["slip"]]

# Plot wheel slip against time
plt.figure(figsize=(10, 6))

plt.plot(
    time_on,
    slip_on,
    label="ABS ON",
    linewidth=1.5
)

plt.plot(
    time_off,
    slip_off,
    label="ABS OFF",
    linewidth=1.5
)

plt.axhline(
    y=20,
    linestyle="--",
    label="20% ABS Threshold"
)

plt.xlabel("Time (s)")
plt.ylabel("Wheel Slip (%)")
plt.title("Wheel Slip During Wet-Road Braking")

plt.ylim(0, 105)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "images/abs_wheel_slip_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("ABS wheel-slip graph saved successfully!")

print(
    f"Maximum slip with ABS ON: {max(slip_on):.1f}%"
)
print(
    f"Maximum slip with ABS OFF: {max(slip_off):.1f}%"
)

def calculate_excessive_slip_duration(time, slip, threshold=20):
    duration = 0.0

    for i in range(1, len(time)):
        if slip[i - 1] > threshold:
            duration += time[i] - time[i - 1]

    return duration


duration_on = calculate_excessive_slip_duration(
    time_on, slip_on
)

duration_off = calculate_excessive_slip_duration(
    time_off, slip_off
)

print("\nExcessive wheel-slip analysis:")
print(f"ABS ON - Time above 20% slip: {duration_on:.3f} s")
print(f"ABS OFF - Time above 20% slip: {duration_off:.3f} s")

# Investigate maximum wheel-slip event
max_slip_index = slip_on.index(max(slip_on))

peak_time = time_on[max_slip_index]
peak_slip = slip_on[max_slip_index]

vehicle_speed_at_peak = (
    abs_on["history"]["vehicle_speed"][max_slip_index]
)

wheel_speed_at_peak = (
    abs_on["history"]["wheel_speed"][max_slip_index]
)

print("\nABS peak-slip investigation:")
print(f"Peak slip: {peak_slip:.2f}%")
print(f"Time of peak slip: {peak_time:.4f} s")
print(
    f"Vehicle speed at peak: "
    f"{vehicle_speed_at_peak * 3.6:.2f} km/h"
)
print(
    f"Wheel angular speed at peak: "
    f"{wheel_speed_at_peak:.2f} rad/s"
)

# Analyze ABS slip only above 5 km/h
minimum_speed_kmh = 5.0

valid_samples = [
    (time, slip, speed)
    for time, slip, speed in zip(
        time_on,
        slip_on,
        abs_on["history"]["vehicle_speed"]
    )
    if speed * 3.6 >= minimum_speed_kmh
]

valid_slips = [sample[1] for sample in valid_samples]

if valid_slips:
    max_valid_slip = max(valid_slips)

    print("\nABS slip analysis above 5 km/h:")
    print(f"Maximum slip: {max_valid_slip:.2f}%")

    duration_above_threshold = 0.0

    for i in range(1, len(valid_samples)):
        previous_time, previous_slip, _ = valid_samples[i - 1]
        current_time, _, _ = valid_samples[i]

        if previous_slip > 20:
            duration_above_threshold += (
                current_time - previous_time
            )

    print(
        f"Time above 20% slip: "
        f"{duration_above_threshold:.3f} s"
    )
else:
    print("No valid samples above 5 km/h.")
