# EV Regenerative Braking System
## Technical Documentation

### 1. Project Overview

This project develops a software-only simulation of
an electric vehicle regenerative braking system.

The simulation combines:
- Vehicle longitudinal dynamics
- Wheel rotational dynamics
- Anti-lock braking control (ABS)
- Regenerative and friction brake coordination
- Battery charging constraints
- Tire-road traction models

### 2. Vehicle Dynamics

The simulation uses a quarter-car model.

Parameters:
- Total vehicle mass: 1500 kg
- Quarter-car mass: 375 kg
- Wheel radius: 0.30 m
- Wheel rotational inertia: 1.8 kg m^2

Longitudinal vehicle dynamics:

    m * dv/dt = -F_tire

Where:
- m = quarter-car mass (kg)
- v = vehicle velocity (m/s)
- F_tire = longitudinal tire force (N)

Vehicle acceleration:

    a = -F_tire / m

Velocity integration:

    v_next = max(0, v + a * dt)

Stopping distance integration:

    x_next = x + v * dt

### 3. Wheel Rotational Dynamics

The wheel dynamics are described by:

    J * domega/dt = (F_tire - F_brake) * R

Where:
- J = wheel rotational inertia (kg m^2)
- omega = wheel angular velocity (rad/s)
- R = wheel radius (m)
- F_brake = total applied braking force (N)

Wheel angular velocity:

    omega_next = max(
        0,
        omega + ((F_tire - F_brake) * R / J) * dt
    )

### 4. Wheel Slip

During braking, wheel slip is calculated from
vehicle speed and wheel circumferential speed.

    slip = (v - R * omega) / max(v, v_reference)

The result is constrained to the range [0, 1].

A low-speed reference prevents division by zero
and stabilizes the slip calculation near rest.

The ABS controller uses wheel slip to regulate
the applied braking force.

### 5. Model Assumptions

- Straight-line braking on level ground
- Four equivalent wheels
- Equal load distribution between wheels
- No steering or lateral vehicle dynamics
- Simplified tire-road friction characteristics
- No physical hardware validation

These assumptions define the scope of the
software simulation and its limitations.
### 6. Anti-lock Braking System (ABS)

#### 6.1 Purpose

The ABS controller regulates braking force to reduce
excessive wheel slip and prevent sustained wheel lock.

The simulation supports multiple ABS control strategies
for comparative engineering analysis.

#### 6.2 Slip Feedback

The controller monitors wheel slip:

    slip = (v - R * omega) / max(v, v_reference)

Where:
- v = vehicle speed (m/s)
- omega = wheel angular speed (rad/s)
- R = wheel radius (m)
- v_reference = low-speed reference (m/s)

The calculated slip is constrained between 0 and 1.

#### 6.3 Proportional ABS Controller

A proportional controller adjusts braking based on
the difference between measured and target slip.

    error = slip - target_slip

    correction = Kp * error

Where Kp is the proportional controller gain.

Excessive slip causes a reduction in braking demand.

#### 6.4 PI ABS Controller

The PI controller includes proportional and integral
feedback to account for accumulated slip error.

    error = slip - target_slip

    integral = integral + error * dt

    correction = Kp * error + Ki * integral

Where:
- Kp = proportional gain
- Ki = integral gain
- dt = simulation time step

The implemented controller includes its own output
limiting and state-handling logic.

#### 6.5 Predictive ABS Controller

Predictive control uses an estimated future wheel-slip
condition to adjust braking before excessive slip
develops.

The prediction horizon is configurable.

This allows comparison between reactive feedback
and prediction-based braking control.

#### 6.6 Hybrid Predictive PI ABS Controller

The hybrid controller combines:
- Proportional slip feedback
- Integral slip feedback
- Prediction-based control

The reference configuration used for engineering
analysis includes:

    Kp = 60
    Ki = 10
    Prediction horizon = 0.030 s

These are simulation tuning parameters, not
production vehicle calibration values.

#### 6.7 Road-Dependent Behavior

The tire-road friction model distinguishes:
- Dry asphalt
- Wet asphalt
- Snow-covered road

Available traction and the slip associated with
peak friction vary with road conditions.

ABS performance is evaluated using:
- Stopping distance
- Stopping time
- Peak wheel slip
- Recovered regenerative energy

#### 6.8 Engineering Limitations

The ABS algorithms are evaluated using a simplified
longitudinal vehicle model.

The simulation does not establish functional-safety
compliance or real-world controller robustness.

Further validation would require calibrated models,
hardware-in-the-loop testing, and vehicle testing.
### 7. Regenerative Braking and Brake Coordination

#### 7.1 Regenerative Braking Principle

During braking, the electric motor operates as a
generator and converts mechanical energy into
electrical energy for battery charging.

Regenerative braking is limited by:
- Maximum motor regenerative force
- Battery state of charge (SOC)
- Battery temperature
- Battery charging power limit
- Wheel speed and available tire traction

#### 7.2 Braking Force Distribution

The brake coordinator receives the requested braking
force and the ABS braking factor.

    F_allowed = F_requested * ABS_factor

The regenerative braking contribution is:

    F_regen = min(F_allowed, F_regen_limit)

The remaining demand is supplied by friction brakes:

    F_friction = F_allowed - F_regen

Total commanded braking force:

    F_brake = F_regen + F_friction

This coordination prioritizes available regenerative
braking while maintaining the permitted braking demand.

#### 7.3 Reference Simulation Parameters

- Requested braking force: 2500 N per wheel
- Maximum regenerative force: 1500 N per wheel
- Maximum battery charging power: 50 kW total
- Motor efficiency: 85%
- Battery charging efficiency: 95%
- Battery capacity: 60 kWh

These values are simulation assumptions.

#### 7.4 Regenerative Power

Mechanical regenerative power per wheel is:

    P_mechanical = F_regen * R * omega

Electrical charging power is calculated using
motor and battery charging efficiencies:

    P_battery = P_mechanical * eta_motor * eta_battery

The charging power is constrained by the
battery power limit.

Recovered energy is integrated over time:

    E_recovered = integral(P_battery dt)

Energy is converted from joules to kWh.

#### 7.5 Battery Operating Constraints

The battery management logic limits regeneration
when charging conditions are unfavorable.

Examples include:
- Full battery: regenerative charging disabled
- High battery temperature: regeneration restricted
- Low battery temperature: regeneration restricted
- High SOC: charging capability reduced

When regenerative capacity decreases, friction
braking can provide the remaining permitted demand.

#### 7.6 Engineering Limitations

The battery and motor models use simplified
efficiency and charging-limit assumptions.

They do not represent a calibrated production
battery management system or motor efficiency map.
### 8. Energy Conservation and Efficiency

#### 8.1 Initial Vehicle Kinetic Energy

The initial energy includes vehicle translation
and rotation of all four wheels.

    E_trans = 0.5 * M * v^2

    E_rot = 4 * 0.5 * J * omega^2

    E_initial = E_trans + E_rot

Where:
- M = vehicle mass (1500 kg)
- v = initial vehicle speed (m/s)
- J = wheel rotational inertia (1.8 kg m^2)
- omega = initial wheel angular speed (rad/s)

At 100 km/h:

    Translational energy = 0.160751 kWh
    Rotational energy    = 0.008573 kWh
    Total initial energy = 0.169324 kWh

#### 8.2 Energy Distribution

During braking, initial kinetic energy is
distributed between:

- Energy recovered by the battery
- Tire slip dissipation
- Friction brake losses
- Motor conversion losses
- Battery charging losses

Energy conservation is evaluated using:

    E_initial = E_recovered + E_losses + E_residual

The residual quantifies numerical energy
accounting error.

#### 8.3 Reference Simulation Results

Configuration:
- Initial speed: 100 km/h
- Road condition: Wet
- Initial battery SOC: 60%
- ABS: Hybrid predictive PI
- Actuator response time: 50 ms
- Prediction horizon: 30 ms
- Adaptive brake coordination
- Enhanced tire model
- Grip-based brake initialization

Results:

    Stopping distance = 87.953 m
    Stopping time     = 6.313 s
    Recovered energy  = 0.068893 kWh
    Energy recovery   = 40.69%

The energy recovery percentage is calculated
relative to initial vehicle and wheel kinetic energy.

#### 8.4 Energy Accounting Validation

The energy conservation tests covered:
- Dry, wet, and snow road conditions
- Initial SOC values of 20%, 60%, 99%, and 100%

Reported relative energy errors:

    Dry road  = 0.002311%
    Wet road  = 0.001643%
    Snow road = 0.000752%

These values represent numerical accounting
accuracy within the simulation model.

They do not independently establish physical
model accuracy.

### 9. Software Engineering Validation

#### 9.1 Automated Testing

Stage 52 final validation results:

    Total tests    = 119
    Passed         = 119
    Failed         = 0
    Execution time = 20.566 seconds

Test coverage includes:
- ABS controller behavior
- Vehicle and wheel dynamics
- Brake coordination
- Battery charging constraints
- Energy conservation
- Numerical convergence
- Low-speed slip boundaries
- Input validation
- Simulation reproducibility

#### 9.2 Validation Scope

All automated tests passed in the Python
simulation environment.

The tests demonstrate consistency with the
implemented equations and software requirements.

They do not replace experimental validation,
hardware-in-the-loop testing, or road testing.
