from coordinated_braking_simulation import simulate_coordinated_braking

ROADS = ["dry", "wet", "snow"]
GAINS = [7.0, 15.0, 30.0, 60.0]

print("\nSTAGE 37 — ABS PERFORMANCE COMPARISON")
print("-" * 85)

for road in ROADS:
    print(f"\nROAD: {road.upper()}")

    for gain in GAINS:
        result = simulate_coordinated_braking(
            road=road,
            abs_enabled=True,
            abs_controller="road_adaptive",
            actuator_enabled=True,
            actuator_response_time=0.02,
            braking_mode="adaptive",
            tire_model="enhanced",
            abs_gain=gain,
        )

        history = result["history"]
        slips = history["slip"]

        avg_slip = sum(slips) / len(slips)
        max_slip = max(slips)

        print(
            f"Gain: {gain:5.1f} | "
            f"Distance: {result['stop_distance']:7.2f} m | "
            f"Time: {result['stop_time']:5.2f} s | "
            f"Avg Slip: {avg_slip * 100:6.2f}% | "
            f"Max Slip: {max_slip * 100:6.2f}% | "
            f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
        )