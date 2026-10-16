
def coordinate_adaptive_braking(
    requested_force,
    regen_limit,
    abs_factor=1.0
):
    """
    Distribute ABS-limited braking force between
    regenerative and friction braking.

    This is a simplified force-allocation model.
    """

    if requested_force < 0:
        raise ValueError("Requested force cannot be negative")

    if regen_limit < 0:
        raise ValueError("Regen limit cannot be negative")

    if not 0.0 <= abs_factor <= 1.0:
        raise ValueError("ABS factor must be between 0 and 1")

    # Total braking force permitted by ABS
    allowed_force = requested_force * abs_factor

    # Allocate permitted force to regeneration first
    regen_force = min(allowed_force, regen_limit)

    # Friction brakes provide the remaining force
    friction_force = allowed_force - regen_force

    return regen_force, friction_force
