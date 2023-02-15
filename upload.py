#!/usr/bin/env python
import argparse
import os

from dotenv import load_dotenv

from client import UploadClient


def get_dir(path: str):
    dirs = [dir_ for dir_ in path.split("/") if dir_]
    if dirs:
        return dirs[-1]


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()

    parser.add_argument("source", help="Path to source dir")
    parser.add_argument("--dest", help="Google Drive dir name")
    parser.add_argument("--dest_id", help="The id of destination dir on Google Drive")

    args = parser.parse_args()

    source = get_dir(args.source)
    dest = args.dest or source
    dest_id = os.getenv("DEST_ID", args.dest_id)

    if source:
        client = UploadClient(source, dest, dest_id)
        client.upload()
