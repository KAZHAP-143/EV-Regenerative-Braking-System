
def calculate_max_regen_force(
    max_battery_power,
    wheel_speed,
    wheel_radius=0.30,
    motor_efficiency=0.85,
    charging_efficiency=0.95
):
    """
    Calculate maximum regenerative braking force permitted
    by battery charging power.

    Returns force in newtons.
    """

    if max_battery_power < 0:
        raise ValueError("Battery power limit cannot be negative")

    if wheel_radius <= 0:
        raise ValueError("Wheel radius must be positive")

    if not 0 < motor_efficiency <= 1:
        raise ValueError("Motor efficiency must be between 0 and 1")

    if not 0 < charging_efficiency <= 1:
        raise ValueError("Charging efficiency must be between 0 and 1")

    if wheel_speed <= 0:
        return 0.0

    maximum_force = max_battery_power / (
        wheel_speed
        * wheel_radius
        * motor_efficiency
        * charging_efficiency
    )

    return maximum_force


if __name__ == "__main__":
    for speed in [100, 60, 30, 0]:
        force = calculate_max_regen_force(
            max_battery_power=50000,
            wheel_speed=speed
        )

        print(
            f"Wheel Speed: {speed:3} rad/s | "
            f"Maximum Regen Force: {force:.2f} N"
        )

