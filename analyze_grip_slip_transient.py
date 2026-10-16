from coordinated_braking_simulation import simulate_coordinated_braking

result = simulate_coordinated_braking(
    road="snow",
    initial_speed_kmh=30,
    abs_enabled=True,
    abs_controller="road_adaptive",
    actuator_enabled=True,
    actuator_response_time=0.05,
    braking_mode="adaptive",
    tire_model="enhanced",
    abs_gain=60.0,
    initialization_mode="grip_based",
)

history = result["history"]
slips = history["slip"]

peak_index = max(range(len(slips)), key=lambda i: slips[i])

print("\nSTAGE 38 — SNOW SLIP TRANSIENT")
print("-" * 70)

print(f"Maximum slip: {slips[peak_index] * 100:.2f}%")
print(f"Time of maximum slip: {history['time'][peak_index]:.4f} s")
print(f"Brake force at peak: {history['total_brake_force'][peak_index]:.1f} N")

print("\nTIME SERIES")
print("-" * 70)

for target_time in [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20]:
    index = min(
        range(len(history["time"])),
        key=lambda i: abs(history["time"][i] - target_time),
    )

    print(
        f"Time: {history['time'][index]:.3f} s | "
        f"Slip: {slips[index] * 100:6.2f}% | "
        f"Brake: {history['total_brake_force'][index]:7.1f} N | "
        f"Tire: {history['tire_force'][index]:7.1f} N"
    )