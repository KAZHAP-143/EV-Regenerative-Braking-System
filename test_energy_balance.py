
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestEnergyBalance(unittest.TestCase):

    def test_energy_balance_for_both_modes(self):
        dt = 0.0001
        wheel_count = 4
        wheel_inertia = 1.8
        vehicle_mass = 1500.0
        initial_speed = 100.0 / 3.6

        for mode in ("original", "adaptive"):
            with self.subTest(mode=mode):
                result = simulate_coordinated_braking(
                    road="wet",
                    abs_enabled=True,
                    abs_controller="proportional",
                    actuator_enabled=True,
                    actuator_response_time=0.02,
                    braking_mode=mode,
                )

                h = result["history"]

                initial_ke = (
                    0.5 * vehicle_mass * initial_speed ** 2
                    + 0.5 * wheel_count * wheel_inertia
                    * h["wheel_speed"][0] ** 2
                )

                final_ke = (
                    0.5 * vehicle_mass
                    * h["vehicle_speed"][-1] ** 2
                    + 0.5 * wheel_count * wheel_inertia
                    * h["wheel_speed"][-1] ** 2
                )

                energy_sinks = 0.0

                for v, slip, tire, friction, regen in zip(
                    h["vehicle_speed"],
                    h["slip"],
                    h["tire_force"],
                    h["friction_force"],
                    h["regen_force"],
                ):
                    wheel_surface_speed = max(
                        0.0, v * (1.0 - slip)
                    )

                    tire_slip_power = (
                        tire * (v - wheel_surface_speed)
                    )

                    brake_power = (
                        (friction + regen) * wheel_surface_speed
                    )

                    energy_sinks += (
                        tire_slip_power + brake_power
                    ) * dt * wheel_count

                residual = (
                    initial_ke - final_ke - energy_sinks
                )

                print(
                    f"{mode}: residual = "
                    f"{residual / 3_600_000:.6f} kWh"
                )

                self.assertLess(
                    abs(residual),
                    100.0,
                    f"{mode} energy residual exceeds 100 J",
                )


if __name__ == "__main__":
    unittest.main()
