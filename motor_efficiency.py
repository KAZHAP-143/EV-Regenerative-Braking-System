
def calculate_motor_efficiency(speed_kmh):
    if speed_kmh < 0:
        raise ValueError("Speed cannot be negative")
    elif speed_kmh < 10:
        return 0.55
    elif speed_kmh < 30:
        return 0.70
    elif speed_kmh < 60:
        return 0.85
    elif speed_kmh < 100:
        return 0.92
    else:
        return 0.88
