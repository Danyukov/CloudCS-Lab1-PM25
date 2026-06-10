# -*- coding: utf-8 -*-
import pandas as pd
from pickle import load
from sklearn.pipeline import Pipeline

FEATURE_COLUMNS = [
    "NO2",
    "NO",
    "CO",
    "SO2",
    "O3",
    "PM10",
    "Benzene",
    "Toluene",
    "Xylene",
    "NH3",
]


def make_inference(in_model: Pipeline, in_data: dict) -> dict[str, float]:
    """Return PM2.5 prediction for raw pollutant readings."""
    row = {column: in_data.get(column) for column in FEATURE_COLUMNS}
    pm25 = float(in_model.predict(pd.DataFrame([row]))[0])
    return {"pm25": round(pm25, 3)}


def load_model(path: str) -> Pipeline:
    """Return the model stored at the given path."""
    with open(path, "rb") as file:
        model: Pipeline = load(file)

    return model
