from coordinated_braking_simulation import simulate_coordinated_braking

print("\nSTAGE 37 — GAIN ROBUSTNESS AT 50 MS ACTUATOR DELAY")
print("-" * 85)

for gain in [7.0, 15.0, 30.0, 60.0]:
    result = simulate_coordinated_braking(
        road="snow",
        initial_speed_kmh=30,
        abs_enabled=True,
        abs_controller="road_adaptive",
        actuator_enabled=True,
        actuator_response_time=0.05,
        braking_mode="adaptive",
        tire_model="enhanced",
        abs_gain=gain,
    )

    slips = result["history"]["slip"]

    print(
        f"Gain: {gain:5.1f} | "
        f"Distance: {result['stop_distance']:6.2f} m | "
        f"Time: {result['stop_time']:5.2f} s | "
        f"Avg Slip: {sum(slips) / len(slips) * 100:6.2f}% | "
        f"Max Slip: {max(slips) * 100:6.2f}% | "
        f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
    )