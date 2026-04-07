import json
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@db:5432/analytics_db")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "locationComments" in df.columns:
        df["locationComments"] = df["locationComments"].fillna("Коментар відсутній")

    required_cols = [col for col in ["latitude", "longitude"] if col in df.columns]
    if required_cols:
        df = df.dropna(subset=required_cols)

    return df


def main() -> None:
    engine = create_engine(DB_URL)
    df = pd.read_sql_table("dtp_data", engine)

    missing_before = {column: int(value) for column, value in df.isna().sum().items()}
    duplicates_before = int(df.duplicated().sum())
    type_profile = {column: str(dtype) for column, dtype in df.dtypes.items()}

    invalid_checks = {}
    if "accidentDate" in df.columns:
        parsed_dates = pd.to_datetime(df["accidentDate"], errors="coerce")
        invalid_checks["invalid_accidentDate"] = int(parsed_dates.isna().sum())

    if "latitude" in df.columns:
        lat = pd.to_numeric(df["latitude"], errors="coerce")
        invalid_checks["invalid_latitude"] = int((lat.isna() | ~lat.between(-90, 90)).sum())

    if "longitude" in df.columns:
        lon = pd.to_numeric(df["longitude"], errors="coerce")
        invalid_checks["invalid_longitude"] = int((lon.isna() | ~lon.between(-180, 180)).sum())

    df_clean = clean_data(df)
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)

    df_clean.to_sql("dtp_data_cleaned", engine, if_exists="replace", index=False)

    quality_report = {
        "rows_before": int(len(df)),
        "rows_after": int(len(df_clean)),
        "dropped_rows": int(len(df) - len(df_clean)),
        "duplicates_before": duplicates_before,
        "missing_values_before": missing_before,
        "type_profile": type_profile,
        "invalid_values": invalid_checks,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output = REPORTS_DIR / "quality.json"
    output.write_text(json.dumps(quality_report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved quality report to {output}")


if __name__ == "__main__":
    main()

