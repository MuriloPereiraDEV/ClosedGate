from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.auth import router as auth_router
from src.core.middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)

app = FastAPI(
    title="OAuth Authentication API",
    description="""
    API de autenticação usando OAuth2 com FastAPI.
    
    ## Funcionalidades
    
    * 🔐 Autenticação completa com JWT
    * 🔄 Refresh tokens
    * 🛡️ Proteção contra ataques
    * 📝 Validação de dados
    * 🔒 Headers de segurança
    
    ## Endpoints
    
    * `/auth/register` - Registro de novos usuários
    * `/auth/login` - Login e obtenção de tokens
    * `/auth/refresh` - Atualização de tokens
    
    ## Segurança
    
    * Rate limiting (10 requisições/minuto)
    * Validação de força de senha
    * Headers de segurança HTTP
    * CORS configurável
    """,
    version="1.0.0",
    contact={
        "name": "Suporte",
        "email": "suporte@exemplo.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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