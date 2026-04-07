# Аналіз даних ДТП у м. Львів (2024)

Проєкт перероблено на ізольовані сервіси з оркестрацією через Docker Compose.

## Нова структура

- `data_load/` — завантаження CSV у PostgreSQL (`dtp_data`)
- `data_quality_analysis/` — очищення даних, звіт `quality.json`, таблиця `dtp_data_cleaned`
- `data_research/` — базові статистики (`df.describe()`), звіт `research.json`
- `visualization/` — карта `cluster_map.html` і гістограма `cluster_histogram.png`
- `web/` — Flask-додаток для перегляду JSON-звітів і графіків
- `compose.yaml` — інтеграція сервісів, мережа, healthcheck, залежності

## Запуск

1) Створіть локальний `.env` на основі прикладу:

```powershell
Copy-Item .env.example .env
```

2) Запустіть усі сервіси:

```powershell
docker compose up --build
```

Після завершення one-shot сервісів відкрийте:

- Web dashboard: `http://localhost:5000`

## Поведінка сервісів

- `data_load`, `data_quality`, `data_research`, `visualization` — one-shot jobs.
- Для них статус `Exited (0)` після запуску є очікуваним (успішне завершення).
- Довгоживучі сервіси: `db` (healthy) і `web` (Up).

## Спільні дані

- Вхідний CSV: `data/dtp2024public.csv`
- PostgreSQL: `analytics_db`
- Спільний том звітів у контейнерах: `/app/reports`

## Вихідні артефакти

- `quality.json`
- `research.json`
- `plots/cluster_map.html`
- `plots/cluster_histogram.png`
