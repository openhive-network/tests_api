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
    parser.add_argument("account", type=str, help="Account name")
    parser.add_argument("start_id", type=int, help="Starting item")
    parser.add_argument("limit", type=int, help="Limits of items to show up to 500")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"Account: {args.account}")
    print(f"Start ID: {args.start_id}")
    print(f"Limit: {args.limit}")

    test_args = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "condenser_api.get_feed_entries",
        "params": [f"{args.account}", args.start_id, args.limit],
    }

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
