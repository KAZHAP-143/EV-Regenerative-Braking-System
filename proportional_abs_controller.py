
def proportional_abs_control(
    slip_ratio,
    target_slip=0.15,
    gain=7.0
):
    """
    Simplified proportional ABS controller.

    Returns a braking-force multiplier between 0 and 1.
    """

    if not 0.0 <= slip_ratio <= 1.0:
        raise ValueError("Slip ratio must be between 0 and 1")

    if not 0.0 < target_slip < 1.0:
        raise ValueError("Target slip must be between 0 and 1")

    if gain < 0:
        raise ValueError("Gain cannot be negative")

    slip_error = slip_ratio - target_slip

    if slip_error <= 0:
        return 1.0

    abs_factor = 1.0 - gain * slip_error

    return max(0.0, min(1.0, abs_factor))


if __name__ == "__main__":
    for slip in [0.0, 0.10, 0.15, 0.20, 0.30, 0.50]:
        factor = proportional_abs_control(slip)

        print(
            f"Slip: {slip * 100:5.1f}% | "
            f"Brake Force Allowed: {factor * 100:5.1f}%"
        )
