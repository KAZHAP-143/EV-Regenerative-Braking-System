
from coordinated_braking_simulation import simulate_coordinated_braking

print("ACTUATOR PERFORMANCE UNDER DIFFERENT ROAD CONDITIONS")
print("-" * 100)

for road in ["dry", "wet"]:
    for actuator_enabled in [False, True]:
        result = simulate_coordinated_braking(
            road=road,
            abs_enabled=True,
            abs_controller="proportional",
            actuator_enabled=actuator_enabled,
            actuator_response_time=0.02
        )

        slips = result["history"]["slip"]
        forces = result["history"]["total_brake_force"]

        max_slip = max(slips) * 100
        high_slip_percentage = (
            100 * sum(slip > 0.20 for slip in slips) / len(slips)
        )

        max_force_change = max(
            abs(forces[i] - forces[i - 1])
            for i in range(1, len(forces))
        )

        print(
            f"Road: {road:4} | "
            f"Actuator: {'ON ' if actuator_enabled else 'OFF'} | "
            f"Distance: {result['stop_distance']:7.2f} m | "
            f"Max Slip: {max_slip:6.2f}% | "
            f"Slip >20%: {high_slip_percentage:6.2f}% | "
            f"Max Force Change: {max_force_change:7.2f} N"
        )
