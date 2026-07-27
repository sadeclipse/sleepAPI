import pandas as pd

dataset_path = "data/WineQT.csv"


def get_dataframe(path: str = dataset_path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df
