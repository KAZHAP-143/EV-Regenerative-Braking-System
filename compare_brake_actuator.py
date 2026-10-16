
from coordinated_braking_simulation import simulate_coordinated_braking

print("BRAKE ACTUATOR RESPONSE TIME COMPARISON")
print("-" * 85)

response_times = [0.01, 0.02, 0.05, 0.10, 0.20]

for response_time in response_times:
    result = simulate_coordinated_braking(
        road="wet",
        abs_enabled=True,
        abs_controller="proportional",
        actuator_enabled=True,
        actuator_response_time=response_time
    )

    forces = result["history"]["total_brake_force"]

    slips = result["history"]["slip"]
    max_slip = max(slips) * 100

    high_slip_steps = sum(slip > 0.20 for slip in slips)
    high_slip_percentage = 100 * high_slip_steps / len(slips)



    force_changes = [
        abs(forces[i] - forces[i - 1])
        for i in range(1, len(forces))
    ]

    print(
        f"Response: {response_time * 1000:5.0f} ms | "
        f"Distance: {result['stop_distance']:6.2f} m | "
        f"Time: {result['stop_time']:5.2f} s | "
        
        f"Max Force Change: {max(force_changes):6.2f} N | "
        f"Max Slip: {max_slip:5.2f}%"

        f" | Slip >20%: {high_slip_percentage:5.2f}%"


    )
