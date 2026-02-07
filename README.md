# ita-api

API FastAPI com SQLAlchemy (async), migrations com Alembic e Task.

## Pré-requisitos

- Python 3.10, Pipenv, [Task](https://taskfile.dev) (`brew install go-task`)
- PostgreSQL (local ou via `docker compose up -d`)

## Comandos (Task)

Na raiz do projeto:

| Comando | Descrição |
|---------|-----------|
| `task` | Lista as tarefas disponíveis |
| `task migrate` | Aplica as migrations no banco |
| `task makemigrations -- "mensagem"` | Gera migração a partir dos modelos em `src/models/` |
| `task check` | Roda ruff check (lint) |
| `task format` | Formata o código com ruff (indent 2) |

Exemplo:

```bash
task makemigrations -- "create examples table"
task migrate
```

## Definir tabelas (models)

Os modelos ficam em **`src/models/`**:

- **`base.py`** — classe `Base` (não altere).
- **`<nome>.py`** — um arquivo por modelo (ex.: `user.py`).

Importe cada novo modelo em **`src/models/__init__.py`** para o Alembic enxergar.

Exemplo de modelo:

```python
# src/models/user.py
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
```

Em `__init__.py`: `from src.models.user import User  # noqa: F401`

## Estrutura

```
src/
  models/            # modelos (base.py, example.py, __init__.py)
  alembic/           # env.py, script.py.mako, versions/
alembic.ini
Taskfile.yml
entrypoint.sh        # migrations + uvicorn no Docker
```

## Docker

```bash
docker compose up -d
```

O container da API roda as migrations e sobe o uvicorn (veja `entrypoint.sh`).
