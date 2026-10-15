
import math


def tire_friction_coefficient(slip_ratio, road="dry"):
    """
    Simplified slip-dependent tire friction model.

    slip_ratio: longitudinal braking slip (0 to 1)
    road: 'dry' or 'wet'

    Returns effective longitudinal friction coefficient.
    """

    if road == "dry":
        peak_mu = 0.85
    elif road == "wet":
        peak_mu = 0.45
    else:
        raise ValueError("Road must be 'dry' or 'wet'")

    slip = max(0.0, min(1.0, slip_ratio))

    # Simplified Burckhardt-style friction curve
    c1 = 1.28
    c2 = 23.99
    c3 = 0.52

    raw_mu = c1 * (1 - math.exp(-c2 * slip)) - c3 * slip

    # Normalize so peak friction equals road-specific peak_mu
    peak_slip = math.log(c1 * c2 / c3) / c2
    raw_peak = (
        c1 * (1 - math.exp(-c2 * peak_slip))
        - c3 * peak_slip
    )

    return peak_mu * raw_mu / raw_peak


def calculate_tire_force(
    slip_ratio,
    normal_force,
    road="dry"
):
    """
    Calculate longitudinal braking force from tire friction.

    normal_force: vertical load on tire (N)
    """

    if normal_force < 0:
        raise ValueError("Normal force cannot be negative")

    mu = tire_friction_coefficient(slip_ratio, road)

    return mu * normal_force


if __name__ == "__main__":
    for road in ["dry", "wet"]:
        print(f"\n{road.upper()} ROAD")

        for slip in [0.0, 0.05, 0.10, 0.15, 0.20, 0.50, 1.0]:
            mu = tire_friction_coefficient(slip, road)

            print(
                f"Slip: {slip * 100:5.1f}% | "
                f"Friction coefficient: {mu:.3f}"
            )
