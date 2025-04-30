from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    RELOAD: bool = os.getenv("ENVIRONMENT") == "development"

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

    class Config:
        case_sensitive = True

try:
    settings = Settings()
except Exception as e:
    print("Erro ao carregar configurações:")
    print("Certifique-se de que as seguintes variáveis de ambiente estão definidas:")
    print("- DATABASE_URL")
    print("- SECRET_KEY")
    raise e 