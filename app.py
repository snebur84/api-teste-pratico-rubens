import dotenv
import secrets
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from database import engine, Base, SessionLocal
from config import Settings, get_settings
from controllers.controllers import router

app = FastAPI(
    title="API Meteorológica Exemplo",
    description="API de exemplo de conceitos de API RESTful com FastAPI e SQLAlchemy",
    version="1.0.0"
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key: str = Security(api_key_header),
    settings: Settings = Depends(get_settings),
):
    if not api_key or not secrets.compare_digest(api_key, settings.API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api", dependencies=[Security(verify_api_key)])