from typing import Any, Generic, TypeVar
from unittest.mock import AsyncMock, Mock

from aio_pika.abc import AbstractIncomingMessage
from pydantic import BaseModel

from worker.models import MainModel
from worker.rabbit import RabbitConsumer

T = TypeVar("T", bound=BaseModel)


class MessageMock(Mock):
    def __init__(self, message_body: bytes, **kwargs: Any) -> None:
        kwargs.setdefault("spec", AbstractIncomingMessage)
        super().__init__(**kwargs)
        self.body = message_body
        self.ack: AsyncMock = AsyncMock()
        self.reject: AsyncMock = AsyncMock()

    def assert_acked(self) -> None:
        self.ack.assert_called_once()

    def assert_rejected(self) -> None:
        self.reject.assert_called_once_with()


class ProducerDriver(Generic[T]):
    def __init__(self, consumer: RabbitConsumer[T]) -> None:
        self.consumer = consumer

    async def send_message(self, message_body: bytes) -> MessageMock:
        message = MessageMock(message_body)
        await self.consumer.handle_message(message)
        return message

    async def send_event(self, data: T) -> MessageMock:
        return await self.send_message(data.__pydantic_serializer__.to_json(data))


MainProducer = ProducerDriver[MainModel]


def assert_consumed(message: MessageMock, rejected: bool = False) -> None:
    if rejected:
        message.assert_rejected()
    else:
        message.assert_acked()
