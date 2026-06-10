# -*- coding: utf-8 -*-
import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from model_utils import FEATURE_COLUMNS, load_model, make_inference


class Instance(BaseModel):
    NO2: Optional[float] = None
    NO: Optional[float] = None
    CO: Optional[float] = None
    SO2: Optional[float] = None
    O3: Optional[float] = None
    PM10: Optional[float] = None
    Benzene: Optional[float] = None
    Toluene: Optional[float] = None
    Xylene: Optional[float] = None
    NH3: Optional[float] = None


app = FastAPI(
    title="PM2.5 Inference Service",
    description=(
        "Synchronous inference for Delhi air quality: predict PM2.5 "
        f"from pollutant readings ({', '.join(FEATURE_COLUMNS)})."
    ),
    version="1.0.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
model_path: str = os.getenv("MODEL_PATH")
if model_path is None:
    raise ValueError("The environment variable $MODEL_PATH is empty!")


async def is_token_correct(token: str) -> bool:
    dummy_correct_token = "00000"
    return token == dummy_correct_token


async def check_token(token: str = Depends(oauth2_scheme)) -> None:
    if not await is_token_correct(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predictions")
async def predictions(
    instance: Instance,
    token: str = Depends(check_token),
) -> dict[str, float]:
    return make_inference(load_model(model_path), instance.dict())
