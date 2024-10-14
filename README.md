# xi.pochta
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

### Run (docker)
The most convenient way to run the worker is to use docker for both dependencies and the app itself:
```
docker compose up --build worker
```
- Press Ctrl+C to quit
- Rerun this command after changing dependencies
- Restart is not needed after updating code files

### Run (local)
```
docker compose up -d --wait
python -m worker.main
```

#### Watchfiles
Watchfiles can be used for quick reloading of the worker:
```
docker compose up -d --wait
watchfiles "python -m worker.main" ./worker
```
- Press Ctrl+C to quit
- Rerun the second command after changing dependencies
- Restart is not needed after updating code files

Sometimes virtual environments don't work inside `watchfiles`, so you may see errors like below:
```
ModuleNotFoundError: No module named 'aio_pika'
```
In this case try specifying python's executable in the virtual environment directly, for example:
```
docker compose up -d --wait
watchfiles "venv/Scripts/python.exe -m worker.main" ./worker
```

### Dependencies
Dependencies from docker compose provide the following interfaces:
- [`http://localhost:15672`](http://localhost:15672): RabbitMQ management portal (username & password: `guest`)
