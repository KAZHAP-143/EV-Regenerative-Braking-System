from coordinated_braking_simulation import simulate_coordinated_braking

print("\nSTAGE 37 — INTEGRATED GRIP-BASED BRAKING")
print("-" * 85)

for road in ["dry", "wet", "snow"]:
    print(f"\nROAD: {road.upper()}")

    for mode in ["original", "grip_based"]:
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
            initialization_mode=mode,
        )

        slips = result["history"]["slip"]

        print(
            f"Mode: {mode:10s} | "
            f"Distance: {result['stop_distance']:6.2f} m | "
            f"Max Slip: {max(slips) * 100:6.2f}% | "
            f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
        )