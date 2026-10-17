
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage40EnergyConservation(unittest.TestCase):

    def test_wet_road_energy_balance(self):
        result = simulate_coordinated_braking(
            road="wet",
            initial_speed_kmh=100,
            abs_controller="predictive_pi",
            pi_kp=60,
            pi_ki=10,
            prediction_time=0.030,
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            initialization_mode="grip_based",
        )

        history = result["history"]

        dt = 0.0001
        mass = 1500.0
        wheel_count = 4
        wheel_radius = 0.30
        wheel_inertia = 1.8
        motor_efficiency = 0.85
        charging_efficiency = 0.95

        initial_speed = 100 / 3.6
        initial_wheel_speed = initial_speed / wheel_radius

        initial_energy = (
            0.5 * mass * initial_speed**2
            + wheel_count
            * 0.5
            * wheel_inertia
            * initial_wheel_speed**2
        )

        friction_energy = 0.0
        tire_slip_energy = 0.0
        regen_mechanical_energy = 0.0

        for vehicle_speed, wheel_speed, tire_force, friction_force, regen_force in zip(
            history["vehicle_speed"],
            history["wheel_speed"],
            history["tire_force"],
            history["friction_force"],
            history["regen_force"],
        ):
            wheel_linear_speed = wheel_speed * wheel_radius

            friction_energy += (
                wheel_count * friction_force * wheel_linear_speed * dt
            )

            tire_slip_energy += (
                wheel_count
                * tire_force
                * (vehicle_speed - wheel_linear_speed)
                * dt
            )

            regen_mechanical_energy += (
                wheel_count * regen_force * wheel_linear_speed * dt
            )

        motor_loss = regen_mechanical_energy * (1 - motor_efficiency)

        charging_loss = (
            regen_mechanical_energy
            * motor_efficiency
            * (1 - charging_efficiency)
        )

        recovered_energy = result["recovered_energy_kwh"] * 3_600_000

        accounted_energy = (
            friction_energy
            + tire_slip_energy
            + motor_loss
            + charging_loss
            + recovered_energy
        )

        relative_error = abs(initial_energy - accounted_energy) / initial_energy

        print(f"Energy balance residual: {initial_energy - accounted_energy:.6f} J")
        print(f"Relative energy error: {relative_error * 100:.6f}%")

        self.assertLess(relative_error, 0.001)


if __name__ == "__main__":
    unittest.main()
