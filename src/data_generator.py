import random
import csv

with open("data/desalination_data.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "temperature",
        "humidity",
        "solar_intensity",
        "salinity",
        "water_output"
    ])

    for _ in range(1000):

        temperature = random.uniform(25, 50)
        humidity = random.uniform(20, 90)
        solar_intensity = random.uniform(400, 1200)
        salinity = random.uniform(30, 45)

        water_output = (
            solar_intensity * 0.08
            + temperature * 0.5
            - humidity * 0.3
            - salinity * 0.2
        )

        noise = random.uniform(-5, 5)
        water_output = water_output + noise

        writer.writerow([
            round(temperature, 2),
            round(humidity, 2),
            round(solar_intensity, 2),
            round(salinity, 2),
            round(water_output, 2)
        ])

print("Dataset generated successfully!")