
# EV Regenerative Braking System
# Stage 1: Vehicle kinetic energy calculation

vehicle_mass = 1500       # kg
initial_speed = 100       # km/h
motor_efficiency = 0.85   # Assumed energy recovery efficiency

# Convert km/h to m/s
speed_ms = initial_speed / 3.6

# Calculate kinetic energy
kinetic_energy = 0.5 * vehicle_mass * speed_ms**2

# Idealized recoverable energy
recovered_energy = kinetic_energy * motor_efficiency

# Convert Joules to kWh
recovered_kwh = recovered_energy / 3_600_000

print("EV Regenerative Braking Simulation")
print("--------------------------------")
print(f"Initial Speed: {initial_speed} km/h")
print(f"Vehicle Mass: {vehicle_mass} kg")
print(f"Kinetic Energy: {kinetic_energy:.2f} J")
print(f"Idealized Recovered Energy: {recovered_kwh:.4f} kWh")

import numpy as np
import matplotlib.pyplot as plt

# Stage 2: Vehicle braking simulation
deceleration = 3.0  # m/s²
time_to_stop = speed_ms / deceleration

time = np.linspace(0, time_to_stop, 200)
velocity = np.maximum(speed_ms - deceleration * time, 0)

# Kinetic energy at each time step
energy = 0.5 * vehicle_mass * velocity**2

# Idealized cumulative recovered energy
energy_recovered = (kinetic_energy - energy) * motor_efficiency
energy_recovered_kwh = energy_recovered / 3_600_000

print(f"Braking Time: {time_to_stop:.2f} seconds")
print(f"Braking Distance: {speed_ms**2 / (2 * deceleration):.2f} meters")

# Create graphs
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

axes[0].plot(time, velocity * 3.6)
axes[0].set_title("Vehicle Speed During Braking")
axes[0].set_xlabel("Time (seconds)")
axes[0].set_ylabel("Speed (km/h)")
axes[0].grid(True)

axes[1].plot(time, energy_recovered_kwh)
axes[1].set_title("Idealized Regenerative Energy Recovery")
axes[1].set_xlabel("Time (seconds)")
axes[1].set_ylabel("Recovered Energy (kWh)")
axes[1].grid(True)

plt.tight_layout()
plt.show()

# Stage 3: Regenerative braking controller

max_regen_force = 2500  # N
max_battery_power = 50000  # W
battery_soc = 0.60  # 60% state of charge

# Total requested braking force
total_braking_force = vehicle_mass * deceleration

regen_force = np.zeros_like(velocity)
friction_force = np.zeros_like(velocity)
regen_power = np.zeros_like(velocity)

for i, v in enumerate(velocity):

    # Disable regeneration at very low speeds
    if v < 1.4 or battery_soc >= 0.95:
        available_regen = 0

    else:
        # Battery charging power limit
        power_limited_force = (
            max_battery_power / (motor_efficiency * v)
        )

        available_regen = min(
            max_regen_force,
            power_limited_force
        )

    regen_force[i] = min(
        total_braking_force,
        available_regen
    )

    friction_force[i] = (
        total_braking_force - regen_force[i]
    )

    # Electrical power delivered to battery
    regen_power[i] = (
        regen_force[i] * v * motor_efficiency
    )

# Integrate recovered energy over time
recovered_energy_j = np.trapezoid(regen_power, time)
recovered_energy_kwh = recovered_energy_j / 3_600_000

print("\nRegenerative Braking Controller")
print("--------------------------------")
print(f"Total Braking Force: {total_braking_force:.0f} N")
print(f"Maximum Regen Force: {max_regen_force:.0f} N")
print(f"Recovered Energy: {recovered_energy_kwh:.4f} kWh")

# Plot braking force distribution
plt.figure(figsize=(10, 5))

plt.plot(time, regen_force, label="Regenerative Braking")
plt.plot(time, friction_force, label="Friction Braking")

plt.title("Regenerative vs Friction Braking Force")
plt.xlabel("Time (seconds)")
plt.ylabel("Braking Force (N)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Stage 4: Battery energy and SOC simulation

battery_capacity_kwh = 60.0
initial_soc = 0.60  # 60%

# Convert battery capacity to joules
battery_capacity_j = battery_capacity_kwh * 3_600_000

# Calculate cumulative energy recovered at each time step
cumulative_energy_j = np.zeros_like(time)

for i in range(1, len(time)):
    dt = time[i] - time[i - 1]

    # Trapezoidal integration of battery charging power
    cumulative_energy_j[i] = (
        cumulative_energy_j[i - 1]
        + 0.5 * (regen_power[i - 1] + regen_power[i]) * dt
    )

# Calculate battery state of charge
soc = initial_soc + cumulative_energy_j / battery_capacity_j
soc_percent = soc * 100

print("\nBattery Management System")
print("--------------------------------")
print(f"Battery Capacity: {battery_capacity_kwh:.1f} kWh")
print(f"Initial SOC: {initial_soc * 100:.4f}%")
print(f"Final SOC: {soc_percent[-1]:.4f}%")
print(f"Energy Recovered: {cumulative_energy_j[-1] / 3_600_000:.4f} kWh")

# Battery SOC graph
plt.figure(figsize=(10, 5))

plt.plot(time, soc_percent, label="Battery SOC")

plt.title("Battery State of Charge During Regenerative Braking")
plt.xlabel("Time (seconds)")
plt.ylabel("Battery SOC (%)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
