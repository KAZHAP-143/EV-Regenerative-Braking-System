from coordinated_braking_simulation import simulate_coordinated_braking

SPEEDS = [30, 60, 100, 120]
ROADS = ["dry", "wet", "snow"]
GAINS = [7.0, 60.0]

print("\nSTAGE 37 — ABS SPEED PERFORMANCE")
print("-" * 90)

for road in ROADS:
    print(f"\nROAD: {road.upper()}")

    for speed in SPEEDS:
        for gain in GAINS:
            result = simulate_coordinated_braking(
                road=road,
                initial_speed_kmh=speed,
                abs_enabled=True,
                abs_controller="road_adaptive",
                actuator_enabled=True,
                actuator_response_time=0.02,
                braking_mode="adaptive",
                tire_model="enhanced",
                abs_gain=gain,
            )

            slips = result["history"]["slip"]

            print(
                f"Speed: {speed:3d} km/h | "
                f"Gain: {gain:4.0f} | "
                f"Distance: {result['stop_distance']:7.2f} m | "
                f"Time: {result['stop_time']:6.2f} s | "
                f"Avg Slip: {sum(slips) / len(slips) * 100:6.2f}% | "
                f"Max Slip: {max(slips) * 100:6.2f}% | "
                f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
            )