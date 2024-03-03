import pytest

from tests.utils import MainProducer
from worker.main import consume_requests
from worker.models import MainModel
from worker.rabbit import RabbitConsumer

pytest_plugins = ("anyio",)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def consumer() -> RabbitConsumer[MainModel]:
    return consume_requests


@pytest.fixture(scope="session")
def producer(consumer: RabbitConsumer[MainModel]) -> MainProducer:
    return MainProducer(consumer)
