
import unittest

from coordinated_braking_simulation import simulate_coordinated_braking


class TestVehicleEnergyAccounting(unittest.TestCase):

    def test_energy_matches_soc_change(self):
        result = simulate_coordinated_braking(
            road="wet",
            abs_enabled=False,
            initial_soc=0.60,
            battery_temperature=25.0
        )

        battery_capacity_kwh = 60.0

        energy_from_soc = (
            result["final_soc"] - result["initial_soc"]
        ) * battery_capacity_kwh

        self.assertAlmostEqual(
            result["recovered_energy_kwh"],
            energy_from_soc,
            places=7
        )

    def test_full_battery_recovers_no_energy(self):
        result = simulate_coordinated_braking(
            road="wet",
            abs_enabled=False,
            initial_soc=1.0,
            battery_temperature=25.0
        )

        self.assertAlmostEqual(
            result["recovered_energy_kwh"],
            0.0,
            places=7
        )

    def test_high_temperature_blocks_regeneration(self):
        result = simulate_coordinated_braking(
            road="wet",
            abs_enabled=False,
            initial_soc=0.60,
            battery_temperature=60.0
        )

        self.assertAlmostEqual(
            result["recovered_energy_kwh"],
            0.0,
            places=7
        )


    def test_recovery_below_initial_kinetic_energy(self):
        vehicle_mass = 1500.0
        initial_speed = 100.0 / 3.6

        initial_energy_kwh = (
            0.5 * vehicle_mass * initial_speed**2
        ) / 3_600_000

        for abs_enabled in [True, False]:
            result = simulate_coordinated_braking(
                road="wet",
                abs_enabled=abs_enabled,
                initial_soc=0.60,
                battery_temperature=25.0
            )

            self.assertGreaterEqual(
                result["recovered_energy_kwh"], 0.0
            )

            self.assertLessEqual(
                result["recovered_energy_kwh"],
                initial_energy_kwh
            )


if __name__ == "__main__":
    unittest.main()
