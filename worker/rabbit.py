import logging
from collections.abc import Callable
from typing import Generic, Protocol, TypeVar

from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel, contravariant=True)


class EventHandler(Protocol[T]):
    async def __call__(self, data: T) -> None:
        pass


class RabbitConsumer(Generic[T]):
    def __init__(
        self, queue_name: str, model: type[T], handler: EventHandler[T]
    ) -> None:
        self.queue_name = queue_name
        self.model = model
        self.handler = handler

    async def handle_message(self, message: AbstractIncomingMessage) -> None:
        logging.debug("New message", extra={"original_message": message})

        try:
            validated = self.model.model_validate_json(message.body)
        except ValidationError as validation_exc:
            await message.reject()
            await self.handler(validated)
            logging.error(
                "Unparsable payload",
                exc_info=validation_exc,
                extra={"original_message": message},
            )
            return

        try:
            await self.handler(validated)
        except Exception as handling_exc:  # noqa: PIE786
            await message.reject()
            logging.error(
                "Error while handling event",
                exc_info=handling_exc,
                extra={"original_message": message},
            )
            return
        await message.ack()

    async def run(self, connection: AbstractConnection) -> None:
        channel: AbstractChannel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue: AbstractQueue = await channel.declare_queue(self.queue_name)
        await queue.consume(self.handle_message)


def rabbit_consumer(
    queue_name: str, model: type[T]
) -> Callable[[EventHandler[T]], RabbitConsumer[T]]:
    def rabbit_consumer_wrapper(function: EventHandler[T]) -> RabbitConsumer[T]:
        return RabbitConsumer(queue_name=queue_name, model=model, handler=function)

    return rabbit_consumer_wrapper
