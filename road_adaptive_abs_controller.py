
import math

from proportional_abs_controller import proportional_abs_control


ROAD_SLIP_TARGETS = {
    "dry": 0.170,
    "wet": 0.133,
    "snow": 0.096,
}


def road_adaptive_abs_control(slip_ratio, road="dry", gain=7.0):
    """
    Calculate ABS braking factor using a road-specific
    target slip ratio.

    Returns a factor between 0.0 and 1.0.
    """
    if road not in ROAD_SLIP_TARGETS:
        raise ValueError("Road must be 'dry', 'wet', or 'snow'")

    if not math.isfinite(slip_ratio):
        raise ValueError("Slip ratio must be finite")

    if not math.isfinite(gain) or gain < 0:
        raise ValueError("Gain must be finite and nonnegative")

    target_slip = ROAD_SLIP_TARGETS[road]

    return proportional_abs_control(
        slip_ratio=slip_ratio,
        target_slip=target_slip,
        gain=gain,
    )


if __name__ == "__main__":
    for road in ROAD_SLIP_TARGETS:
        factor = road_adaptive_abs_control(
            slip_ratio=0.20,
            road=road,
        )

        print(
            f"{road.upper():5} | "
            f"Target slip: {ROAD_SLIP_TARGETS[road] * 100:.1f}% | "
            f"ABS factor at 20% slip: {factor:.3f}"
        )
