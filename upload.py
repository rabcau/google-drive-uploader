#!/usr/bin/env python
import argparse
import os
from typing import Optional

from dotenv import load_dotenv

from client import UploadClient


def get_dir(path: str) -> Optional[str]:
    dirs = [dir_ for dir_ in path.split("/") if dir_]
    if dirs:
        return dirs[-1]


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()

    parser.add_argument("source", help="Path to source dir")
    parser.add_argument("--dest", help="Google Drive dir name")
    parser.add_argument("--dest_id", help="The id of destination dir on Google Drive")
    parser.add_argument("-r", action="store_const", const=True)

    args = parser.parse_args()

    source = args.source
    dest = args.dest or get_dir(source)
    dest_id = os.getenv("DEST_ID", args.dest_id)

    client = UploadClient(source, dest, dest_id, args.r)
    client.upload_dir()
