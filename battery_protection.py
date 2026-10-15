
import numpy as np
import matplotlib.pyplot as plt

# Vehicle parameters
mass = 1500.0
speed = 100 / 3.6
requested_deceleration = 3.0
efficiency = 0.85
# Electric motor and drivetrain
motor_max_torque = 200.0  # Nm
gear_ratio = 9.0
wheel_radius = 0.32  # meters
drivetrain_efficiency = 0.95

# Maximum regenerative braking force at wheels
max_regen_force = (
    motor_max_torque
    * gear_ratio
    * drivetrain_efficiency
    / wheel_radius
)

# Battery parameters
capacity_j = 60 * 3_600_000
soc = 0.60
temperature = 25.0
max_charge_power = 50_000.0

# Simulation parameters
dt = 0.01
time = 0.0
distance = 0.0
energy_recovered = 0.0

# Data storage
times = []
speeds = []
soc_values = []
regen_forces = []
friction_forces = []
battery_powers = []

while speed > 0:

    # Battery protection factors
    if soc >= 0.95:
        soc_factor = 0.0
    elif soc > 0.90:
        soc_factor = (0.95 - soc) / 0.05
    else:
        soc_factor = 1.0

    if temperature < 0 or temperature > 50:
        temp_factor = 0.0
    elif temperature < 10:
        temp_factor = temperature / 10
    elif temperature > 40:
        temp_factor = (50 - temperature) / 10
    else:
        temp_factor = 1.0

    # Charging power permitted by battery
    allowed_power = (
        max_charge_power * soc_factor * temp_factor
    )

    # Requested total braking force
    total_force = mass * requested_deceleration

    # Regenerative braking availability
    if speed < 1.4:
        regen_force = 0.0
    else:
        power_force_limit = (
            allowed_power / (efficiency * speed)
        )

        regen_force = min(
            total_force,
            max_regen_force,
            power_force_limit
        )

    # Friction brakes supply remaining force
    friction_force = total_force - regen_force

    # Battery charging power
    battery_power = regen_force * speed * efficiency

    # Update vehicle and battery
    step = min(dt, speed / requested_deceleration)

    energy_step = battery_power * step
    energy_recovered += energy_step
    soc = min(1.0, soc + energy_step / capacity_j)

    distance += speed * step - (
        0.5 * requested_deceleration * step**2
    )

    speed = max(
        0.0,
        speed - requested_deceleration * step
    )

    time += step

    # Record results
    times.append(time)
    speeds.append(speed * 3.6)
    soc_values.append(soc * 100)
    regen_forces.append(regen_force)
    friction_forces.append(friction_force)
    battery_powers.append(battery_power / 1000)

# Results
print("Battery Protection Simulation")
print("-----------------------------")
print(f"Stopping time: {time:.2f} s")
print(f"Stopping distance: {distance:.2f} m")
print(f"Final SOC: {soc * 100:.4f}%")
print(
    f"Recovered energy: "
    f"{energy_recovered / 3_600_000:.4f} kWh"
)

# Visualization
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

axes[0].plot(times, speeds)
axes[0].set_title("Vehicle Speed")
axes[0].set_ylabel("km/h")

axes[1].plot(times, regen_forces, label="Regenerative")
axes[1].plot(times, friction_forces, label="Friction")
axes[1].set_title("Braking Force Distribution")
axes[1].set_ylabel("Force (N)")
axes[1].legend()

axes[2].plot(times, soc_values, label="Battery SOC")
axes[2].set_title("Battery State of Charge")
axes[2].set_xlabel("Time (s)")
axes[2].set_ylabel("SOC (%)")

for ax in axes:
    ax.grid(True)

plt.tight_layout()
plt.show()

# Stage 6: Electric motor torque calculation

motor_max_torque = 200.0  # Nm
gear_ratio = 9.0
wheel_radius = 0.32  # meters
drivetrain_efficiency = 0.95

# Maximum braking force from motor torque
motor_braking_force = (
    motor_max_torque
    * gear_ratio
    * drivetrain_efficiency
    / wheel_radius
)

# Motor rotational speed at 100 km/h
vehicle_speed_ms = 100 / 3.6

wheel_angular_speed = vehicle_speed_ms / wheel_radius
motor_angular_speed = wheel_angular_speed * gear_ratio

motor_rpm = motor_angular_speed * 60 / (2 * np.pi)

print("\nElectric Motor Model")
print("--------------------------")
print(f"Maximum Motor Braking Force: {motor_braking_force:.2f} N")
print(f"Motor Speed at 100 km/h: {motor_rpm:.0f} RPM")
