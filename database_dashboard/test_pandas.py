import pandas as pd

df = pd.read_csv("games_march2025_cleaned.csv", nrows=0)

for i, col in enumerate(df.columns):
    print(i, repr(col))