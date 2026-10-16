
from coordinated_braking_simulation import simulate_coordinated_braking

print("ABS CONTROLLER PERFORMANCE COMPARISON")
print("-" * 75)

for controller in ["original", "proportional"]:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller=controller
    )

    print(
        f"{controller.capitalize():<15} | "
        f"Distance: {result['stop_distance']:.2f} m | "
        f"Time: {result['stop_time']:.2f} s | "
        f"Energy: {result['recovered_energy_kwh']:.4f} kWh"
    )
