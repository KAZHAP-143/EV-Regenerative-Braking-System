import unittest

from grip_based_brake_initializer import (
    calculate_initial_brake_force,
)


class TestGripBasedBrakeInitializer(unittest.TestCase):

    def setUp(self):
        self.normal_force = 375.0 * 9.81
        self.requested_force = 2500.0

    def test_dry_road(self):
        force = calculate_initial_brake_force(
            "dry", self.normal_force, self.requested_force
        )
        self.assertAlmostEqual(force, 2500.0)

    def test_wet_road(self):
        force = calculate_initial_brake_force(
            "wet", self.normal_force, self.requested_force
        )
        self.assertAlmostEqual(force, 1407.1, delta=0.2)

    def test_snow_road(self):
        force = calculate_initial_brake_force(
            "snow", self.normal_force, self.requested_force
        )
        self.assertAlmostEqual(force, 515.0, delta=0.2)

    def test_requested_force_limit(self):
        force = calculate_initial_brake_force(
            "dry", self.normal_force, 1000.0
        )
        self.assertAlmostEqual(force, 1000.0)

    def test_zero_requested_force(self):
        force = calculate_initial_brake_force(
            "wet", self.normal_force, 0.0
        )
        self.assertEqual(force, 0.0)

    def test_invalid_road(self):
        with self.assertRaises(ValueError):
            calculate_initial_brake_force(
                "ice", self.normal_force, self.requested_force
            )

    def test_negative_normal_force(self):
        with self.assertRaises(ValueError):
            calculate_initial_brake_force(
                "dry", -100.0, self.requested_force
            )

    def test_zero_normal_force(self):
        with self.assertRaises(ValueError):
            calculate_initial_brake_force(
                "dry", 0.0, self.requested_force
            )

    def test_negative_requested_force(self):
        with self.assertRaises(ValueError):
            calculate_initial_brake_force(
                "dry", self.normal_force, -100.0
            )


if __name__ == "__main__":
    unittest.main()