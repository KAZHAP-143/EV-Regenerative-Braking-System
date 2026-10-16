
import unittest

from brake_actuator import update_brake_pressure


class TestBrakeActuator(unittest.TestCase):

    def test_pressure_reduction(self):
        result = update_brake_pressure(
            2500, 1000, dt=0.01
        )
        self.assertAlmostEqual(result, 2200.0)

    def test_pressure_increase(self):
        result = update_brake_pressure(
            1000, 2500, dt=0.01
        )
        self.assertAlmostEqual(result, 1300.0)

    def test_no_pressure_change(self):
        result = update_brake_pressure(
            1500, 1500, dt=0.01
        )
        self.assertAlmostEqual(result, 1500.0)

    def test_zero_target_pressure(self):
        result = update_brake_pressure(
            1000, 0, dt=0.01
        )
        self.assertAlmostEqual(result, 800.0)

    def test_invalid_negative_force(self):
        with self.assertRaises(ValueError):
            update_brake_pressure(-100, 1000, dt=0.01)

    def test_invalid_time_step(self):
        with self.assertRaises(ValueError):
            update_brake_pressure(1000, 500, dt=0)

    def test_invalid_response_time(self):
        with self.assertRaises(ValueError):
            update_brake_pressure(
                1000, 500, dt=0.01, response_time=0
            )


if __name__ == "__main__":
    unittest.main()
