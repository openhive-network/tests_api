#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(__file__) + "/../../../")

import json

from testbase import SimpleJsonTest

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("test_node", type=str, help="IP address of test node")
    parser.add_argument("ref_node", type=str, help="IP address of reference node")
    parser.add_argument("work_dir", type=str, help="Work dir")
    parser.add_argument("start", type=str, help="Start object")
    parser.add_argument("limit", type=int, help="Query limit")
    parser.add_argument("order", type=str, help="")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"Start: {args.start}")
    print(f"Limit: {args.limit}")
    print(f"Order: {args.order}")

    test_args = {
        "jsonrpc": "2.0",
        "method": "database_api.list_comments",
        "params": {"start": json.loads(args.start), "limit": args.limit, "order": args.order},
        "id": 1,
    }

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
