import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

dataset_path = r"app/data/Wearable_Tech_Sleep_Stress_Dataset.csv"


def get_dataframe(path: str = dataset_path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


df = get_dataframe(dataset_path)
new_cols = []
for column in df.columns:
    new_cols.append(column.replace(" ", "_").lower())

df.columns = new_cols
df.drop(columns=["user_id"], inplace=True)
df["sleep_deviation"] = (8 - df["daily_sleep_hours"]).abs()
df = df.drop(columns=["daily_sleep_hours"])
df.dropna(axis=0, inplace=True)
df.to_csv("app/data/reSS.csv", index=False)
