import folium
import pandas as pd
from pathlib import Path


def generate_cluster_map():
    art = Path("artifacts/visualization")
    art.mkdir(parents=True, exist_ok=True)
    (art / "run.log").write_text("Visualization started\n", encoding="utf-8")
    data_path = Path("../reports/clustered_data.csv")

    if not data_path.exists():
        print("Clustered data not found. Run notebook first.")
        return

    df = pd.read_csv(data_path)

    m = folium.Map(location=[49.8397, 24.0297], zoom_start=12)

    colors = ['red', 'blue', 'green', 'purple', 'orange']

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=4,
            color=colors[int(row['cluster'])],
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    output_path = Path("../reports/figures/cluster_map.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    m.save(output_path)

    print(f"Map saved to {output_path}")
    (art / "run.log").write_text("Map generated: cluster_map.html\n", encoding="utf-8")

if __name__ == "__main__":
    generate_cluster_map()