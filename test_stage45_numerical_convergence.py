import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage45NumericalConvergence(unittest.TestCase):

    def test_time_step_convergence_all_roads(self):
        settings = dict(
            initial_soc=0.60,
            initial_speed_kmh=100.0,
            abs_controller="predictive_pi",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            initialization_mode="grip_based",
            prediction_time=0.030,
            pi_kp=60.0,
            pi_ki=10.0,
        )

        for road in ["dry", "wet", "snow"]:
            with self.subTest(road=road):
                coarse = simulate_coordinated_braking(
                    road=road, time_step=0.0002, **settings
                )
                fine = simulate_coordinated_braking(
                    road=road, time_step=0.00005, **settings
                )

                distance_error = abs(
                    coarse["stop_distance"] - fine["stop_distance"]
                ) / fine["stop_distance"]

                energy_error = abs(
                    coarse["recovered_energy_kwh"]
                    - fine["recovered_energy_kwh"]
                ) / fine["recovered_energy_kwh"]

                self.assertLess(distance_error, 0.001)
                self.assertLess(energy_error, 0.001)


if __name__ == "__main__":
    unittest.main()
