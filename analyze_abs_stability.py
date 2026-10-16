
from coordinated_braking_simulation import simulate_coordinated_braking

for controller in ["original", "proportional"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller=controller
    )

    slips = result["history"]["slip"]

    maximum_slip = max(slips)
    average_slip = sum(slips) / len(slips)

    high_slip_count = sum(
        1 for slip in slips if slip > 0.20
    )

    high_slip_percentage = (
        high_slip_count / len(slips) * 100
    )

    print(f"\nController: {controller.capitalize()}")
    print(f"Maximum slip: {maximum_slip * 100:.2f}%")
    print(f"Average slip: {average_slip * 100:.2f}%")
    print(
        f"Time above 20% slip: "
        f"{high_slip_percentage:.2f}%"
    )

    forces = result["history"]["total_brake_force"]

    force_changes = [
        abs(forces[i] - forces[i - 1])
        for i in range(1, len(forces))
    ]

    average_force_change = (
        sum(force_changes) / len(force_changes)
    )

    maximum_force_change = max(force_changes)

    print(
        f"Average brake-force change per step: "
        f"{average_force_change:.2f} N"
    )
    print(
        f"Maximum brake-force change per step: "
        f"{maximum_force_change:.2f} N"
    )
