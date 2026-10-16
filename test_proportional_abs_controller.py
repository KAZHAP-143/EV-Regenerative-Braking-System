
import unittest

from proportional_abs_controller import proportional_abs_control


class TestProportionalABSController(unittest.TestCase):

    def test_zero_slip(self):
        self.assertEqual(proportional_abs_control(0.0), 1.0)

    def test_below_target_slip(self):
        self.assertEqual(proportional_abs_control(0.10), 1.0)

    def test_target_slip(self):
        self.assertEqual(proportional_abs_control(0.15), 1.0)

    def test_above_target_slip(self):
        self.assertAlmostEqual(
            proportional_abs_control(0.20), 0.65
        )

    def test_high_slip(self):
        self.assertAlmostEqual(
            proportional_abs_control(0.30), 0.0
        )

    def test_extreme_slip(self):
        self.assertEqual(proportional_abs_control(0.50), 0.0)

    def test_invalid_slip(self):
        with self.assertRaises(ValueError):
            proportional_abs_control(1.2)

    def test_invalid_gain(self):
        with self.assertRaises(ValueError):
            proportional_abs_control(0.20, gain=-1.0)


if __name__ == "__main__":
    unittest.main()
