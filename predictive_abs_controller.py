import math

from road_adaptive_abs_controller import (
    road_adaptive_abs_control,
    ROAD_SLIP_TARGETS,
)


def predictive_abs_control(
    slip_ratio,
    previous_slip,
    dt,
    road="dry",
    gain=60.0,
    prediction_time=0.02,
):
    """
    Experimental slip-rate-aware ABS controller.

    Predicts future slip using a constant slip-rate
    approximation and applies the existing road-adaptive
    ABS controller to the predicted slip.

    This is a simplified controller, not a validated
    vehicle safety system.
    """

    if road not in ROAD_SLIP_TARGETS:
        raise ValueError("Unsupported road condition")

    for value in (
        slip_ratio,
        previous_slip,
        dt,
        gain,
        prediction_time,
    ):
        if not math.isfinite(value):
            raise ValueError("Controller inputs must be finite")

    if dt <= 0:
        raise ValueError("Time step must be positive")

    if gain < 0:
        raise ValueError("Gain must be nonnegative")

    if prediction_time < 0:
        raise ValueError("Prediction time must be nonnegative")

    slip_rate = (slip_ratio - previous_slip) / dt

    predicted_slip = slip_ratio + slip_rate * prediction_time

    predicted_slip = max(0.0, min(1.0, predicted_slip))

    return road_adaptive_abs_control(
        slip_ratio=predicted_slip,
        road=road,
        gain=gain,
    )