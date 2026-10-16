
from coordinated_braking_simulation import simulate_coordinated_braking

print("STAGE 31 — ADAPTIVE BRAKING COMPARISON")
print("-" * 75)

for mode in ["original", "adaptive"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller="proportional",
        actuator_enabled=True,
        actuator_response_time=0.02,
        braking_mode=mode
    )

    regen_forces = result["history"]["regen_force"]
    slips = result["history"]["slip"]

    regen_availability = (
        sum(force > 0 for force in regen_forces)
        / len(regen_forces) * 100
    )

    print(
        f"Mode: {mode:8} | "
        f"Distance: {result['stop_distance']:.2f} m | "
        f"Energy: {result['recovered_energy_kwh']:.6f} kWh | "
        f"Regen Active: {regen_availability:.2f}% | "
        f"Max Slip: {max(slips) * 100:.2f}%"
    )

print("\nENERGY CONSERVATION CHECK")
print("-" * 75)

vehicle_mass = 1500
initial_speed = 100 / 3.6

initial_kinetic_energy_kwh = (
    0.5 * vehicle_mass * initial_speed ** 2 / 3_600_000
)

print(f"Initial kinetic energy: {initial_kinetic_energy_kwh:.6f} kWh")

for mode in ["original", "adaptive"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller="proportional",
        actuator_enabled=True,
        actuator_response_time=0.02,
        braking_mode=mode
    )

    recovered = result["recovered_energy_kwh"]
    recovery_percentage = (
        recovered / initial_kinetic_energy_kwh * 100
    )

    print(
        f"Mode: {mode:8} | "
        f"Recovered: {recovered:.6f} kWh | "
        f"Recovery: {recovery_percentage:.2f}%"
    )
