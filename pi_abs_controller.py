import math

from road_adaptive_abs_controller import ROAD_SLIP_TARGETS


def pi_abs_control(
    slip_ratio,
    integral_error,
    dt,
    road="dry",
    kp=60.0,
    ki=10.0,
):
    """
    Experimental PI ABS controller.

    Returns:
        braking_factor: value between 0 and 1
        integral_error: updated integral state
    """

    if road not in ROAD_SLIP_TARGETS:
        raise ValueError("Unsupported road condition")

    for value in (slip_ratio, integral_error, dt, kp, ki):
        if not math.isfinite(value):
            raise ValueError("Inputs must be finite")

    if not 0.0 <= slip_ratio <= 1.0:
        raise ValueError("Slip ratio must be between 0 and 1")

    if dt <= 0:
        raise ValueError("Time step must be positive")

    if kp < 0 or ki < 0:
        raise ValueError("Controller gains must be nonnegative")

    target_slip = ROAD_SLIP_TARGETS[road]

    error = slip_ratio - target_slip

       # Calculate candidate integral state
    candidate_integral = integral_error + error * dt

    # Calculate braking command before saturation
    candidate_factor = (
        1.0
        - kp * error
        - ki * candidate_integral
    )

    # Conditional integration anti-windup
    if candidate_factor > 1.0 and error < 0:
        pass  # Prevent upper-limit windup
    elif candidate_factor < 0.0 and error > 0:
        pass  # Prevent lower-limit windup
    else:
        integral_error = candidate_integral

    # Bound integral state
    integral_error = max(-1.0, min(1.0, integral_error))

    # Calculate final braking factor
    braking_factor = 1.0 - kp * error - ki * integral_error
    braking_factor = max(0.0, min(1.0, braking_factor))

    return braking_factor, integral_error