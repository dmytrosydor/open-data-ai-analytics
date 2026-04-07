import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@db:5432/analytics_db")
DATA_PATH = os.getenv("DATA_PATH", "/app/data/dtp2024public.csv")


def resolve_data_path(raw_path: str) -> Path:
    candidates = [Path(raw_path), Path("/app/data/raw/dtp2024public.csv")]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "CSV file not found. Checked: " + ", ".join(str(path) for path in candidates)
    )


def main() -> None:
    data_path = resolve_data_path(DATA_PATH)
    df = pd.read_csv(data_path, on_bad_lines="skip", na_values=["null", "NULL", ""])

    engine = create_engine(DB_URL)
    df.to_sql("dtp_data", engine, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into 'dtp_data' from {data_path}")


if __name__ == "__main__":
    main()

