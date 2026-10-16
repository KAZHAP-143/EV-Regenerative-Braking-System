import unittest
import math

from enhanced_tire_model import (
    enhanced_tire_friction_coefficient,
    enhanced_tire_force,
)


class TestEnhancedTireModel(unittest.TestCase):

    def test_zero_slip(self):
        for road in ["dry", "wet", "snow"]:
            with self.subTest(road=road):
                mu = enhanced_tire_friction_coefficient(0.0, road)
                self.assertAlmostEqual(mu, 0.0)

    def test_peak_friction(self):
        peaks = {
            "dry": (0.17, 0.85),
            "wet": (0.133, 0.45),
            "snow": (0.096, 0.20),
        }

        for road, (slip, expected_mu) in peaks.items():
            with self.subTest(road=road):
                mu = enhanced_tire_friction_coefficient(slip, road)
                self.assertAlmostEqual(mu, expected_mu, delta=0.001)

    def test_road_grip_order(self):
        slip = 0.10

        dry = enhanced_tire_friction_coefficient(slip, "dry")
        wet = enhanced_tire_friction_coefficient(slip, "wet")
        snow = enhanced_tire_friction_coefficient(slip, "snow")

        self.assertGreater(dry, wet)
        self.assertGreater(wet, snow)

    def test_force_calculation(self):
        normal_force = 375 * 9.81
        slip = 0.10

        mu = enhanced_tire_friction_coefficient(slip, "wet")
        force = enhanced_tire_force(slip, normal_force, "wet")

        self.assertAlmostEqual(force, mu * normal_force)

    def test_invalid_road(self):
        with self.assertRaises(ValueError):
            enhanced_tire_friction_coefficient(0.10, "ice")

    def test_negative_normal_force(self):
        with self.assertRaises(ValueError):
            enhanced_tire_force(0.10, -100, "snow")

    def test_nonfinite_slip(self):
        for value in [math.nan, math.inf, -math.inf]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    enhanced_tire_friction_coefficient(value, "wet")


if __name__ == "__main__":
    unittest.main()