import statistics
import time

from coordinated_braking_simulation import simulate_coordinated_braking


def benchmark_road(road, repetitions=5):
    durations = []
    steps = None

    for _ in range(repetitions):
        start = time.perf_counter()

        result = simulate_coordinated_braking(
            road=road,
            initial_speed_kmh=100.0,
            initial_soc=0.60,
            abs_controller="predictive_pi",
            actuator_enabled=True,
            actuator_response_time=0.05,
            braking_mode="adaptive",
            tire_model="enhanced",
            initialization_mode="grip_based",
            prediction_time=0.030,
            pi_kp=60.0,
            pi_ki=10.0,
        )

        durations.append(time.perf_counter() - start)
        current_steps = len(result["history"]["time"])

        if steps is not None and current_steps != steps:
            raise RuntimeError("Simulation step count changed")

        steps = current_steps

    average = statistics.mean(durations)
    cost_us = average / steps * 1_000_000

    print(
        f"{road.upper():4} | "
        f"Average: {average:.4f} s | "
        f"Steps: {steps} | "
        f"Cost: {cost_us:.3f} us/step"
    )


if __name__ == "__main__":
    print("STAGE 49 - SIMULATION PERFORMANCE BENCHMARK")
    print("-" * 65)

    for road in ["dry", "wet", "snow"]:
        benchmark_road(road)
