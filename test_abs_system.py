
import unittest

from wheel_dynamics import calculate_slip_ratio, update_wheel_speed
from abs_controller import abs_brake_control
from tire_model import tire_friction_coefficient, calculate_tire_force
from abs_vehicle_simulation import simulate_abs


class TestABSSystem(unittest.TestCase):

    def test_zero_slip(self):
        slip = calculate_slip_ratio(
            vehicle_speed=20,
            wheel_speed=20 / 0.30
        )
        self.assertAlmostEqual(slip, 0.0, places=5)

    def test_locked_wheel(self):
        slip = calculate_slip_ratio(
            vehicle_speed=20,
            wheel_speed=0
        )
        self.assertAlmostEqual(slip, 1.0)

    def test_abs_activation(self):
        result = abs_brake_control(
            vehicle_speed=20,
            wheel_speed=50,
            requested_brake_force=6000
        )
        self.assertAlmostEqual(result["brake_force"], 3000)
        self.assertIn("ABS ACTIVE", result["status"])

    def test_normal_braking(self):
        result = abs_brake_control(
            vehicle_speed=20,
            wheel_speed=20 / 0.30,
            requested_brake_force=6000
        )
        self.assertAlmostEqual(result["brake_force"], 6000)

    def test_wheel_deceleration(self):
        new_speed = update_wheel_speed(
            wheel_speed=60,
            brake_force=3000,
            tire_force=2000,
            time_step=0.01
        )
        self.assertAlmostEqual(new_speed, 58.333333, places=4)

    def test_dry_traction_higher_than_wet(self):
        dry_mu = tire_friction_coefficient(0.15, "dry")
        wet_mu = tire_friction_coefficient(0.15, "wet")
        self.assertGreater(dry_mu, wet_mu)

    def test_tire_force_nonnegative(self):
        force = calculate_tire_force(
            slip_ratio=0.15,
            normal_force=3500,
            road="dry"
        )
        self.assertGreaterEqual(force, 0)

    def test_abs_reduces_wet_stopping_distance(self):
        abs_on = simulate_abs("wet", True)
        abs_off = simulate_abs("wet", False)

        self.assertLess(
            abs_on["stop_distance"],
            abs_off["stop_distance"]
        )


if __name__ == "__main__":
    unittest.main()
