import json
import os
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, send_from_directory
from sqlalchemy import create_engine, inspect


REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))
PLOTS_DIR = REPORTS_DIR / "plots"
DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@db:5432/analytics_db")

app = Flask(__name__)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"status": "missing", "path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def load_data_preview(limit: int = 20) -> dict:
    try:
        engine = create_engine(DB_URL)
        inspector = inspect(engine)
        table = "dtp_data_clustered"
        if not inspector.has_table(table):
            table = "dtp_data_cleaned" if inspector.has_table("dtp_data_cleaned") else "dtp_data"

        df = pd.read_sql_table(table, engine)
        preview = df.head(limit)
        return {
            "source_table": table,
            "columns": preview.columns.tolist(),
            "rows": preview.fillna("").to_dict(orient="records"),
            "total_rows": int(len(df)),
        }
    except Exception as exc:
        return {"error": str(exc), "source_table": None, "columns": [], "rows": [], "total_rows": 0}


@app.route("/")
def index():
    quality = load_json(REPORTS_DIR / "quality.json")
    research = load_json(REPORTS_DIR / "research.json")
    data_preview = load_data_preview()

    if PLOTS_DIR.exists():
        plots = sorted(file.name for file in PLOTS_DIR.iterdir() if file.is_file())
    else:
        plots = []

    image_plots = [name for name in plots if name.lower().endswith((".png", ".jpg", ".jpeg", ".svg"))]
    html_plots = [name for name in plots if name.lower().endswith(".html")]

    return render_template(
        "index.html",
        data_preview=data_preview,
        quality=quality,
        research=research,
        image_plots=image_plots,
        html_plots=html_plots,
    )


@app.route("/plots/<path:filename>")
def serve_plot(filename: str):
    return send_from_directory(PLOTS_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

