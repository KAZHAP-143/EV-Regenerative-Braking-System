from enhanced_tire_model import enhanced_tire_force
from road_adaptive_abs_controller import ROAD_SLIP_TARGETS

quarter_mass = 1500.0 / 4
normal_force = quarter_mass * 9.81

print("\nSTAGE 37 — AVAILABLE TIRE GRIP")
print("-" * 65)

for road, target_slip in ROAD_SLIP_TARGETS.items():
    max_tire_force = enhanced_tire_force(
        slip_ratio=target_slip,
        normal_force=normal_force,
        road=road,
    )

    print(
        f"Road: {road.upper():4s} | "
        f"Target slip: {target_slip * 100:5.1f}% | "
        f"Peak tire force: {max_tire_force:7.1f} N"
    )