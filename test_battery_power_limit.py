
import unittest

from battery_power_limit import calculate_max_regen_force
from motor_power_model import calculate_regen_power


class TestBatteryPowerLimit(unittest.TestCase):

    def test_power_limit_at_speed(self):
        force = calculate_max_regen_force(
            max_battery_power=12500,
            wheel_speed=100
        )

        battery_power = calculate_regen_power(
            regen_force=force,
            wheel_speed=100
        ) * 0.95

        self.assertAlmostEqual(battery_power, 12500)

    def test_zero_wheel_speed(self):
        force = calculate_max_regen_force(
            max_battery_power=12500,
            wheel_speed=0
        )

        self.assertEqual(force, 0.0)

    def test_zero_power_limit(self):
        force = calculate_max_regen_force(
            max_battery_power=0,
            wheel_speed=60
        )

        self.assertEqual(force, 0.0)

    def test_negative_power_limit(self):
        with self.assertRaises(ValueError):
            calculate_max_regen_force(
                max_battery_power=-100,
                wheel_speed=60
            )

    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError):
            calculate_max_regen_force(
                max_battery_power=12500,
                wheel_speed=60,
                motor_efficiency=0
            )


if __name__ == "__main__":
    unittest.main()
