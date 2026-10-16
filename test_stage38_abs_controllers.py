import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage38ABSControllers(unittest.TestCase):

    def test_all_new_controllers(self):
        for controller in ("pi", "predictive", "predictive_pi"):
            with self.subTest(controller=controller):
                result = simulate_coordinated_braking(
                    road="snow",
                    initial_speed_kmh=30,
                    abs_controller=controller,
                    abs_gain=60,
                    pi_kp=60,
                    pi_ki=10,
                    prediction_time=0.015,
                    actuator_enabled=True,
                    actuator_response_time=0.05,
                    braking_mode="adaptive",
                    tire_model="enhanced",
                    initialization_mode="grip_based",
                )

                self.assertGreater(result["stop_distance"], 0)
                self.assertGreaterEqual(
                    result["recovered_energy_kwh"], 0
                )
                self.assertLessEqual(
                    max(result["history"]["slip"]), 1.0
                )

    def test_hybrid_reduces_peak_slip_vs_pi(self):
        def simulate(controller):
            return simulate_coordinated_braking(
                road="snow",
                initial_speed_kmh=30,
                abs_controller=controller,
                abs_gain=60,
                pi_kp=60,
                pi_ki=10,
                prediction_time=0.015,
                actuator_enabled=True,
                actuator_response_time=0.05,
                braking_mode="adaptive",
                tire_model="enhanced",
                initialization_mode="grip_based",
            )

        pi = simulate("pi")
        hybrid = simulate("predictive_pi")

        self.assertLess(
            max(hybrid["history"]["slip"]),
            max(pi["history"]["slip"]),
        )


if __name__ == "__main__":
    unittest.main()
    