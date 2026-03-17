import folium
import pandas as pd
from pathlib import Path
from data_load import getDataFrame
from data_quality import clean_data


def generate_cluster_map(df):
    # Використовуємо шляхи відносно кореня проекту, а не ../
    art = Path("artifacts/visualization")
    art.mkdir(parents=True, exist_ok=True)
    (art / "run.log").write_text("Visualization started\n", encoding="utf-8")

    # Видалено перевірку data_path.exists() та pd.read_csv(data_path),
    # оскільки ми використовуємо очищений 'df', переданий у функцію.

    # Перевірка наявності необхідних колонок для фоліума
    if "latitude" not in df.columns or "longitude" not in df.columns:
        print("Error: Latitude/Longitude columns missing.")
        return

    m = folium.Map(location=[49.8397, 24.0297], zoom_start=12)

    # Додано перевірку наявності колонки 'cluster'
    if "cluster" in df.columns:
        colors = ["red", "blue", "green", "purple", "orange"]
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=4,
                color=colors[int(row["cluster"]) % len(colors)],
                fill=True,
                fill_opacity=0.7,
            ).add_to(m)
    else:
        # Якщо кластерів ще немає, просто малюємо точки одним кольором
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]], radius=4, color="blue"
            ).add_to(m)

    # Зберігаємо у папку reports у корені проекту
    output_path = Path("reports/figures/cluster_map.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    m.save(output_path)

    print(f"Map saved to {output_path}")
    with open(art / "run.log", "a", encoding="utf-8") as f:
        f.write("Map generated: cluster_map.html\n")


if __name__ == "__main__":
    data_path = "../data/dtp2024public.csv"
    df_raw = getDataFrame(data_path)

    # 2. Очищення
    df = clean_data(df_raw)

    # 3. Візуалізація
    generate_cluster_map(df)