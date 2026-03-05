import pandas as pd
from pathlib import Path


def getDataFrame(path:Path = "../data/raw/dtp2024public.csv" ):
    path = Path(path, sep = ";", on_bad_lines = "skip")
    if not path.exists():
        raise FileNotFoundError("File not found")
    df = pd.read_csv(
        path,
        sep=";",
        engine="python",
        na_values=["null"]
    )
    return df
