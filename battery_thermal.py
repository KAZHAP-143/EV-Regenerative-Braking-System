
def temperature_charge_factor(temperature_c):
    """
    Simplified battery charging protection model.

    Returns a factor between 0 and 1:
    0 = regenerative charging disabled
    1 = full permitted regenerative charging
    """

    if temperature_c <= 0:
        return 0.0

    elif temperature_c < 15:
        return temperature_c / 15.0

    elif temperature_c <= 40:
        return 1.0

    elif temperature_c < 50:
        return (50.0 - temperature_c) / 10.0

    else:
        return 0.0
