from enhanced_tire_model import enhanced_tire_force
from road_adaptive_abs_controller import ROAD_SLIP_TARGETS


ROAD_GRIP_FACTORS = {
    "dry": 0.85,
    "wet": 0.85,
    "snow": 0.70,
}


def calculate_initial_brake_force(
    road,
    normal_force,
    requested_force,
):
    """
    Calculate an experimental road-dependent initial brake force.

    This uses the modeled tire force at the target slip ratio
    and a provisional road-specific grip factor.
    """

    if road not in ROAD_GRIP_FACTORS:
        raise ValueError(f"Unsupported road condition: {road}")

    if normal_force <= 0:
        raise ValueError("Normal force must be positive")

    if requested_force < 0:
        raise ValueError("Requested force cannot be negative")

    target_slip = ROAD_SLIP_TARGETS[road]

    peak_tire_force = enhanced_tire_force(
        target_slip,
        normal_force,
        road,
    )

    grip_factor = ROAD_GRIP_FACTORS[road]

    return min(
        requested_force,
        grip_factor * peak_tire_force,
    )