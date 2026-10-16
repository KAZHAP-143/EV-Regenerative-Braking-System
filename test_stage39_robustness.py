
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage39Robustness(unittest.TestCase):

    def run_simulation(self, soc):
        return simulate_coordinated_braking(
            road="snow",
            initial_speed_kmh=100,
            initial_soc=soc,
            abs_controller="predictive_pi",
            pi_kp=60,
            pi_ki=10,
            prediction_time=0.030,
            actuator_enabled=True,
            actuator_response_time=0.10,
            braking_mode="adaptive",
            tire_model="enhanced",
            initialization_mode="grip_based",
        )

    def test_full_battery_disables_regeneration(self):
        result = self.run_simulation(1.0)

        self.assertAlmostEqual(
            result["recovered_energy_kwh"], 0.0
        )

        self.assertAlmostEqual(
            max(result["history"]["regen_force"]), 0.0
        )

    def test_braking_force_balance(self):
        for soc in [0.20, 1.0]:
            with self.subTest(soc=soc):
                result = self.run_simulation(soc)
                history = result["history"]

                for regen, friction, total in zip(
                    history["regen_force"],
                    history["friction_force"],
                    history["total_brake_force"],
                ):
                    self.assertAlmostEqual(
                        regen + friction, total, places=6
                    )

    def test_friction_compensates_at_full_soc(self):
        low_soc = self.run_simulation(0.20)
        full_soc = self.run_simulation(1.0)

        self.assertGreater(
            max(full_soc["history"]["friction_force"]),
            max(low_soc["history"]["friction_force"]),
        )

        self.assertAlmostEqual(
            low_soc["stop_distance"],
            full_soc["stop_distance"],
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
