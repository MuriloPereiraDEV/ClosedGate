# OAuth Authentication API

Este projeto implementa um sistema de autenticação OAuth usando FastAPI e PostgreSQL.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Configuração do Ambiente

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados PostgreSQL:
- Crie um banco de dados chamado `oauth_db`
- Atualize a URL de conexão no arquivo `.env` (se necessário)

4. Execute as migrações do banco de dados (quando implementadas):
```bash
alembic upgrade head
```

5. Execute o servidor:
```bash
uvicorn src.main:app --reload
```

## Estrutura do Projeto

```
src/
├── api/           # Endpoints da API
├── core/          # Configurações e utilitários
├── schemas/       # Schemas Pydantic
└── services/      # Lógica de negócio
```

## Documentação

A API é documentada usando Swagger UI e ReDoc:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/oauth_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Autor

[Seu Nome] - [Seu GitHub](https://github.com/seu-usuario) 