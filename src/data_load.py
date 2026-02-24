import pandas as pd
from pathlib import Path


def getDataFrame(path: Path = "../data/raw/dtp2024public.csv"):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError("File not found")
    df = pd.read_csv(path)
    return df
