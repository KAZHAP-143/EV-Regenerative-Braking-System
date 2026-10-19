from coordinated_braking_simulation import simulate_coordinated_braking

BASELINE = {
    "road": "wet",
    "initial_speed_kmh": 100.0,
    "initial_soc": 0.60,
    "abs_controller": "predictive_pi",
    "actuator_enabled": True,
    "actuator_response_time": 0.05,
    "braking_mode": "adaptive",
    "tire_model": "enhanced",
    "initialization_mode": "grip_based",
    "prediction_time": 0.030,
    "pi_kp": 60.0,
    "pi_ki": 10.0,
}

EXPERIMENTS = {
    "Proportional gain (Kp)": ("pi_kp", [40.0, 60.0, 80.0]),
    "Integral gain (Ki)": ("pi_ki", [0.0, 10.0, 30.0]),
    "Prediction horizon (s)": ("prediction_time", [0.010, 0.030, 0.050]),
    "Actuator response (s)": ("actuator_response_time", [0.020, 0.050, 0.100]),
    "Road condition": ("road", ["dry", "wet", "snow"]),
}


def main():
    print("STAGE 51 - PARAMETER SENSITIVITY ANALYSIS")

    for title, (parameter, values) in EXPERIMENTS.items():
        print(f"\n{title}")
        print("-" * 85)

        for value in values:
            settings = BASELINE.copy()
            settings[parameter] = value

            result = simulate_coordinated_braking(**settings)

            print(
                f"{parameter}={str(value):>6} | "
                f"Distance={result['stop_distance']:.3f} m | "
                f"Time={result['stop_time']:.3f} s | "
                f"Energy={result['recovered_energy_kwh']:.6f} kWh"
            )


if __name__ == "__main__":
    main()
