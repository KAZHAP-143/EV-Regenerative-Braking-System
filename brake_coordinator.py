
def coordinate_braking(
    requested_force,
    regen_limit,
    abs_factor=1.0
):
    """
    Coordinate regenerative and friction braking.

    Forces are in newtons.
    abs_factor ranges from 0.0 to 1.0.
    """

    if requested_force < 0 or regen_limit < 0:
        raise ValueError("Braking forces cannot be negative")

    if not 0.0 <= abs_factor <= 1.0:
        raise ValueError("ABS factor must be between 0 and 1")

    allowed_force = requested_force * abs_factor

    # Simplified ABS intervention:
    # Disable regenerative braking when ABS reduces
    # the permitted total braking force.
    if abs_factor < 1.0:
        regen_force = 0.0
    else:
        regen_force = min(allowed_force, regen_limit)

    friction_force = allowed_force - regen_force

    return {
        "regen_force": regen_force,
        "friction_force": friction_force,
        "total_brake_force": regen_force + friction_force,
        "abs_factor": abs_factor
    }
