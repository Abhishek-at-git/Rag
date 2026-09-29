import os

from redis import Redis
from rq import Queue
from rq.worker import SimpleWorker


def main() -> None:
    connection = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
    )
    queue = Queue("rag-queue", connection=connection)
    worker = SimpleWorker([queue], connection=connection)
    worker.work()


if __name__ == "__main__":
    main()
