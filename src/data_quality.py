import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Початкова кількість записів: {df.shape[0]}")

    df['locationComments'] = df['locationComments'].fillna('Коментар відсутній')

    df_cleaned = df.dropna(subset=['latitude', 'longitude'])

    print(f"Кількість записів після очищення: {df_cleaned.shape[0]}")
    return df_cleaned
