
from abs_controller import abs_brake_control
from brake_coordinator import coordinate_braking

vehicle_speed = 20.0
requested_force = 2500.0
regen_limit = 1500.0

print("ABS + Regenerative Braking Integration Test")
print("-" * 45)

for wheel_speed in [66.67, 60.0, 50.0, 30.0, 0.0]:

    abs_result = abs_brake_control(
        vehicle_speed=vehicle_speed,
        wheel_speed=wheel_speed,
        requested_brake_force=requested_force
    )

    abs_factor = abs_result["brake_force"] / requested_force

    braking = coordinate_braking(
        requested_force=requested_force,
        regen_limit=regen_limit,
        abs_factor=abs_factor
    )

    print(
        f"Wheel speed: {wheel_speed:6.2f} rad/s | "
        f"Slip: {abs_result['slip_ratio'] * 100:5.1f}% | "
        f"Regen: {braking['regen_force']:6.0f} N | "
        f"Friction: {braking['friction_force']:6.0f} N | "
        f"Total: {braking['total_brake_force']:6.0f} N"
    )
