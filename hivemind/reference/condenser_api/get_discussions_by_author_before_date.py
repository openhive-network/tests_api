#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../../../")
from testbase import SimpleJsonTest

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("test_node", type=str, help="IP address of test node")
    parser.add_argument("ref_node", type=str, help="IP address of reference node")
    parser.add_argument("work_dir", type=str, help="Work dir")
    parser.add_argument("author", type=str, help="Author we want to check")
    parser.add_argument("start_permlink", type=str, help="Start permlink")
    parser.add_argument("before_date", type=str, help="Date")
    parser.add_argument("limit", type=int, help="Posts limit")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"Ref node: {args.author}")
    print(f"Work dir: {args.start_permlink}")
    print(f"Ref node: {args.before_date}")
    print(f"Work dir: {args.limit}")

    test_args = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "condenser_api.get_discussions_by_author_before_date",
        "params": [args.author, args.start_permlink, args.before_date, args.limit],
    }

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
