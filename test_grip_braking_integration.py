import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestGripBrakingIntegration(unittest.TestCase):

    def simulate(self, road, mode):
        return simulate_coordinated_braking(
            road=road,
            initial_speed_kmh=30,
            abs_enabled=True,
            abs_controller="road_adaptive",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            abs_gain=60.0,
            initialization_mode=mode,
        )

    def test_snow_peak_slip_reduction(self):
        original = self.simulate("snow", "original")
        grip_based = self.simulate("snow", "grip_based")

        original_peak = max(original["history"]["slip"])
        grip_peak = max(grip_based["history"]["slip"])

        self.assertLess(grip_peak, original_peak)

    def test_wet_peak_slip_reduction(self):
        original = self.simulate("wet", "original")
        grip_based = self.simulate("wet", "grip_based")

        self.assertLess(
            max(grip_based["history"]["slip"]),
            max(original["history"]["slip"]),
        )

    def test_snow_stopping_distance(self):
        original = self.simulate("snow", "original")
        grip_based = self.simulate("snow", "grip_based")

        self.assertLess(
            grip_based["stop_distance"],
            original["stop_distance"],
        )

    def test_invalid_initialization_mode(self):
        with self.assertRaises(ValueError):
            simulate_coordinated_braking(
                initialization_mode="invalid"
            )

    def test_explicit_initial_force_override(self):
        explicit = simulate_coordinated_braking(
            road="snow",
            initial_speed_kmh=30,
            abs_controller="road_adaptive",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            abs_gain=60.0,
            initialization_mode="grip_based",
            initial_actuator_force=500.0,
        )

        baseline = simulate_coordinated_braking(
            road="snow",
            initial_speed_kmh=30,
            abs_controller="road_adaptive",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            abs_gain=60.0,
            initial_actuator_force=500.0,
        )

        self.assertAlmostEqual(
            explicit["stop_distance"],
            baseline["stop_distance"],
        )


if __name__ == "__main__":
    unittest.main()
