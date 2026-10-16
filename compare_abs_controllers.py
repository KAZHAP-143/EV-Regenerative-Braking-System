
from proportional_abs_controller import proportional_abs_control


def original_abs_control(slip):
    """Existing ABS reduction logic, for comparison."""
    if slip > 0.20:
        return 0.50
    elif slip < 0.10:
        return 1.00
    else:
        return 0.85


print(f"{'Slip':<10} {'Original ABS':<16} {'Proportional ABS'}")
print("-" * 45)

for slip in [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]:
    original = original_abs_control(slip)
    proportional = proportional_abs_control(slip)

    print(
        f"{slip * 100:5.1f}%     "
        f"{original * 100:6.1f}%          "
        f"{proportional * 100:6.1f}%"
    )
