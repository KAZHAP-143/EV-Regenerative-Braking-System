
def calculate_regen_temperature_factor(temperature_c):
    """
    Illustrative battery-temperature derating curve.

    Temperature in degrees Celsius.
    Returns regenerative braking availability from 0 to 1.
    """

    if temperature_c <= -10:
        return 0.0

    if temperature_c < 10:
        return (temperature_c + 10) / 20

    if temperature_c <= 40:
        return 1.0

    if temperature_c < 60:
        return (60 - temperature_c) / 20

    return 0.0


if __name__ == "__main__":
    for temperature in [-10, 0, 10, 25, 40, 50, 60]:
        factor = calculate_regen_temperature_factor(temperature)

        print(
            f"Temperature: {temperature:4.0f} °C | "
            f"Regen availability: {factor * 100:5.1f}%"
        )

