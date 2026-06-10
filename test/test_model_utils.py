# -*- coding: utf-8 -*-
import pytest
import pandas as pd
from model_utils import FEATURE_COLUMNS, make_inference, load_model
from sklearn.pipeline import Pipeline
from pickle import dumps


@pytest.fixture
def create_data() -> dict[str, float]:
    return {
        "NO2": 45.2,
        "NO": 12.1,
        "CO": 1.5,
        "SO2": 8.0,
        "O3": 35.0,
        "PM10": 120.0,
        "Benzene": 2.1,
        "Toluene": 5.3,
        "Xylene": 1.2,
        "NH3": 18.0,
    }


def test_make_inference(monkeypatch, create_data):
    def mock_get_predictions(_, data: pd.DataFrame) -> list[float]:
        assert list(data.columns) == FEATURE_COLUMNS
        assert create_data == data.iloc[0].to_dict()
        return [87.432]

    in_model = Pipeline([])
    monkeypatch.setattr(Pipeline, "predict", mock_get_predictions)

    result = make_inference(in_model, create_data)
    assert result == {"pm25": 87.432}


@pytest.fixture()
def filepath_and_data(tmpdir):
    p = tmpdir.mkdir("datadir").join("fakedmodel.pkl")
    example: str = "Test message!"
    p.write_binary(dumps(example))
    return str(p), example


def test_load_model(filepath_and_data):
    assert filepath_and_data[1] == load_model(filepath_and_data[0])
