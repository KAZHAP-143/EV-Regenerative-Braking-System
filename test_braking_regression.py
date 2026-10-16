
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestBrakingRegression(unittest.TestCase):

    def test_wet_road_braking_performance(self):
        for mode in ("original", "adaptive"):
            with self.subTest(mode=mode):
                result = simulate_coordinated_braking(
                    road="wet",
                    abs_enabled=True,
                    abs_controller="proportional",
                    actuator_enabled=True,
                    actuator_response_time=0.02,
                    braking_mode=mode,
                )

                history = result["history"]

                # Baseline established in Stage 31
                self.assertAlmostEqual(
                    result["stop_distance"],
                    87.98,
                    delta=0.5,
                )

                self.assertAlmostEqual(
                    result["stop_time"],
                    6.32,
                    delta=0.1,
                )

                self.assertLessEqual(
                    max(history["slip"]),
                    0.205,
                )

                expected_energy = {
                    "original": 0.001104,
                    "adaptive": 0.067590,
                }

                self.assertAlmostEqual(
                    result["recovered_energy_kwh"],
                    expected_energy[mode],
                    delta=0.002,
                )

                print(
                    f"{mode}: "
                    f"distance={result['stop_distance']:.2f} m, "
                    f"time={result['stop_time']:.2f} s, "
                    f"energy={result['recovered_energy_kwh']:.6f} kWh"
                )


if __name__ == "__main__":
    unittest.main()
