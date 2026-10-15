
from wheel_dynamics import (
    calculate_slip_ratio,
    update_wheel_speed
)
from abs_controller import abs_brake_control
from tire_model import calculate_tire_force


def simulate_abs(road="dry", abs_enabled=True):
    """
    Simplified quarter-car braking simulation.
    """

    vehicle_mass = 1500.0
    quarter_mass = vehicle_mass / 4

    wheel_radius = 0.30
    wheel_inertia = 1.8

    gravity = 9.81
    normal_force = quarter_mass * gravity

    time_step = 0.0001
    initial_speed = 100 / 3.6

    vehicle_speed = initial_speed
    wheel_speed = initial_speed / wheel_radius

    requested_brake_force = 2500.0

    time = 0.0
    distance = 0.0

    history = {
        "time": [],
        "vehicle_speed": [],
        "wheel_speed": [],
        "slip": [],
        "brake_force": [],
        "tire_force": []
    }

    while vehicle_speed > 0.01 and time < 60:

        slip = calculate_slip_ratio(
            vehicle_speed,
            wheel_speed,
            wheel_radius
        )

        if abs_enabled:
            controller = abs_brake_control(
                vehicle_speed,
                wheel_speed,
                requested_brake_force,
                wheel_radius
            )
            brake_force = controller["brake_force"]
        else:
            brake_force = requested_brake_force

        tire_force = calculate_tire_force(
            slip,
            normal_force,
            road
        )

        # Longitudinal vehicle dynamics
        acceleration = -tire_force / quarter_mass

        new_vehicle_speed = max(
            0.0,
            vehicle_speed + acceleration * time_step
        )

        # Wheel rotational dynamics
        new_wheel_speed = update_wheel_speed(
            wheel_speed,
            brake_force,
            tire_force,
            time_step,
            wheel_radius,
            wheel_inertia
        )

        distance += (
            vehicle_speed + new_vehicle_speed
        ) * 0.5 * time_step

        history["time"].append(time)
        history["vehicle_speed"].append(vehicle_speed)
        history["wheel_speed"].append(wheel_speed)
        history["slip"].append(slip)
        history["brake_force"].append(brake_force)
        history["tire_force"].append(tire_force)

        vehicle_speed = new_vehicle_speed
        wheel_speed = new_wheel_speed

        time += time_step

    return {
        "stop_time": time,
        "stop_distance": distance,
        "final_speed": vehicle_speed,
        "history": history
    }


if __name__ == "__main__":

    for road in ["dry", "wet"]:
        for abs_enabled in [True, False]:

            result = simulate_abs(
                road=road,
                abs_enabled=abs_enabled
            )

            print(
                f"Road: {road.upper():3s} | "
                f"ABS: {'ON ' if abs_enabled else 'OFF'} | "
                f"Stopping Distance: "
                f"{result['stop_distance']:.2f} m | "
                f"Stopping Time: "
                f"{result['stop_time']:.2f} s"
            )
