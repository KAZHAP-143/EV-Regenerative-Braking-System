
import unittest

from battery_soc_control import calculate_regen_soc_factor
from battery_temperature_control import calculate_regen_temperature_factor


class TestBatteryControls(unittest.TestCase):

    def test_normal_soc(self):
        self.assertAlmostEqual(
            calculate_regen_soc_factor(0.60), 1.0
        )

    def test_high_soc(self):
        self.assertAlmostEqual(
            calculate_regen_soc_factor(0.95), 0.5
        )

    def test_full_battery(self):
        self.assertAlmostEqual(
            calculate_regen_soc_factor(1.00), 0.0
        )

    def test_invalid_soc(self):
        with self.assertRaises(ValueError):
            calculate_regen_soc_factor(1.10)

    def test_normal_temperature(self):
        self.assertAlmostEqual(
            calculate_regen_temperature_factor(25), 1.0
        )

    def test_cold_battery(self):
        self.assertAlmostEqual(
            calculate_regen_temperature_factor(0), 0.5
        )

    def test_hot_battery(self):
        self.assertAlmostEqual(
            calculate_regen_temperature_factor(50), 0.5
        )

    def test_extreme_temperature(self):
        self.assertAlmostEqual(
            calculate_regen_temperature_factor(60), 0.0
        )


if __name__ == "__main__":
    unittest.main()
