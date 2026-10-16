
from enhanced_tire_model import (
    enhanced_tire_friction_coefficient,
)


print("STAGE 36 — OPTIMAL TIRE SLIP ANALYSIS")
print("-" * 60)

for road in ("dry", "wet", "snow"):
    best_slip = 0.0
    best_mu = -1.0

    for i in range(1001):
        slip = i / 1000.0

        mu = enhanced_tire_friction_coefficient(
            slip_ratio=slip,
            road=road,
        )

        if mu > best_mu:
            best_mu = mu
            best_slip = slip

    print(
        f"{road.upper():5} | "
        f"Optimal slip: {best_slip * 100:.1f}% | "
        f"Peak friction: {best_mu:.4f}"
    )
