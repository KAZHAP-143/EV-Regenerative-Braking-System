
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage43SpeedPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.results = {}

        for speed in [30, 60, 100]:
            cls.results[speed] = simulate_coordinated_braking(
                road="wet",
                initial_speed_kmh=speed,
                initial_soc=0.60,
                abs_controller="predictive_pi",
                pi_kp=60,
                pi_ki=10,
                prediction_time=0.030,
                actuator_enabled=True,
                actuator_response_time=0.05,
                braking_mode="adaptive",
                tire_model="enhanced",
                initialization_mode="grip_based",
            )

    def test_stopping_distance_increases_with_speed(self):
        r = self.results

        self.assertLess(r[30]["stop_distance"], r[60]["stop_distance"])
        self.assertLess(r[60]["stop_distance"], r[100]["stop_distance"])

    def test_stopping_time_increases_with_speed(self):
        r = self.results

        self.assertLess(r[30]["stop_time"], r[60]["stop_time"])
        self.assertLess(r[60]["stop_time"], r[100]["stop_time"])

    def test_recovered_energy_increases_with_speed(self):
        r = self.results

        self.assertLess(
            r[30]["recovered_energy_kwh"],
            r[60]["recovered_energy_kwh"],
        )
        self.assertLess(
            r[60]["recovered_energy_kwh"],
            r[100]["recovered_energy_kwh"],
        )

    def test_vehicle_speed_never_becomes_negative(self):
        for speed, result in self.results.items():
            with self.subTest(initial_speed_kmh=speed):
                self.assertTrue(
                    all(v >= 0 for v in result["history"]["vehicle_speed"])
                )

    def test_peak_slip_is_consistent_across_speeds(self):
        peaks = [
            max(result["history"]["slip"])
            for result in self.results.values()
        ]

        self.assertLess(max(peaks) - min(peaks), 0.001)


if __name__ == "__main__":
    unittest.main()
