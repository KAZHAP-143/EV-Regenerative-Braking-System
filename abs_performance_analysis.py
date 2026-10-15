
import matplotlib.pyplot as plt
from abs_controller import abs_brake_control

vehicle_speed = 20.0
requested_brake_force = 6000
wheel_radius = 0.30

slip_percentages = list(range(0, 101))
braking_forces = []

for slip_percent in slip_percentages:
    slip = slip_percent / 100

    # Convert target slip into wheel angular speed
    wheel_speed = (
        vehicle_speed * (1 - slip)
    ) / wheel_radius

    result = abs_brake_control(
        vehicle_speed=vehicle_speed,
        wheel_speed=wheel_speed,
        requested_brake_force=requested_brake_force
    )

    braking_forces.append(result["brake_force"])

plt.figure(figsize=(10, 6))

plt.plot(
    slip_percentages,
    braking_forces,
    linewidth=2,
    label="ABS Applied Braking Force"
)

plt.axvline(
    x=10,
    linestyle="--",
    label="10% Slip Threshold"
)

plt.axvline(
    x=20,
    linestyle="--",
    label="20% Slip Threshold"
)

plt.xlabel("Wheel Slip (%)")
plt.ylabel("Applied Braking Force (N)")
plt.title("ABS Controller Response to Wheel Slip")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    "images/abs_controller_response.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("ABS response graph saved successfully!")
