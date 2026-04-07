import os
from pathlib import Path

import folium
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sqlalchemy import create_engine


matplotlib.use("Agg")

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@db:5432/analytics_db")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))
PLOTS_DIR = REPORTS_DIR / "plots"


def add_clusters(df: pd.DataFrame) -> pd.DataFrame:
    if "cluster" in df.columns:
        return df

    df = df.copy()
    df["cluster"] = pd.NA
    valid_mask = df["latitude"].notna() & df["longitude"].notna()
    valid_count = int(valid_mask.sum())
    if valid_count == 0:
        return df

    n_clusters = min(5, valid_count)
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df.loc[valid_mask, "cluster"] = model.fit_predict(
        df.loc[valid_mask, ["latitude", "longitude"]]
    )
    return df


def save_map(df: pd.DataFrame) -> Path:
    city_center = [49.8397, 24.0297]
    folium_map = folium.Map(location=city_center, zoom_start=12)
    colors = ["red", "blue", "green", "purple", "orange"]

    for _, row in df.dropna(subset=["latitude", "longitude"]).iterrows():
        cluster = int(row["cluster"]) if pd.notna(row.get("cluster")) else 0
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=colors[cluster % len(colors)],
            fill=True,
            fill_opacity=0.7,
            popup=str(row.get("mainAccidentCause", "N/A")),
        ).add_to(folium_map)

    map_path = PLOTS_DIR / "cluster_map.html"
    folium_map.save(map_path)
    return map_path


def save_cluster_histogram(df: pd.DataFrame) -> Path:
    plot_path = PLOTS_DIR / "cluster_histogram.png"

    clustered = df[df["cluster"].notna()].copy() if "cluster" in df.columns else pd.DataFrame()
    if clustered.empty:
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, "No cluster data available", ha="center", va="center")
        plt.axis("off")
    else:
        clustered["cluster"] = clustered["cluster"].astype(int)
        counts = clustered["cluster"].value_counts().sort_index()
        plt.figure(figsize=(8, 4))
        counts.plot(kind="bar", color="steelblue")
        plt.title("Accidents by Cluster")
        plt.xlabel("Cluster")
        plt.ylabel("Count")
        plt.tight_layout()

    plt.savefig(plot_path)
    plt.close()
    return plot_path


def main() -> None:
    engine = create_engine(DB_URL)
    source_table = "dtp_data_cleaned"
    df = pd.read_sql_table(source_table, engine)

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    df_clustered = add_clusters(df)
    df_clustered.to_sql("dtp_data_clustered", engine, if_exists="replace", index=False)

    map_path = save_map(df_clustered)
    histogram_path = save_cluster_histogram(df_clustered)

    print(f"Saved map to {map_path}")
    print(f"Saved histogram to {histogram_path}")


if __name__ == "__main__":
    main()

