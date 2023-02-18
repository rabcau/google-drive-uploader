from queue import Queue
import os
from typing import Optional, Any
from concurrent.futures import ThreadPoolExecutor

from client import UploadClient


class UniqueQueue(Queue):
    def __init__(self, maxsize: int = 0):
        self.items = set()
        super().__init__(maxsize)

    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None):
        if item not in self.items:
            self.items.add(item)
            super().put(item, block, timeout)


def execute_task(client: UploadClient, q: UniqueQueue, item):
    client.upload_file(item)
    q.task_done()


def worker(client: UploadClient, q: UniqueQueue, executor: ThreadPoolExecutor):
    while True:
        item = q.get()
        executor.submit(execute_task, client, q, item)


def producer(q: Queue, source: str):
    while True:
        files = os.listdir(source)
        for file in files:
            q.put(file)
