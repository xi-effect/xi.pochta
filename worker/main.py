from asyncio import new_event_loop

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from worker.config import MQ_POCHTA_QUEUE, MQ_URL
from worker.models import MainModel
from worker.rabbit import rabbit_consumer


@rabbit_consumer(MQ_POCHTA_QUEUE, MainModel)
async def consume_requests(data: MainModel) -> None:
    print(data)  # TODO  # noqa: T201 WPS421


async def main() -> AbstractRobustConnection:
    connection = await connect_robust(MQ_URL)
    await connection.connect()
    await consume_requests.run(connection)
    return connection


if __name__ == "__main__":
    main_loop = new_event_loop()
    connection = main_loop.run_until_complete(main())
    try:
        main_loop.run_forever()
    finally:
        main_loop.run_until_complete(connection.close())
