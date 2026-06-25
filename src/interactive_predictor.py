import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


data = pd.read_csv("data/desalination_data.csv")

X = data[
    [
        "temperature",
        "humidity",
        "solar_intensity",
        "salinity"
    ]
]

y = data["water_output"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)


print("\nAquaMind AI - Interactive Prediction System\n")

temperature = float(input("Temperature (°C): "))
humidity = float(input("Humidity (%): "))
solar_intensity = float(input("Solar Intensity (W/m²): "))
salinity = float(input("Salinity (ppt): "))

new_data = pd.DataFrame(
    [[temperature, humidity, solar_intensity, salinity]],
    columns=[
        "temperature",
        "humidity",
        "solar_intensity",
        "salinity"
    ]
)

prediction = model.predict(new_data)[0]
efficiency = (prediction / solar_intensity) * 100

print("\nPrediction Results")
print("------------------")
print("Predicted Water Output:", round(prediction, 2), "L/day")
print("Estimated Efficiency:", round(efficiency, 2), "%")
print("Model Accuracy:", round(accuracy * 100, 2), "%")

print("\nRecommendations")
print("---------------")

if solar_intensity >= 900:
    print("✓ Solar intensity is favorable for high water production.")
elif solar_intensity >= 650:
    print("⚠ Solar intensity is moderate. Water production may be limited.")
else:
    print("⚠ Low solar intensity is significantly reducing expected water output.")

if humidity > 70:
    print("⚠ High humidity may reduce evaporation efficiency.")
elif humidity >= 40:
    print("✓ Humidity is within a reasonable operating range.")
else:
    print("✓ Low humidity may support stronger evaporation.")

if salinity > 40:
    print("⚠ High salinity may reduce desalination performance.")
else:
    print("✓ Salinity is within the expected seawater range.")

if prediction >= 75:
    print("✓ Overall predicted performance is strong.")
elif prediction >= 50:
    print("⚠ Overall predicted performance is moderate.")
else:
    print("⚠ Overall predicted performance is low.")