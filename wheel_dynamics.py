

def calculate_slip_ratio(
    vehicle_speed,
    wheel_speed,
    wheel_radius=0.30
):
    """
    Calculate longitudinal braking slip ratio.

    vehicle_speed: m/s
    wheel_speed: rad/s
    wheel_radius: meters

    A 0.5 m/s reference-speed floor improves
    numerical stability near standstill.
    """

    if vehicle_speed <= 0:
        return 0.0

    wheel_linear_speed = wheel_speed * wheel_radius

    reference_speed = max(vehicle_speed, 0.5)

    slip_ratio = (
        vehicle_speed - wheel_linear_speed
    ) / reference_speed

    return max(0.0, min(1.0, slip_ratio))



# Example test
if __name__ == "__main__":
    vehicle_speed = 20.0
    wheel_speed = 50.0

    slip = calculate_slip_ratio(vehicle_speed, wheel_speed)

    print(f"Wheel slip ratio: {slip:.3f}")
    print(f"Wheel slip percentage: {slip * 100:.1f}%")

def update_wheel_speed(
    wheel_speed,
    brake_force,
    tire_force,
    time_step,
    wheel_radius=0.30,
    wheel_inertia=1.8
):
    """
    Update wheel angular speed using rotational dynamics.

    wheel_speed: angular speed (rad/s)
    brake_force: equivalent braking force at wheel (N)
    tire_force: road force acting on wheel (N)
    time_step: simulation time step (s)
    wheel_radius: wheel radius (m)
    wheel_inertia: rotational inertia (kg m^2)
    """

    if wheel_inertia <= 0:
        raise ValueError("Wheel inertia must be positive")

    if time_step <= 0:
        raise ValueError("Time step must be positive")

    # Convert forces into torques
    braking_torque = brake_force * wheel_radius
    road_torque = tire_force * wheel_radius

    # Newton's second law for rotation
    angular_acceleration = (
        road_torque - braking_torque
    ) / wheel_inertia

    # Euler integration
    new_wheel_speed = (
        wheel_speed + angular_acceleration * time_step
    )

    # Prevent reverse wheel rotation in this braking model
    return max(0.0, new_wheel_speed)
