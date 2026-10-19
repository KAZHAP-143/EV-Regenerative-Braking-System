import unittest

from wheel_dynamics import calculate_slip_ratio


class TestStage46SlipBoundary(unittest.TestCase):

    def test_stationary_vehicle(self):
        self.assertEqual(
            calculate_slip_ratio(0.0, 0.0),
            0.0
        )

    def test_locked_wheel_at_reference_speed(self):
        self.assertAlmostEqual(
            calculate_slip_ratio(0.5, 0.0),
            1.0
        )

    def test_locked_wheel_below_reference_speed(self):
        self.assertAlmostEqual(
            calculate_slip_ratio(0.1, 0.0),
            0.2
        )

    def test_free_rolling_wheel(self):
        for speed in [0.1, 0.5, 1.0, 10.0]:
            with self.subTest(speed=speed):
                slip = calculate_slip_ratio(
                    speed,
                    speed / 0.30
                )
                self.assertAlmostEqual(slip, 0.0)


if __name__ == "__main__":
    unittest.main()
