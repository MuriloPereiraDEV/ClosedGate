# OAuth Authentication API

Este projeto implementa um sistema de autenticação OAuth usando FastAPI e PostgreSQL.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Configuração do Ambiente

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
.\venv\Scripts\Activate.ps1   # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados PostgreSQL:
- Crie um banco de dados chamado `oauth_db`
- Copie o arquivo `.env.example` para `.env`
- Atualize as variáveis no arquivo `.env` conforme necessário

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

O arquivo `.env.example` contém todas as variáveis necessárias. Copie-o para `.env` e configure:

```bash
cp .env.example .env
```

As variáveis incluem:
- Configurações do banco de dados
- Chaves de segurança
- Configurações de CORS
- Configurações do ambiente

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Autor

Murilo da Silva Pereira - [GitHub](https://github.com/MuriloPereiraDEV) 
