
# Workout API (FastAPI + Docker)

API mínima seguindo as instruções:

- **Query parameters** no endpoint `GET /atletas`: `nome`, `cpf`.
- **Resposta customizada** no `GET /atletas`: retorna somente `nome`, `centro_treinamento` e `categoria`.
- **Exceção de integridade (SQLAlchemy IntegrityError)** no `POST /atletas`: retorna **303** com a mensagem `Já existe um atleta cadastrado com o cpf: X`.
- **Paginação** via [`fastapi-pagination`](https://github.com/uriyyo/fastapi-pagination) usando o modelo `LimitOffsetPage` (parâmetros `limit` e `offset`).

## Rodando com Docker
```bash
docker build -t workout_api .
docker run --rm -p 8000:8000 workout_api
# ou
docker compose up --build
```

Acesse: `http://localhost:8000/docs`

## Endpoints principais

- `POST /categorias` → `{ "nome": "Profissional" }`
- `POST /centros-treinamento` → `{ "nome": "CT João Pessoa" }`
- `POST /atletas` → `{ "nome": "João", "cpf": "111.111.111-11", "categoria_id": 1, "centro_treinamento_id": 1 }`
- `GET /atletas?nome=jo&cpf=111.111.111-11&limit=10&offset=0`
- `GET /atletas/{id}`

## Observações
- Banco padrão: SQLite (`app.db`). Para outro banco, defina `DATABASE_URL` (ex.: PostgreSQL: `postgresql+psycopg2://user:pass@host/db`).
- As tabelas são criadas automaticamente no start (apenas para demo).
