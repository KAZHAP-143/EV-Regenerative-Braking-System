from coordinated_braking_simulation import simulate_coordinated_braking
from enhanced_tire_model import enhanced_tire_force
from road_adaptive_abs_controller import ROAD_SLIP_TARGETS

normal_force = 375.0 * 9.81

print("\nSTAGE 37 — GRIP FACTOR ANALYSIS")
print("-" * 90)

for road in ["dry", "wet", "snow"]:
    peak_force = enhanced_tire_force(
        ROAD_SLIP_TARGETS[road],
        normal_force,
        road,
    )

    print(f"\nROAD: {road.upper()}")

    for factor in [0.40, 0.55, 0.70, 0.85, 1.00]:
        initial_force = min(2500.0, factor * peak_force)

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
            f"Factor: {factor:.2f} | "
            f"Force: {initial_force:7.1f} N | "
            f"Distance: {result['stop_distance']:6.2f} m | "
            f"Max Slip: {max(slips) * 100:6.2f}% | "
            f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
        )
    