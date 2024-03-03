FROM python:3.12-alpine AS final

WORKDIR /backend
RUN pip install --upgrade pip

RUN pip install poetry==1.8.0
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --only main

COPY ./worker ./worker

ENTRYPOINT ["python", "-m", "worker.main"]

FROM final AS watchfiles

RUN poetry install --no-interaction --no-ansi --only watchfiles

ENTRYPOINT ["watchfiles", "python -m worker.main", "/backend/worker"]

FROM final
