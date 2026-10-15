
import numpy as np
from battery_thermal import temperature_charge_factor
from motor_efficiency import calculate_motor_efficiency

# Vehicle parameters
mass = 1500.0
gravity = 9.81
drag_coefficient = 0.28
frontal_area = 2.2
air_density = 1.225
rolling_coefficient = 0.012

# Electric motor and battery parameters
motor_torque = 200.0
gear_ratio = 9.0
wheel_radius = 0.32
drivetrain_efficiency = 0.95
max_charge_power = 50_000.0
battery_capacity_j = 60 * 3_600_000


def simulate(mu, initial_speed_kmh=100, brake_force=4500,
             initial_soc=0.60, battery_temperature=25):
    # Initial conditions
    soc = initial_soc
    speed = initial_speed_kmh / 3.6
    distance = 0.0
    time = 0.0
    dt = 0.01
    recovered_energy = 0.0
    friction_energy = 0.0
    drag_energy = 0.0
    rolling_energy = 0.0
    motor_loss_energy = 0.0

    # Simulation history
    times = [0.0]
    speeds = [speed * 3.6]
    distances = [0.0]
    soc_history = [soc * 100]
    regen_history = [0.0]
    friction_history = [0.0]
    power_history = [0.0]

    while speed > 0:
        # Aerodynamic resistance
        drag = (
            0.5 * air_density
            * drag_coefficient
            * frontal_area
            * speed**2
        )

        # Rolling resistance
        rolling = rolling_coefficient * mass * gravity

        # Tyre-road traction limit
        traction_limit = mu * mass * gravity

        # Driver's braking demand
        braking_force = min(
            brake_force,
            traction_limit
        )

        # Motor torque limitation
        motor_force_limit = (
            motor_torque
            * gear_ratio
            * drivetrain_efficiency
            / wheel_radius
        )

        
        # Battery SOC protection
        if soc >= 0.95:
            soc_factor = 0.0
        elif soc > 0.90:
            soc_factor = (0.95 - soc) / 0.05
        else:
            soc_factor = 1.0

        # Battery temperature protection
        thermal_factor = temperature_charge_factor(
            battery_temperature
        )

        # Always calculate allowed charging power
        allowed_charge_power = (
            max_charge_power * soc_factor * thermal_factor
        )

        # Regenerative braking controller
        regen_efficiency = calculate_motor_efficiency(speed * 3.6)

        if speed > 1.4:
            power_force_limit = (
                allowed_charge_power
                / (regen_efficiency * speed)
            )

            regen_force = min(
                braking_force,
                motor_force_limit,
                power_force_limit
            )
        else:
            regen_force = 0.0

        # Friction braking supplies the remaining force

        
        friction_force = braking_force - regen_force

        # Vehicle longitudinal dynamics
        total_force = (
            regen_force
            + friction_force
            + drag
            + rolling
        )

        deceleration = total_force / mass

        # Stop exactly at zero speed
        step = min(dt, speed / deceleration)

        # Electrical energy delivered to battery
        battery_power = (
            regen_force * speed * regen_efficiency
        )
        energy_step = battery_power * step


        # Calculate energy for this simulation step
        distance_step = speed * step - 0.5 * deceleration * step**2

        regen_mechanical_energy = regen_force * distance_step
        battery_energy_step = regen_mechanical_energy * regen_efficiency

        # Track energy distribution
        recovered_energy += battery_energy_step
        friction_energy += friction_force * distance_step
        drag_energy += drag * distance_step
        rolling_energy += rolling * distance_step
        motor_loss_energy += regen_mechanical_energy - battery_energy_step

        # Update battery SOC
        soc = min(1.0, soc + battery_energy_step / battery_capacity_j)

        # Update vehicle position
        distance += (
            speed * step
            - 0.5 * deceleration * step**2
        )

        # Update speed and time
        speed = max(0.0, speed - deceleration * step)
        time += step

        # Record simulation results
        times.append(time)
        speeds.append(speed * 3.6)
        distances.append(distance)
        soc_history.append(soc * 100)
        regen_history.append(regen_force)
        friction_history.append(friction_force)
        power_history.append(battery_power / 1000)

    return {
    "time": np.array(times),
    "speed": np.array(speeds),
    "distance_history": np.array(distances),
    "distance": distance,
    "stop_time": time,
        "energy_kwh": recovered_energy / 3_600_000,
        "soc": np.array(soc_history),
        "regen_force": np.array(regen_history),
        "friction_force": np.array(friction_history),
        "battery_power_kw": np.array(power_history),

"friction_energy_kwh": friction_energy / 3_600_000,
"drag_energy_kwh": drag_energy / 3_600_000,
"rolling_energy_kwh": rolling_energy / 3_600_000,
"motor_loss_energy_kwh": motor_loss_energy / 3_600_000,

    }
