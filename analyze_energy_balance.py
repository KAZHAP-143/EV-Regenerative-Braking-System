
from coordinated_braking_simulation import simulate_coordinated_braking

VEHICLE_MASS = 1500.0
INITIAL_SPEED = 100.0 / 3.6

initial_kinetic_energy = (
    0.5 * VEHICLE_MASS * INITIAL_SPEED ** 2
)

print("STAGE 32 — VEHICLE ENERGY BALANCE")
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

    history = result["history"]

    # Rotational kinetic energy of all four wheels
    wheel_inertia = 1.8
    wheel_count = 4

    initial_wheel_speed = history["wheel_speed"][0]
    final_wheel_speed = history["wheel_speed"][-1]

    initial_rotational_energy = (
        0.5 * wheel_count * wheel_inertia
        * initial_wheel_speed ** 2
    )

    final_rotational_energy = (
        0.5 * wheel_count * wheel_inertia
        * final_wheel_speed ** 2
    )

    rotational_energy_lost = (
        initial_rotational_energy - final_rotational_energy
    )

    print(
        f"{mode.capitalize()} wheel rotational energy lost: "
        f"{rotational_energy_lost / 3_600_000:.6f} kWh"
    )


    wheel_radius = 0.30
    dt = 0.0001
    wheel_count = 4

    tire_slip_energy = 0.0

    for tire_force, vehicle_speed, slip in zip(
        history["tire_force"],
        history["vehicle_speed"],
        history["slip"]
    ):
        # Slip ratio = (vehicle speed - wheel surface speed)
        #              / vehicle speed
        wheel_surface_speed = vehicle_speed * (1.0 - slip)

        relative_slip_speed = max(
            0.0,
            vehicle_speed - wheel_surface_speed
        )

        tire_slip_energy += (
            tire_force * relative_slip_speed * dt * wheel_count
        )

    print(
        f"{mode.capitalize()} tire-slip dissipation: "
        f"{tire_slip_energy / 3_600_000:.6f} kWh"
    )

    # Calculate friction-brake energy dissipation
    friction_brake_energy = 0.0

    for friction_force, vehicle_speed, slip in zip(
        history["friction_force"],
        history["vehicle_speed"],
        history["slip"]
    ):
        wheel_surface_speed = max(
            0.0,
            vehicle_speed * (1.0 - slip)
        )

        friction_brake_energy += (
            friction_force
            * wheel_surface_speed
            * dt
            * wheel_count
        )

    print(
        f"{mode.capitalize()} friction-brake dissipation: "
        f"{friction_brake_energy / 3_600_000:.6f} kWh"
    )


    # Mechanical energy absorbed by regenerative braking
    regen_mechanical_energy = 0.0

    for regen_force, vehicle_speed, slip in zip(
        history["regen_force"],
        history["vehicle_speed"],
        history["slip"]
    ):
        wheel_surface_speed = max(
            0.0,
            vehicle_speed * (1.0 - slip)
        )

        regen_mechanical_energy += (
            regen_force
            * wheel_surface_speed
            * dt
            * wheel_count
        )

    print(
        f"{mode.capitalize()} regen mechanical energy: "
        f"{regen_mechanical_energy / 3_600_000:.6f} kWh"
    )


    final_speed = history["vehicle_speed"][-1]

    final_kinetic_energy = (
        0.5 * VEHICLE_MASS * final_speed ** 2
    )

    kinetic_energy_lost = (
        initial_kinetic_energy - final_kinetic_energy
    )

    recovered_energy = (
        result["recovered_energy_kwh"] * 3_600_000
    )

    recovery_fraction = (
        recovered_energy / kinetic_energy_lost * 100
    )

    remaining_energy = (
        kinetic_energy_lost - recovered_energy
    )

    # Compare vehicle kinetic energy loss with modeled energy sinks
    total_mechanical_energy = (
        tire_slip_energy
        + friction_brake_energy
        + regen_mechanical_energy
    )

    total_kinetic_energy_lost = (
    kinetic_energy_lost + rotational_energy_lost
    )

    energy_residual = (
        total_kinetic_energy_lost - total_mechanical_energy
    )

    print(
        f"{mode.capitalize()} mechanical energy total: "
        f"{total_mechanical_energy / 3_600_000:.6f} kWh"
    )

    print(
        f"{mode.capitalize()} energy balance residual: "
        f"{energy_residual / 3_600_000:.6f} kWh"
    )


    print(
        f"Mode: {mode:8} | "
        f"KE Lost: {kinetic_energy_lost / 3600000:.6f} kWh | "
        f"Recovered: {recovered_energy / 3600000:.6f} kWh | "
        f"Recovery: {recovery_fraction:.2f}% | "
        f"Remaining: {remaining_energy / 3600000:.6f} kWh"
    )
