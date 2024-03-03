import pytest

from tests.utils import MainProducer, assert_consumed
from worker.models import MainModel

pytestmark = pytest.mark.anyio


async def test_basic(producer: MainProducer) -> None:
    assert_consumed(await producer.send_event(MainModel(t="hello")))
