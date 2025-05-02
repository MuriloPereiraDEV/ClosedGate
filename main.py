from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.v1.endpoints.auth import router as auth_router
from src.core.middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)

app = FastAPI(
    title="OAuth Authentication API",
    description="API de autenticação usando OAuth2",
    version="1.0.0"
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router) 