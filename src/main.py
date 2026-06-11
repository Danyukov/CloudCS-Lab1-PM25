# -*- coding: utf-8 -*-
import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from keycloak.uma_permissions import AuthStatus
from pydantic import BaseModel

from fastapi_utils import Oauth2ClientCredentials
from keycloak_utils import get_keycloak_data
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
        "Containerized inference for Delhi air quality with Keycloak auth. "
        f"Features: {', '.join(FEATURE_COLUMNS)}."
    ),
    version="2.0.0",
)
keycloak_openid, token_endpoint = get_keycloak_data()
oauth2_scheme = Oauth2ClientCredentials(tokenUrl=token_endpoint)

model_path: str = os.getenv("MODEL_PATH")
if model_path is None:
    raise ValueError("The environment variable $MODEL_PATH is empty!")


async def get_token_status(token: str) -> AuthStatus:
    return keycloak_openid.has_uma_access(token, "infer_endpoint#doInfer")


async def check_token(token: str = Depends(oauth2_scheme)) -> None:
    auth_status = await get_token_status(token)
    if not auth_status.is_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth_status.is_authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
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
