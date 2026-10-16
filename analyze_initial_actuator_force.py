from coordinated_braking_simulation import simulate_coordinated_braking

print("\nSTAGE 37 — INITIAL FORCE CROSS-ROAD COMPARISON")
print("-" * 90)

for road in ["dry", "wet", "snow"]:
    print(f"\nROAD: {road.upper()}")

    for initial_force in [500, 2500]:
        result = simulate_coordinated_braking(
            road=road,
            initial_speed_kmh=30,
            abs_enabled=True,
            abs_controller="road_adaptive",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            abs_gain=60.0,
            initial_actuator_force=initial_force,
        )

        slips = result["history"]["slip"]

        print(
            f"Initial Force: {initial_force:4d} N | "
            f"Distance: {result['stop_distance']:6.2f} m | "
            f"Time: {result['stop_time']:5.2f} s | "
            f"Avg Slip: {sum(slips) / len(slips) * 100:6.2f}% | "
            f"Max Slip: {max(slips) * 100:6.2f}% | "
            f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
        )