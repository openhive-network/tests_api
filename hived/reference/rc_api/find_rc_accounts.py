#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(__file__) + "/../../../")

import json
from testbase import SimpleJsonTest

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("test_node", type = str, help = "IP address of test node")
  parser.add_argument("ref_node", type = str, help = "IP address of reference node")
  parser.add_argument("work_dir", type = str, help = "Work dir")
  parser.add_argument("block_number", type = int, help = "Block to compare")
  parser.add_argument("accounts", help="Array of accounts")

  args = parser.parse_args()
  tester = SimpleJsonTest(args.test_node, args.ref_node, args.work_dir)

  print("Test node: {}".format(args.test_node))
  print("Ref node: {}".format(args.ref_node))
  print("Work dir: {}".format(args.work_dir))
  print("Block number: {}".format(args.block_number))

  accounts = args.accounts.split(",")

  test_args = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "rc_api.find_rc_accounts",
    "params": {
      "accounts": accounts
    }
  }

  if tester.compare_results(test_args, True):
    exit(0)
  exit(1)