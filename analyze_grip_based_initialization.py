from coordinated_braking_simulation import simulate_coordinated_braking
from enhanced_tire_model import enhanced_tire_force
from road_adaptive_abs_controller import ROAD_SLIP_TARGETS

normal_force = 375.0 * 9.81
requested_force = 2500.0

print("\nSTAGE 37 — GRIP-BASED BRAKE INITIALIZATION")
print("-" * 90)

for road in ["dry", "wet", "snow"]:
    peak_force = enhanced_tire_force(
        ROAD_SLIP_TARGETS[road],
        normal_force,
        road,
    )

    grip_based_force = min(requested_force, 0.70 * peak_force)

    print(f"\nROAD: {road.upper()}")
    print(f"Grip-based initial force: {grip_based_force:.1f} N")

    for label, initial_force in [
        ("Baseline", requested_force),
        ("Grip-based", grip_based_force),
    ]:
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
            f"{label:10s} | "
            f"Distance: {result['stop_distance']:6.2f} m | "
            f"Max Slip: {max(slips) * 100:6.2f}% | "
            f"Energy: {result['recovered_energy_kwh']:.6f} kWh"
        )