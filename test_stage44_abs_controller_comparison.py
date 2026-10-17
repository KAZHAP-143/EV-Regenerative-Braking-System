
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestStage44ABSControllerComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.results = {}

        for road in ["dry", "wet", "snow"]:
            for controller in ["pi", "predictive", "predictive_pi"]:
                cls.results[(road, controller)] = (
                    simulate_coordinated_braking(
                        road=road,
                        initial_speed_kmh=100,
                        initial_soc=0.60,
                        abs_controller=controller,
                        pi_kp=60,
                        pi_ki=10,
                        prediction_time=0.030,
                        actuator_enabled=True,
                        actuator_response_time=0.05,
                        braking_mode="adaptive",
                        tire_model="enhanced",
                        initialization_mode="grip_based",
                    )
                )

    def test_predictive_pi_matches_other_controllers_on_dry_road(self):
        pi = self.results[("dry", "pi")]
        predictive = self.results[("dry", "predictive")]
        hybrid = self.results[("dry", "predictive_pi")]

        self.assertAlmostEqual(
            pi["stop_distance"], predictive["stop_distance"], places=2
        )
        self.assertAlmostEqual(
            pi["stop_distance"], hybrid["stop_distance"], places=2
        )

    def test_predictive_pi_has_lower_peak_slip_on_wet_road(self):
        pi = self.results[("wet", "pi")]
        predictive = self.results[("wet", "predictive")]
        hybrid = self.results[("wet", "predictive_pi")]

        pi_slip = max(pi["history"]["slip"])
        predictive_slip = max(predictive["history"]["slip"])
        hybrid_slip = max(hybrid["history"]["slip"])

        self.assertLess(hybrid_slip, pi_slip)
        self.assertLess(hybrid_slip, predictive_slip)

    def test_predictive_pi_stops_shortest_on_wet_road(self):
        pi = self.results[("wet", "pi")]
        predictive = self.results[("wet", "predictive")]
        hybrid = self.results[("wet", "predictive_pi")]

        self.assertLess(hybrid["stop_distance"], pi["stop_distance"])
        self.assertLess(hybrid["stop_distance"], predictive["stop_distance"])

    def test_predictive_pi_stops_shortest_on_snow(self):
        pi = self.results[("snow", "pi")]
        predictive = self.results[("snow", "predictive")]
        hybrid = self.results[("snow", "predictive_pi")]

        self.assertLess(hybrid["stop_distance"], pi["stop_distance"])
        self.assertLess(hybrid["stop_distance"], predictive["stop_distance"])

    def test_predictive_pi_has_lowest_peak_slip_on_snow(self):
        pi = self.results[("snow", "pi")]
        predictive = self.results[("snow", "predictive")]
        hybrid = self.results[("snow", "predictive_pi")]

        pi_slip = max(pi["history"]["slip"])
        predictive_slip = max(predictive["history"]["slip"])
        hybrid_slip = max(hybrid["history"]["slip"])

        self.assertLess(hybrid_slip, pi_slip)
        self.assertLess(hybrid_slip, predictive_slip)

    def test_stopping_distance_increases_from_dry_to_snow(self):
        for controller in ["pi", "predictive", "predictive_pi"]:
            with self.subTest(controller=controller):
                dry = self.results[("dry", controller)]
                wet = self.results[("wet", controller)]
                snow = self.results[("snow", controller)]

                self.assertLess(dry["stop_distance"], wet["stop_distance"])
                self.assertLess(wet["stop_distance"], snow["stop_distance"])


if __name__ == "__main__":
    unittest.main()
