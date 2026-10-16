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
)

history = result["history"]

max_index = max(
    range(len(history["slip"])),
    key=lambda i: history["slip"][i]
)

print("\nSTAGE 37 — MAXIMUM SLIP EVENT")
print("-" * 50)

print(f"Time: {history['time'][max_index]:.4f} s")
print(f"Vehicle speed: {history['vehicle_speed'][max_index] * 3.6:.2f} km/h")
print(f"Wheel speed: {history['wheel_speed'][max_index]:.2f} rad/s")
print(f"Slip: {history['slip'][max_index] * 100:.2f}%")
print(f"Brake force: {history['total_brake_force'][max_index]:.2f} N")
print(f"Tire force: {history['tire_force'][max_index]:.2f} N")
print("\nINITIAL BRAKING TRANSIENT")
print("-" * 80)

for target_time in [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20]:
    index = min(
        range(len(history["time"])),
        key=lambda i: abs(history["time"][i] - target_time)
    )

    print(
        f"Time: {history['time'][index]:.3f} s | "
        f"Slip: {history['slip'][index] * 100:6.2f}% | "
        f"Brake: {history['total_brake_force'][index]:7.1f} N | "
        f"Tire: {history['tire_force'][index]:7.1f} N"
    )