import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage48Reproducibility(unittest.TestCase):

    def test_reproducibility_across_roads(self):
        for road in ["dry", "wet", "snow"]:
            with self.subTest(road=road):
                settings = dict(
                    road=road,
                    initial_speed_kmh=100.0,
                    initial_soc=0.60,
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

                first = simulate_coordinated_braking(**settings)
                second = simulate_coordinated_braking(**settings)

                for key in [
                    "stop_distance",
                    "stop_time",
                    "recovered_energy_kwh",
                    "final_soc",
                ]:
                    self.assertEqual(
                        first[key],
                        second[key],
                        f"{road}: {key} differs between runs",
                    )

                self.assertEqual(
                    first["history"],
                    second["history"],
                    f"{road}: simulation histories differ",
                )


if __name__ == "__main__":
    unittest.main()
