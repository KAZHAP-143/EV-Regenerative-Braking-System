
import unittest

from motor_power_model import calculate_regen_power


class TestMotorPowerModel(unittest.TestCase):

    def test_normal_regeneration(self):
        power = calculate_regen_power(
            regen_force=1500,
            wheel_speed=60
        )
        self.assertAlmostEqual(power, 22950.0)

    def test_locked_wheel_zero_power(self):
        power = calculate_regen_power(
            regen_force=1500,
            wheel_speed=0
        )
        self.assertEqual(power, 0.0)

    def test_negative_wheel_speed(self):
        power = calculate_regen_power(
            regen_force=1500,
            wheel_speed=-10
        )
        self.assertEqual(power, 0.0)

    def test_zero_regen_force(self):
        power = calculate_regen_power(
            regen_force=0,
            wheel_speed=60
        )
        self.assertEqual(power, 0.0)

    def test_invalid_regen_force(self):
        with self.assertRaises(ValueError):
            calculate_regen_power(
                regen_force=-100,
                wheel_speed=60
            )

    def test_invalid_wheel_radius(self):
        with self.assertRaises(ValueError):
            calculate_regen_power(
                regen_force=1500,
                wheel_speed=60,
                wheel_radius=0
            )


if __name__ == "__main__":
    unittest.main()

