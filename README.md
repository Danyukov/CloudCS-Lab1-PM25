## Лабораторная работа № 1 — Синхронный инференс PM2.5

Индивидуальный проект по дисциплине **«Облачные вычислительные системы»**.

### Задача

По суточным измерениям загрязнителей воздуха в **Delhi** предсказать концентрацию **PM2.5** (µg/m³) через REST-сервис на **FastAPI**.

### Датасет

[Air Quality Data in India](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india) — файл `data/city_day.csv`.

### Модель

`sklearn` Pipeline:

- `SimpleImputer` (median) — обработка пропусков в сырых данных;
- `StandardScaler` — масштабирование признаков;
- `Ridge` — линейная регрессия с подбором `alpha` через `GridSearchCV`.

Признаки: `NO2`, `NO`, `CO`, `SO2`, `O3`, `PM10`, `Benzene`, `Toluene`, `Xylene`, `NH3`.

### API

| Метод | Путь | Авторизация | Описание |
|-------|------|-------------|----------|
| GET | `/healthcheck` | нет | Проверка работоспособности |
| POST | `/predictions` | Bearer `00000` | Предсказание PM2.5 |

**Пример запроса:**

```bash
curl -X POST http://localhost:8000/predictions \
  -H "Authorization: Bearer 00000" \
  -H "Content-Type: application/json" \
  -d '{"NO2": 45.2, "NO": 12.1, "CO": 1.5, "SO2": 8.0, "O3": 35.0, "PM10": 120.0}'
```

**Ответ:** `{"pm25": 87.432}`

### Установка и запуск

```bash
conda create -n cloudsc-env python=3.10
conda activate cloudsc-env
pip install -r requirements.txt
```

Обучение модели:

```bash
python train_model.py
```

Тесты:

```bash
# Linux / macOS
PYTHONPATH=./:./src/ pytest test

# Windows PowerShell
$env:PYTHONPATH="./;./src/"; pytest test
```

Запуск сервиса:

```bash
cd src/
# Linux / macOS
MODEL_PATH="../models/pipeline.pkl" uvicorn main:app

# Windows PowerShell
$env:MODEL_PATH="../models/pipeline.pkl"; uvicorn main:app
```

Документация API: http://localhost:8000/docs

### Структура проекта

```
├── data/city_day.csv       # датасет
├── notebooks/              # ноутбук обучения (шаблон + pm25-delhi)
├── models/pipeline.pkl     # обученный конвейер (после train_model.py)
├── src/                    # FastAPI-сервис
├── test/                   # модульные тесты
├── train_model.py          # скрипт обучения
└── .github/workflows/      # CI
```
