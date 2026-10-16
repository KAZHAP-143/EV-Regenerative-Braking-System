
import math


# Illustrative road-specific parameters.
# These are engineering assumptions, not calibrated tire-test data.
ROAD_PARAMETERS = {
    "dry": {
        "peak_mu": 0.85,
        "c1": 1.28,
        "c2": 23.99,
        "c3": 0.52,
    },
    "wet": {
        "peak_mu": 0.45,
        "c1": 1.28,
        "c2": 30.0,
        "c3": 0.70,
    },
    "snow": {
        "peak_mu": 0.20,
        "c1": 1.28,
        "c2": 40.0,
        "c3": 1.10,
    },
}


def enhanced_tire_friction_coefficient(slip_ratio, road="dry"):
    """
    Calculate longitudinal tire friction using
    road-specific Burckhardt-style curves.
    """
    if road not in ROAD_PARAMETERS:
        raise ValueError("Road must be 'dry', 'wet', or 'snow'")

    if not math.isfinite(slip_ratio):
        raise ValueError("Slip ratio must be finite")

    p = ROAD_PARAMETERS[road]

    slip = max(0.0, min(1.0, slip_ratio))

    c1 = p["c1"]
    c2 = p["c2"]
    c3 = p["c3"]

    raw_mu = c1 * (1.0 - math.exp(-c2 * slip)) - c3 * slip

    peak_slip = math.log(c1 * c2 / c3) / c2
    raw_peak = (
        c1 * (1.0 - math.exp(-c2 * peak_slip))
        - c3 * peak_slip
    )

    return max(0.0, p["peak_mu"] * raw_mu / raw_peak)


def enhanced_tire_force(slip_ratio, normal_force, road="dry"):
    if not math.isfinite(normal_force) or normal_force < 0:
        raise ValueError("Normal force must be finite and nonnegative")

    return (
        enhanced_tire_friction_coefficient(slip_ratio, road)
        * normal_force
    )


if __name__ == "__main__":
    for road in ROAD_PARAMETERS:
        print(f"\n{road.upper()} ROAD")

        for slip in [0.0, 0.05, 0.10, 0.15, 0.20, 0.50, 1.0]:
            mu = enhanced_tire_friction_coefficient(slip, road)

            print(
                f"Slip: {slip * 100:5.1f}% | "
                f"Friction coefficient: {mu:.3f}"
            )
