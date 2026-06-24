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

score = model.score(X_test, y_test)

print("Model Accuracy:", round(score * 100, 2), "%")

new_data = pd.DataFrame(
    [[42, 55, 1000, 35]],
    columns=[
        "temperature",
        "humidity",
        "solar_intensity",
        "salinity"
    ]
)

prediction = model.predict(new_data)

print(
    "Predicted Water Output:",
    round(prediction[0], 2)
)