
import unittest

from brake_coordinator import coordinate_braking


class TestBrakeCoordinator(unittest.TestCase):

    def test_normal_braking(self):
        result = coordinate_braking(5000, 3000)

        self.assertEqual(result["regen_force"], 3000)
        self.assertEqual(result["friction_force"], 2000)
        self.assertEqual(result["total_brake_force"], 5000)

    
    def test_abs_reduces_braking(self):
        result = coordinate_braking(5000, 3000, 0.5)

        self.assertEqual(result["regen_force"], 0)
        self.assertEqual(result["friction_force"], 2500)
        self.assertEqual(result["total_brake_force"], 2500)


    def test_zero_regen_capacity(self):
        result = coordinate_braking(5000, 0)

        self.assertEqual(result["regen_force"], 0)
        self.assertEqual(result["friction_force"], 5000)

    def test_invalid_abs_factor(self):
        with self.assertRaises(ValueError):
            coordinate_braking(5000, 3000, 1.5)


if __name__ == "__main__":
    unittest.main()
