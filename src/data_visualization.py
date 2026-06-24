import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data/desalination_data.csv")

plt.scatter(
    data["solar_intensity"],
    data["water_output"]
)

plt.xlabel("Solar Intensity")
plt.ylabel("Water Output")
plt.title("Solar Intensity vs Water Output")

plt.show()