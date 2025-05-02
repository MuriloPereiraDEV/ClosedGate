from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from src.models.user import User
from src.schemas.user import UserCreate, UserInDB, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"description": "Não autorizado"},
        400: {"description": "Requisição inválida"},
        429: {"description": "Muitas requisições"}
    }
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post(
    "/register",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um novo usuário",
    description="""
    Registra um novo usuário no sistema.
    
    Requisitos:
    - Email válido e único
    - Username único
    - Senha forte (mínimo 8 caracteres, maiúsculas, minúsculas, números e caracteres especiais)
    """,
    response_description="Usuário criado com sucesso"
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.
    
    - **email**: Email do usuário (deve ser único)
    - **username**: Nome de usuário (deve ser único)
    - **password**: Senha do usuário
    - **full_name**: Nome completo (opcional)
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post(
    "/login",
    response_model=Token,
    summary="Login de usuário",
    description="""
    Realiza o login do usuário e retorna tokens de acesso.
    
    O token de acesso expira em 30 minutos por padrão.
    O token de refresh expira em 7 dias por padrão.
    """,
    response_description="Tokens de acesso gerados com sucesso"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Realiza o login do usuário.
    
    - **username**: Nome de usuário
    - **password**: Senha do usuário
    
    Retorna:
    - access_token: Token de acesso JWT
    - refresh_token: Token de atualização JWT
    - token_type: Tipo do token (sempre "bearer")
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

@router.post(
    "/refresh",
    response_model=Token,
    summary="Atualiza tokens",
    description="""
    Atualiza os tokens de acesso usando o token de refresh.
    
    Gera um novo par de tokens (access e refresh) válidos.
    """,
    response_description="Novos tokens gerados com sucesso"
)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Atualiza os tokens de acesso.
    
    - **refresh_token**: Token de atualização JWT
    
    Retorna:
    - access_token: Novo token de acesso JWT
    - refresh_token: Novo token de atualização JWT
    - token_type: Tipo do token (sempre "bearer")
    """
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token
    }

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Middleware para obter o usuário atual a partir do token.
    
    - **token**: Token JWT de acesso
    
    Retorna:
    - User: Objeto do usuário autenticado
    
    Levanta:
    - HTTPException: Se o token for inválido ou o usuário não existir
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if not payload or payload.get("type") != "access":
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user 