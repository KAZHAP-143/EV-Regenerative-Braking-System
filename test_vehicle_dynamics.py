
import unittest
import numpy as np
from vehicle_dynamics import simulate


class TestEVBraking(unittest.TestCase):

    def test_vehicle_stops(self):
        result = simulate(mu=0.85)
        self.assertAlmostEqual(result["speed"][-1], 0.0)

    def test_speed_never_negative(self):
        result = simulate(mu=0.85)
        self.assertTrue(np.all(result["speed"] >= 0))

    def test_wet_road_longer_stopping_distance(self):
        dry = simulate(mu=0.85, brake_force=10000)
        wet = simulate(mu=0.45, brake_force=10000)
        self.assertGreater(wet["distance"], dry["distance"])

    def test_full_battery_blocks_regeneration(self):
        result = simulate(mu=0.85, initial_soc=1.0)
        self.assertAlmostEqual(result["energy_kwh"], 0.0)

    def test_energy_conservation(self):
        result = simulate(
            mu=0.85,
            initial_speed_kmh=100,
            brake_force=4500,
            initial_soc=0.60
        )

        initial_energy = (
            0.5 * 1500 * (100 / 3.6) ** 2
        ) / 3_600_000

        accounted_energy = sum([
            result["energy_kwh"],
            result["friction_energy_kwh"],
            result["drag_energy_kwh"],
            result["rolling_energy_kwh"],
            result["motor_loss_energy_kwh"]
        ])

        self.assertAlmostEqual(
            initial_energy,
            accounted_energy,
            delta=1e-5
        )


if __name__ == "__main__":
    unittest.main()
