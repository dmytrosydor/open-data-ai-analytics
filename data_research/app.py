import json
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect


DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@db:5432/analytics_db")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))


def replace_nan(value):
    if isinstance(value, float) and pd.isna(value):
        return None
    return value


def normalize_nested(data):
    if isinstance(data, dict):
        return {k: normalize_nested(v) for k, v in data.items()}
    return replace_nan(data)


def main() -> None:
    engine = create_engine(DB_URL)
    inspector = inspect(engine)

    source_table = "dtp_data_cleaned" if inspector.has_table("dtp_data_cleaned") else "dtp_data"
    df = pd.read_sql_table(source_table, engine)

    describe_dict = normalize_nested(df.describe(include="all").to_dict())

    research_report = {
        "source_table": source_table,
        "rows": int(len(df)),
        "columns": df.columns.tolist(),
        "describe": describe_dict,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output = REPORTS_DIR / "research.json"
    output.write_text(json.dumps(research_report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved research report to {output}")


if __name__ == "__main__":
    main()

