
from wheel_dynamics import calculate_slip_ratio


def abs_brake_control(
    vehicle_speed,
    wheel_speed,
    requested_brake_force,
    wheel_radius=0.30
):
    """
    Simplified ABS braking force controller.

    Reduces braking force when wheel slip is excessive.
    """

    slip = calculate_slip_ratio(
        vehicle_speed,
        wheel_speed,
        wheel_radius
    )

    if slip > 0.20:
        # High slip: reduce braking force
        brake_factor = 0.50
        status = "ABS ACTIVE - Brake pressure reduced"

    elif slip < 0.10:
        # Low slip: full requested braking force
        brake_factor = 1.00
        status = "ABS INACTIVE - Normal braking"

    else:
        # Intermediate slip: moderate braking
        brake_factor = 0.85
        status = "ABS MODULATING"

    actual_brake_force = requested_brake_force * brake_factor

    return {
        "slip_ratio": slip,
        "brake_force": actual_brake_force,
        "status": status
    }


if __name__ == "__main__":

    result = abs_brake_control(
        vehicle_speed=20.0,
        wheel_speed=50.0,
        requested_brake_force=6000
    )

    print(f"Wheel Slip: {result['slip_ratio'] * 100:.1f}%")
    print(f"Applied Brake Force: {result['brake_force']:.0f} N")
    print(f"ABS Status: {result['status']}")
