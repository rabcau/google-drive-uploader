#!/usr/bin/env python
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("option", choices=("count", "auth", "process_id"))

    args = parser.parse_args()
    if args.option == "count":
        parser.add_argument("id")
        args = parser.parse_args()
    print(args)