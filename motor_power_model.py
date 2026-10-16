
def calculate_regen_power(
    regen_force,
    wheel_speed,
    wheel_radius=0.30,
    motor_efficiency=0.85
):
    """
    Calculate regenerative electrical power from wheel rotation.

    regen_force: Braking force at tire contact patch (N)
    wheel_speed: Wheel angular speed (rad/s)
    wheel_radius: Wheel radius (m)
    motor_efficiency: Mechanical-to-electrical efficiency
    """

    if regen_force < 0:
        raise ValueError("Regenerative force cannot be negative")

    if wheel_radius <= 0:
        raise ValueError("Wheel radius must be positive")

    if not 0 <= motor_efficiency <= 1:
        raise ValueError("Efficiency must be between 0 and 1")

    wheel_angular_speed = max(0.0, wheel_speed)

    regen_torque = regen_force * wheel_radius

    mechanical_power = regen_torque * wheel_angular_speed

    electrical_power = mechanical_power * motor_efficiency

    return electrical_power


if __name__ == "__main__":
    for wheel_speed in [90, 60, 30, 0]:
        power = calculate_regen_power(
            regen_force=1500,
            wheel_speed=wheel_speed
        )

        print(
            f"Wheel Speed: {wheel_speed:3} rad/s | "
            f"Regenerative Power: {power / 1000:.2f} kW"
        )
