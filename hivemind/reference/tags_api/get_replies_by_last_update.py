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
    parser.add_argument("start_parent_author", type=str, help="Parent author")
    parser.add_argument("start_permlink", type=str, help="Permlink")
    parser.add_argument("limit", type=int, help="Limit")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"Parent author: {args.start_parent_author}")
    print(f"Start permlink: {args.start_permlink}")
    print(f"Limit: {args.limit}")

    test_args = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tags_api.get_replies_by_last_update",
        "params": {
            "start_parent_author": f"{args.start_parent_author}",
            "start_permlink": f"{args.start_permlink}",
            "limit": f"{args.limit}",
        },
    }

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
