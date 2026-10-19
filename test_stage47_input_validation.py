import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage47InputValidation(unittest.TestCase):

    def test_invalid_initial_speed(self):
        for value in [0, -10, 300, "100", None, float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    simulate_coordinated_braking(initial_speed_kmh=value)

    def test_invalid_initial_soc(self):
        for value in [-0.1, 1.1, "0.6", None, float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    simulate_coordinated_braking(initial_soc=value)

    def test_invalid_time_step(self):
        for value in [0, -0.001, 0.02, "0.0001", None, float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    simulate_coordinated_braking(time_step=value)

    def test_invalid_actuator_force(self):
        for value in [-1, 2501, "100", float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    simulate_coordinated_braking(initial_actuator_force=value)


if __name__ == "__main__":
    unittest.main()
