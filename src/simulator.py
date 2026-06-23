# AquaMind AI - Version 1 Simulator

temperature = float(input("Temperature (°C): "))            # Celsius
humidity = float(input("Humidity (%): "))                   # Percent
solar_intensity = float(input("Solar Intensity (W/m²): "))  # W/m^2
salinity = float(input("Salinity (ppt): "))                 # ppt

water_output = (
    solar_intensity * 0.08
    + temperature * 0.5
    - humidity * 0.3
    - salinity * 0.2
)

efficiency = (
    water_output / solar_intensity
) * 100

print("Water Production:", round(water_output, 2), "L/day")
print("Efficiency:", round(efficiency, 2), "%")