
def calculate_regen_soc_factor(soc):
    """
    Calculate regenerative braking availability
    based on battery state of charge.

    SOC is represented as a fraction from 0 to 1.

    Full regeneration is available up to 90% SOC.
    Regeneration decreases linearly between 90% and 100%.
    """

    if not 0.0 <= soc <= 1.0:
        raise ValueError("SOC must be between 0 and 1")

    if soc <= 0.90:
        return 1.0

    if soc >= 1.0:
        return 0.0

    return (1.0 - soc) / 0.10


if __name__ == "__main__":
    for soc in [0.60, 0.90, 0.95, 0.98, 1.00]:
        factor = calculate_regen_soc_factor(soc)

        print(
            f"Battery SOC: {soc * 100:.0f}% | "
            f"Regenerative braking availability: {factor * 100:.1f}%"
        )
