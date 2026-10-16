
from adaptive_brake_coordinator import coordinate_adaptive_braking

print("STAGE 31 — ADAPTIVE BRAKE COORDINATOR TEST")
print("-" * 65)

test_cases = [
    (2500, 1500, 1.0),
    (2500, 1500, 0.8),
    (2500, 1500, 0.6),
    (2500, 1500, 0.4),
    (2500, 1500, 0.0),
]

for requested, regen_limit, abs_factor in test_cases:
    regen, friction = coordinate_adaptive_braking(
        requested_force=requested,
        regen_limit=regen_limit,
        abs_factor=abs_factor
    )

    total = regen + friction
    expected = requested * abs_factor

    assert abs(total - expected) < 1e-9

    print(
        f"ABS Factor: {abs_factor:.1f} | "
        f"Regen: {regen:7.1f} N | "
        f"Friction: {friction:7.1f} N | "
        f"Total: {total:7.1f} N"
    )

print("\nAll adaptive braking tests passed!")
