import pandas as pd

data = pd.read_csv("data/desalination_data.csv")

print("\nFirst 5 Rows:")
print(data.head())

print("\nDataset Shape:")
print(data.shape)

print("\nSummary Statistics:")
print(data.describe())
