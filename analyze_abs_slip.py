
from coordinated_braking_simulation import simulate_coordinated_braking
import statistics

print("STAGE 29 — ABS WHEEL-SLIP ANALYSIS")
print("-" * 75)

for road in ["dry", "wet"]:
    for controller in ["original", "proportional"]:
        result = simulate_coordinated_braking(
            road=road,
            abs_enabled=True,
            abs_controller=controller,
            actuator_enabled=True,
            actuator_response_time=0.02
        )

        slips = result["history"]["slip"]

        average_slip = sum(slips) / len(slips) * 100
        target_slip = 0.15
        mean_absolute_slip_error = (
            sum(abs(slip - target_slip) for slip in slips)
            / len(slips) * 100
        )
        maximum_slip = max(slips) * 100
        slip_std = statistics.pstdev(slips) * 100

        active_slips = [
            slip for slip in slips
            if slip > 0.15
        ]
        active_slip_count = len(active_slips)
        active_slip_percentage = (
            active_slip_count / len(slips) * 100
        )

        active_slip_std = (
            statistics.pstdev(active_slips) * 100
            if len(active_slips) > 1
            else 0.0
        )

        high_slip_percentage = (
            sum(slip > 0.20 for slip in slips)
            / len(slips) * 100
        )

        print(
            f"Road: {road:3} | "
            f"ABS: {controller:12} | "
            f"Distance: {result['stop_distance']:6.2f} m | "
            f"Avg Slip: {average_slip:5.2f}% | "
            f"Max Slip: {maximum_slip:5.2f}% | "
            f"Slip >20%: {high_slip_percentage:5.2f}% | "
            f"Mean Slip Error: {mean_absolute_slip_error:5.2f}% | "
            f"Slip Std Dev: {slip_std:5.2f}%"
            f" | Active Slip Std Dev: {active_slip_std:5.2f}%"
            f" | Active Samples: {active_slip_count} ({active_slip_percentage:.2f}%)"
        )
