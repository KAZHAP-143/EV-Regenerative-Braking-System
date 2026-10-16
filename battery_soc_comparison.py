
from coordinated_braking_simulation import simulate_coordinated_braking

print("Battery SOC Comparison — Wet Road")
print("-" * 85)

for soc in [0.60, 0.95, 1.00]:
    for abs_enabled in [True, False]:

        result = simulate_coordinated_braking(
            road="wet",
            abs_enabled=abs_enabled,
            initial_soc=soc
        )

        print(
            f"Initial SOC: {soc * 100:5.1f}% | "
            f"ABS: {'ON ' if abs_enabled else 'OFF'} | "
            f"Distance: {result['stop_distance']:7.2f} m | "
            f"Recovered: {result['recovered_energy_kwh']:.5f} kWh | "
            f"Final SOC: {result['final_soc'] * 100:.4f}%"
        )

    print("-" * 85)
