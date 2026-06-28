import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def train_model():
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

    return model, accuracy


def predict_water_output(
    model,
    temperature,
    humidity,
    solar_intensity,
    salinity
):
    new_data = pd.DataFrame(
        [[temperature, humidity, solar_intensity, salinity]],
        columns=[
            "temperature",
            "humidity",
            "solar_intensity",
            "salinity"
        ]
    )

    prediction = model.predict(new_data)

    return prediction[0]


def get_system_status(prediction):

    if prediction >= 90:
        return "High Production Potential", "success"

    elif prediction >= 60:
        return "Moderate Production Potential", "warning"

    else:
        return "Low Production Potential", "error"