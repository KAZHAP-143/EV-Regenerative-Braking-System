
from wheel_dynamics import calculate_slip_ratio, update_wheel_speed
from abs_controller import abs_brake_control
from brake_coordinator import coordinate_braking
from tire_model import calculate_tire_force
from battery_soc_control import calculate_regen_soc_factor
from battery_temperature_control import calculate_regen_temperature_factor
from motor_power_model import calculate_regen_power
from battery_power_limit import calculate_max_regen_force

def simulate_coordinated_braking(
    road="wet",
    abs_enabled=True,
    initial_soc=0.60,
    battery_temperature=25.0
):
    """
    Simplified quarter-car model with coordinated
    regenerative braking, friction braking, and ABS.
    """

    quarter_mass = 1500.0 / 4
    # Simplified assumption: four identical regenerative wheels
    regenerative_wheel_count = 4
    wheel_radius = 0.30
    wheel_inertia = 1.8
    normal_force = quarter_mass * 9.81

    dt = 0.0001
    vehicle_speed = 100.0 / 3.6
    wheel_speed = vehicle_speed / wheel_radius

    requested_force = 2500.0
    regen_limit = 1500.0

    time = 0.0
    distance = 0.0
    recovered_energy_joules = 0.0
    motor_efficiency = 0.85
    battery_charging_efficiency = 0.95
    max_battery_charging_power = 50_000.0  # Watts
    battery_capacity_kwh = 60.0

    if not 0.0 <= initial_soc <= 1.0:
        raise ValueError("Initial SOC must be between 0 and 1")

    battery_soc = initial_soc
    history = {
        "time": [],
        "vehicle_speed": [],
        "slip": [],
        "regen_force": [],
        "friction_force": [],
        "total_brake_force": [],
        "tire_force": []
    }

    while vehicle_speed > 0.01 and time < 60.0:

        slip = calculate_slip_ratio(
            vehicle_speed, wheel_speed, wheel_radius
        )

        if abs_enabled:
            abs_result = abs_brake_control(
                vehicle_speed, wheel_speed,
                requested_force, wheel_radius
            )
            abs_factor = (
                abs_result["brake_force"] / requested_force
            )
        else:
            abs_factor = 1.0

        
        # Reduce regenerative braking availability at high SOC
        
        # Battery SOC and temperature constraints
        soc_factor = calculate_regen_soc_factor(battery_soc)

        temperature_factor = calculate_regen_temperature_factor(
            battery_temperature
        )

        # Combined regenerative braking availability
        available_regen_force = (
            regen_limit * soc_factor * temperature_factor
        )
                # Battery charging power constraint
        # 50 kW is the full-vehicle charging limit.
        # Allocate one quarter of it to this wheel.
        wheel_charging_power_limit = max_battery_charging_power / 4.0

        power_limited_regen_force = calculate_max_regen_force(
            max_battery_power=wheel_charging_power_limit,
            wheel_speed=wheel_speed,
            wheel_radius=wheel_radius,
            motor_efficiency=motor_efficiency,
            charging_efficiency=battery_charging_efficiency
        )

        available_regen_force = min(
            available_regen_force,
            power_limited_regen_force
        )


        # Coordinate regenerative and friction braking
        braking = coordinate_braking(
            requested_force=requested_force,
            regen_limit=available_regen_force,
            abs_factor=abs_factor
        )


        
        total_brake_force = braking["total_brake_force"]

                # Calculate regenerative power from wheel rotation
        regen_electrical_power = calculate_regen_power(
            regen_force=braking["regen_force"],
            wheel_speed=wheel_speed,
            wheel_radius=wheel_radius,
            motor_efficiency=motor_efficiency
        )

        # Apply battery charging efficiency
        battery_power = (
            regen_electrical_power * battery_charging_efficiency
        )

        # Limit power stored in the battery to 50 kW
        regen_power = min(
            battery_power,
            wheel_charging_power_limit
        )
        # Total charging power from all regenerative wheels
        total_regen_power = regen_power * regenerative_wheel_count
        # Accumulate recovered energy
        recovered_energy_joules += total_regen_power * dt
        # Update battery state of charge
        energy_added_kwh = total_regen_power * dt / 3600000

        battery_soc += energy_added_kwh / battery_capacity_kwh

        battery_soc = min(battery_soc, 1.0)
        regen_power = min(
            battery_power,
            wheel_charging_power_limit
        )
        # Check that regenerative power is nonnegative
        assert regen_power >= 0.0

        # Calculate tire-road braking force
        tire_force = calculate_tire_force(
            slip, normal_force, road
        )


        

        acceleration = -tire_force / quarter_mass

        new_vehicle_speed = max(
            0.0, vehicle_speed + acceleration * dt
        )

        new_wheel_speed = update_wheel_speed(
            wheel_speed,
            total_brake_force,
            tire_force,
            dt,
            wheel_radius,
            wheel_inertia
        )

        distance += (
            vehicle_speed + new_vehicle_speed
        ) * 0.5 * dt

        history["time"].append(time)
        history["vehicle_speed"].append(vehicle_speed)
        history["slip"].append(slip)
        history["regen_force"].append(braking["regen_force"])
        history["friction_force"].append(braking["friction_force"])
        history["total_brake_force"].append(total_brake_force)
        history["tire_force"].append(tire_force)

        vehicle_speed = new_vehicle_speed
        wheel_speed = new_wheel_speed
        time += dt

    return {
        "stop_time": time,
        "stop_distance": distance,
        "recovered_energy_kwh": recovered_energy_joules / 3_600_000,
        "initial_soc": initial_soc,
        "final_soc": battery_soc,
        "history": history
    }




if __name__ == "__main__":
    for enabled in [True, False]:
        result = simulate_coordinated_braking(
            road="wet",
            abs_enabled=enabled
        )

        print(
            f"ABS {'ON ' if enabled else 'OFF'} | "
            f"Distance: {result['stop_distance']:.2f} m | "
            f"Time: {result['stop_time']:.2f} s | "
            f"Recovered Energy: {result['recovered_energy_kwh']:.4f} kWh | "
            f"Initial SOC: {result['initial_soc'] * 100:.4f}% | "
            f"Final SOC: {result['final_soc'] * 100:.4f}%"
        )
