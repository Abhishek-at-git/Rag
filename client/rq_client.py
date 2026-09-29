import os

from redis import Redis
from rq import Queue

redis_connection = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
)
queue = Queue("rag-queue", connection=redis_connection)


def enqueue_query(query: str):
    """Queue a RAG query without importing the worker's model dependencies."""
    return queue.enqueue("rag_queue.queues.worker.process_query", query)