import pandas as pd
from pathlib import Path

def getDataFrame(path: str = "https://opendata.city-adm.lviv.ua/dataset/d07c92fd-dbd9-436a-ac00-8d455c438eb6/resource/377dacf2-e372-4b89-91a8-1911e21e26c3/download/dtp2024public.csv"):
    # Перевіряємо, чи це посилання, чи локальний шлях
    if path.startswith("http"):
        print(f"Завантаження даних з URL: {path}")
        df = pd.read_csv(
            path,
            sep=";",
            engine="python",
            on_bad_lines="skip",
            na_values=["null"],
            storage_options={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        )
    else:
        local_path = Path(path)
        if not local_path.exists():
            raise FileNotFoundError(f"Файл не знайдено за шляхом: {local_path}")
        df = pd.read_csv(
            local_path
        )
    return df