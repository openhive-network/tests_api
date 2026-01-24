#!/usr/bin/env python3

# Currently non-working arguments are commented.

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
    parser.add_argument("tag", type=str, help="Tag to organise posts")
    parser.add_argument("limit", type=int, help="How many records we want")
    # parser.add_argument("truncate_body", type = int, help = "...")
    # parser.add_argument("filter_tags", type = str, help = "Tags to filter")
    # parser.add_argument("select_authors", type = str, help = "Selected authors")
    # parser.add_argument("select_tags", type = str, help = "Selected tags")

    args = parser.parse_args()
    tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

    print(f"Test node: {args.test_node}")
    print(f"Ref node: {args.ref_node}")
    print(f"Work dir: {args.work_dir}")
    print(f"tag: {args.tag}")
    print(f"limit: {args.limit}")
    # print("truncate_body: {}".format(args.truncate_body))
    # print("filter_tags: {}".format(args.filter_tags))
    # print("select_authors: {}".format(args.select_authors))
    # print("select_tags: {}".format(args.select_tags))

    test_args = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tags_api.get_post_discussions_by_payout",
        "params": {"tag": f"{args.tag}", "limit": f"{args.limit}"},
    }
    # "truncate_body": "{}".format(args.truncate_body),
    # "filter_tags": "{}".format(args.filter_tags),
    # "select_authors": "{}".format(args.select_authors),
    # "select_tags": "{}".format(args.select_tags)

    if tester.compare_results(test_args, True):
        exit(0)
    exit(1)
