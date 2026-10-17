
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage42SOCBrakingPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.results = {}

        for soc in [0.20, 0.60, 0.99, 1.00]:
            result = simulate_coordinated_braking(
                road="wet",
                initial_soc=soc,
                initial_speed_kmh=100,
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

            history = result["history"]

            avg_regen = (
                sum(history["regen_force"])
                / len(history["regen_force"])
            )

            avg_friction = (
                sum(history["friction_force"])
                / len(history["friction_force"])
            )

            cls.results[soc] = {
                "distance": result["stop_distance"],
                "energy": result["recovered_energy_kwh"],
                "regen": avg_regen,
                "friction": avg_friction,
                "total": avg_regen + avg_friction,
            }

    def test_regeneration_decreases_near_full_soc(self):
        r = self.results

        self.assertAlmostEqual(
            r[0.20]["energy"],
            r[0.60]["energy"],
            places=6,
        )

        self.assertGreater(
            r[0.60]["energy"],
            r[0.99]["energy"],
        )

        self.assertGreater(
            r[0.99]["energy"],
            r[1.00]["energy"],
        )

    def test_full_battery_disables_regeneration(self):
        r = self.results[1.00]

        self.assertAlmostEqual(r["energy"], 0.0, places=9)
        self.assertAlmostEqual(r["regen"], 0.0, places=6)

    def test_friction_compensates_for_reduced_regen(self):
        r = self.results

        for soc in [0.20, 0.60, 0.99, 1.00]:
            with self.subTest(soc=soc):
                self.assertAlmostEqual(
                    r[soc]["total"],
                    r[0.20]["total"],
                    delta=0.1,
                )

        self.assertLess(
            r[0.20]["friction"],
            r[0.99]["friction"],
        )

        self.assertLess(
            r[0.99]["friction"],
            r[1.00]["friction"],
        )

    def test_stopping_distance_remains_consistent(self):
        r = self.results

        for soc in [0.60, 0.99, 1.00]:
            with self.subTest(soc=soc):
                self.assertAlmostEqual(
                    r[soc]["distance"],
                    r[0.20]["distance"],
                    delta=0.1,
                )


if __name__ == "__main__":
    unittest.main()
