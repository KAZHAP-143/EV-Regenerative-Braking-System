
from abs_controller import abs_brake_control

vehicle_speed = 20.0
requested_brake_force = 6000

wheel_speeds = [
    66.67,  # Approximately 0% slip
    60.00,  # 10% slip
    56.67,  # Approximately 15% slip
    50.00,  # 25% slip
    33.33,  # Approximately 50% slip
    0.00    # 100% slip (locked wheel)
]

print("ABS Controller Test Results")
print("-" * 75)

for wheel_speed in wheel_speeds:

    result = abs_brake_control(
        vehicle_speed=vehicle_speed,
        wheel_speed=wheel_speed,
        requested_brake_force=requested_brake_force
    )

    print(
        f"Slip: {result['slip_ratio'] * 100:6.1f}% | "
        f"Brake Force: {result['brake_force']:6.0f} N | "
        f"{result['status']}"
    )
