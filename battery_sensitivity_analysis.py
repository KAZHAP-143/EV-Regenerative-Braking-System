
from vehicle_dynamics import simulate
import matplotlib.pyplot as plt

# Test different battery charge levels
soc_levels = [20, 40, 60, 80, 90, 95, 100]
soc_energy = []

for soc in soc_levels:
    result = simulate(
        mu=0.85,
        initial_speed_kmh=100,
        brake_force=4500,
        initial_soc=soc / 100,
        battery_temperature=25
    )
    soc_energy.append(result["energy_kwh"])

# Create SOC sensitivity graph
plt.figure(figsize=(9, 5))
plt.plot(soc_levels, soc_energy, marker="o")
plt.xlabel("Initial Battery SOC (%)")
plt.ylabel("Recovered Energy (kWh)")
plt.title("Effect of Battery SOC on Regenerative Braking")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "battery_soc_sensitivity.png",
    dpi=300,
    bbox_inches="tight"
)

print("SOC sensitivity results:")
for soc, energy in zip(soc_levels, soc_energy):
    print(f"{soc}% SOC: {energy:.4f} kWh")

print("SOC sensitivity graph saved successfully!")

# Battery temperature sensitivity analysis
temperatures = [-10, 0, 5, 10, 15, 25, 35, 40, 45, 50, 55]
temperature_energy = []

for temperature in temperatures:
    result = simulate(
        mu=0.85,
        initial_speed_kmh=100,
        brake_force=4500,
        initial_soc=0.60,
        battery_temperature=temperature
    )

    temperature_energy.append(result["energy_kwh"])

plt.figure(figsize=(9, 5))
plt.plot(temperatures, temperature_energy, marker="o")

plt.xlabel("Battery Temperature (°C)")
plt.ylabel("Recovered Energy (kWh)")
plt.title("Effect of Battery Temperature on Regenerative Braking")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "battery_temperature_sensitivity.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nBattery temperature sensitivity results:")

for temperature, energy in zip(temperatures, temperature_energy):
    print(f"{temperature}°C: {energy:.4f} kWh")

print("Temperature sensitivity graph saved successfully!")
