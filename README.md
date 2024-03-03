# xi.pochta
## Basics
### Stack
- Python 3.12
- AsyncIO
- Aio-Pika
- RabbitMQ
- Poetry
- Linters (flake8, wemake-style-guide, mypy)
- Formatters (black, autoflake)
- Pre-commit
- Pytest

### Install
```
pip install poetry==1.8.0
poetry install
pre-commit install
```

### Run (local)
```
docker compose up -d --wait
python -m worker.main
```
