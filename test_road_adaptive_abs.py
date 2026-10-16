import unittest

from road_adaptive_abs_controller import (
    road_adaptive_abs_control,
    ROAD_SLIP_TARGETS,
)


class TestRoadAdaptiveABS(unittest.TestCase):

    def test_road_targets(self):
        self.assertAlmostEqual(ROAD_SLIP_TARGETS["dry"], 0.170)
        self.assertAlmostEqual(ROAD_SLIP_TARGETS["wet"], 0.133)
        self.assertAlmostEqual(ROAD_SLIP_TARGETS["snow"], 0.096)

    def test_no_reduction_below_target(self):
        for road, target in ROAD_SLIP_TARGETS.items():
            with self.subTest(road=road):
                factor = road_adaptive_abs_control(
                    target / 2,
                    road=road
                )
                self.assertAlmostEqual(factor, 1.0)

    def test_reduction_above_target(self):
        for road, target in ROAD_SLIP_TARGETS.items():
            with self.subTest(road=road):
                factor = road_adaptive_abs_control(
                    target + 0.05,
                    road=road
                )
                self.assertLess(factor, 1.0)
                self.assertGreaterEqual(factor, 0.0)

    def test_gain_changes_output(self):
        low = road_adaptive_abs_control(
            0.20, road="snow", gain=7.0
        )
        high = road_adaptive_abs_control(
            0.20, road="snow", gain=8.0
        )
        self.assertLess(high, low)

    def test_invalid_road(self):
        with self.assertRaises(ValueError):
            road_adaptive_abs_control(0.15, road="ice")

    def test_invalid_gain(self):
        with self.assertRaises(ValueError):
            road_adaptive_abs_control(
                0.15, road="snow", gain=-1
            )


if __name__ == "__main__":
    unittest.main()