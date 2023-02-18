#!/usr/bin/env python
import argparse
import os
import time
import threading
from dataclasses import dataclass
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

import queue_
from client import UploadClient


def get_dir(path: str) -> Optional[str]:
    dirs = [dir_ for dir_ in path.split("/") if dir_]
    if dirs:
        return dirs[-1]


@dataclass(frozen=True)
class Mode:
    manual = "manual"
    queue = "queue"
    service = "service"


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=("manual", "queue", "service"))
    parser.add_argument("source", help="Path to source dir")
    parser.add_argument("--dest", help="Google Drive dir name")
    parser.add_argument("--dest_id", help="The id of destination dir on Google Drive")
    parser.add_argument(
        "-r", action="store_const", const=True, help="Remove files after upload"
    )

    args = parser.parse_args()

    mode = args.mode
    source = args.source
    dest = args.dest or get_dir(source)
    dest_id = os.getenv("DEST_ID", args.dest_id)

    client = UploadClient(source, dest, dest_id, args.r)

    print(f"[{time.asctime()}] Starting in {mode} mode.")
    try:
        if mode == Mode.manual:
            client.upload_dir()
        elif mode == Mode.queue:
            queue = queue_.UniqueQueue()
            with ThreadPoolExecutor() as executor:
                threading.Thread(
                    target=queue_.worker, args=(client, queue, executor)
                ).start()
                queue_.producer(queue, source)
        print(f"[{time.asctime()}] The script has finished.")
    except KeyboardInterrupt:
        print(f"[{time.asctime()}] The script has been stopped manually.")
    except Exception as exc:
        print(f"[{time.asctime()}] The script has failed to finish. The reason - {exc}")
