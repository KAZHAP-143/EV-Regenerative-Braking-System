
from coordinated_braking_simulation import simulate_coordinated_braking

print("Battery Temperature Comparison — Wet Road")
print("-" * 95)

for temperature in [-10, 0, 25, 50, 60]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=False,
        initial_soc=0.60,
        battery_temperature=temperature
    )

    print(
        f"Temperature: {temperature:4} °C | "
        f"Distance: {result['stop_distance']:7.2f} m | "
        f"Recovered: {result['recovered_energy_kwh']:.5f} kWh | "
        f"Final SOC: {result['final_soc'] * 100:.4f}%"
    )
