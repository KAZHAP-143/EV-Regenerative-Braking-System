
from coordinated_braking_simulation import simulate_coordinated_braking

print("STAGE 30 — REGENERATIVE BRAKING ENERGY ANALYSIS")
print("-" * 85)

for road in ["dry", "wet"]:
    for controller in ["original", "proportional"]:
        result = simulate_coordinated_braking(
            road=road,
            abs_enabled=True,
            abs_controller=controller,
            actuator_enabled=True,
            actuator_response_time=0.02
        )

        print(
            f"Road: {road:3} | "
            f"ABS: {controller:12} | "
            f"Recovered Energy: {result['recovered_energy_kwh']:.6f} kWh | "
            f"Stopping Distance: {result['stop_distance']:.2f} m"
        )

print("\nABS ENABLED VS DISABLED — WET ROAD")
print("-" * 85)

for enabled in [False, True]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=enabled,
        abs_controller="proportional",
        actuator_enabled=True,
        actuator_response_time=0.02
    )

    print(
        f"ABS Enabled: {str(enabled):5} | "
        f"Recovered Energy: {result['recovered_energy_kwh']:.6f} kWh | "
        f"Stopping Distance: {result['stop_distance']:.2f} m"
    )

print("\nREGENERATIVE BRAKING AVAILABILITY — WET ROAD")
print("-" * 85)

for controller in ["original", "proportional"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller=controller,
        actuator_enabled=True,
        actuator_response_time=0.02
    )

    regen_forces = result["history"]["regen_force"]

    active_steps = sum(force > 0 for force in regen_forces)
    total_steps = len(regen_forces)

    availability = active_steps / total_steps * 100

    print(
        f"ABS: {controller:12} | "
        f"Regen Active: {active_steps}/{total_steps} steps | "
        f"Availability: {availability:.2f}%"
    )

print("\nREGENERATIVE ENERGY UTILIZATION — WET ROAD")
print("-" * 85)

baseline = simulate_coordinated_braking(
    road="wet",
    abs_enabled=False,
    actuator_enabled=True,
    actuator_response_time=0.02
)

baseline_energy = baseline["recovered_energy_kwh"]

for controller in ["original", "proportional"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller=controller,
        actuator_enabled=True,
        actuator_response_time=0.02
    )

    recovered_energy = result["recovered_energy_kwh"]

    utilization = (
        recovered_energy / baseline_energy * 100
        if baseline_energy > 0
        else 0.0
    )

    print(
        f"ABS: {controller:12} | "
        f"Recovered: {recovered_energy:.6f} kWh | "
        f"Baseline: {baseline_energy:.6f} kWh | "
        f"Utilization: {utilization:.2f}%"
    )
