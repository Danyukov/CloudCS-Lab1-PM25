# -*- coding: utf-8 -*-
"""Train and save sklearn pipeline for PM2.5 inference (Delhi)."""
import sys
from pathlib import Path
from pickle import dump

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).parent / "src"))
from model_utils import FEATURE_COLUMNS

DATA_PATH = Path("data/city_day.csv")
MODEL_PATH = Path("models/pipeline.pkl")
CITY = "Delhi"
TARGET = "PM2.5"


def build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[("numeric", numeric_transformer, FEATURE_COLUMNS)],
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", Ridge()),
        ]
    )


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    delhi = df[df["City"] == CITY].copy()
    delhi = delhi.dropna(subset=[TARGET])
    x = delhi[FEATURE_COLUMNS]
    y = delhi[TARGET]
    return x, y


def main() -> None:
    x, y = load_training_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42
    )

    param_grid = {"regressor__alpha": np.linspace(0.0, 10.0, num=41)}
    search_cv = GridSearchCV(build_pipeline(), param_grid, cv=5)
    search_cv.fit(x_train, y_train)

    y_pred = search_cv.predict(x_test)
    print(f"Best params: {search_cv.best_params_}")
    print(f"Train R2: {search_cv.score(x_train, y_train):.3f}")
    print(f"Test R2:  {search_cv.score(x_test, y_test):.3f}")
    print(f"Test MAE: {mean_absolute_error(y_test, y_pred):.2f} ug/m3")
    print(f"Test R2 (metric): {r2_score(y_test, y_pred):.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as file:
        dump(search_cv, file)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
