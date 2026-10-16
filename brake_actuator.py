
def update_brake_pressure(
    current_force,
    target_force,
    dt,
    response_time=0.05
):
    """
    Simplified first-order brake actuator model.

    response_time: actuator time constant in seconds.
    """

    if current_force < 0 or target_force < 0:
        raise ValueError("Brake forces cannot be negative")

    if dt <= 0:
        raise ValueError("Time step must be positive")

    if response_time <= 0:
        raise ValueError("Response time must be positive")

    alpha = min(dt / response_time, 1.0)

    new_force = current_force + alpha * (
        target_force - current_force
    )

    return max(0.0, new_force)


if __name__ == "__main__":
    current_force = 2500.0
    target_force = 1000.0

    for step in range(10):
        current_force = update_brake_pressure(
            current_force,
            target_force,
            dt=0.01
        )

        print(
            f"Step {step + 1}: "
            f"Brake Force = {current_force:.2f} N"
        )
