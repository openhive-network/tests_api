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
    parser.add_argument("start_tag", type=str, help="Start tag")
    parser.add_argument("limit", type=int, help="Limit")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"Start tag: {args.start_tag}")
    print(f"Limit: {args.limit}")

    test_args = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tags_api.get_trending_tags",
        "params": {"start_tag": f"{args.start_tag}", "limit": f"{args.limit}"},
    }

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
