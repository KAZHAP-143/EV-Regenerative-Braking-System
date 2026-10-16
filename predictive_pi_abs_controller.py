from predictive_abs_controller import predictive_abs_control
from pi_abs_controller import pi_abs_control


def predictive_pi_abs_control(
    slip_ratio,
    previous_slip,
    integral_error,
    dt,
    road="dry",
    kp=60.0,
    ki=10.0,
    prediction_time=0.015,
):
    # Predictive braking command
    predictive_factor = predictive_abs_control(
        slip_ratio=slip_ratio,
        previous_slip=previous_slip,
        dt=dt,
        road=road,
        gain=kp,
        prediction_time=prediction_time,
    )

    # PI braking command
    pi_factor, integral_error = pi_abs_control(
        slip_ratio=slip_ratio,
        integral_error=integral_error,
        dt=dt,
        road=road,
        kp=kp,
        ki=ki,
    )

    # Select the more conservative braking command
    braking_factor = min(predictive_factor, pi_factor)

    return braking_factor, integral_error