#!/usr/bin/env python3
"""
  Usage: __name__ jobs url1 url2 [working_dir [accounts_file]]
    Example: script_name 4 http://127.0.0.1:8090 http://127.0.0.1:8091 [get_account_history [accounts]]
    set jobs to 0 if you want use all processors
    url1 is reference url for list_accounts
"""
import sys
import json
import os
from argparse import ArgumentParser
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from jsonsocket import universal_call as hived_call
from pathlib import Path


wdir = Path()
errors = 0


def future_end_cb(future : Future):
  global errors
  exc = future.exception()
  if exc is not None or future.result() == False:
    errors += 1


def main():
  global wdir
  global errors

  arg_engine = ArgumentParser()
  arg_engine.add_argument('--ref', dest='ref_node', type=str, help='address to reference node (ex. http://127.0.0.1:8091)')
  arg_engine.add_argument('--test', dest='test_node', type=str, help='address to tested node (ex. http://127.0.0.1:8095)')
  arg_engine.add_argument('-f', dest='in_file', type=str, help='path to file with transaction hashes')
  arg_engine.add_argument('-j', dest='jobs', type=int, default=4, help='amount of threads to use')
  arg_engine.add_argument('-d', dest='wdir', type=str, default='workdir', help='path where output should be kept (ex. /path/to/workdir)')
  args = arg_engine.parse_args(list(sys.argv[1:]))

  jobs = args.jobs
  url1 = args.ref_node
  url2 = args.test_node
  wdir = Path(args.wdir)
  trx_file = args.in_file


  if trx_file != "":
    try:
      with open(trx_file, "rt") as file:
        hashes = [x.strip('\n') for x in file.readlines()]
    except:
      exit("Cannot open file: " + trx_file)

  length = len(hashes)

  if length == 0:
    exit("There are no any transaction!")

  create_wdir()

  print( str(length) + " hashes" )

  if jobs > length:
    jobs = length

  print( "setup:" )
  print( "  jobs: {}".format(jobs) )
  print( "  url1: {}".format(url1) )
  print( "  url2: {}".format(url2) )
  print( "  wdir: {}".format(wdir) )
  print( "  trx hash file: {}".format(trx_file) )

  if jobs > 1:
    first = 0
    last = length
    accounts_per_job = length // jobs

    with ProcessPoolExecutor(max_workers=jobs) as executor:
      for i in range(jobs-1):
        future = executor.submit(compare_results, url1, url2, hashes[first : first+accounts_per_job])
        future.add_done_callback(future_end_cb)
        first = first + accounts_per_job
      future = executor.submit(compare_results, url1, url2, hashes[first : last])
      future.add_done_callback(future_end_cb)
  else:
    errors = (compare_results(url1, url2, hashes) == False)

  exit( errors )


def create_wdir():
  global wdir

  if wdir.exists():
    if wdir.is_file():
      os.remove(wdir)

  if wdir.exists() == False:
    wdir.mkdir(parents=True)


def compare_results(url1, url2, transactions, max_tries=10, timeout=0.1):
  success = True
  print("Compare transactions: [{}..{}]".format(transactions[0], transactions[-1]))

  for trx in transactions:
    if get_tramsacton(url1, url2, trx, max_tries, timeout) == False:
      success = False; break

  print("Compare transactions: [{}..{}] {}".format(transactions[0], transactions[-1], "finished" if success else "break with error" ))
  return success


def get_tramsacton(url1, url2, trx : str, max_tries=10, timeout=0.1):
  global wdir
  HARD_LIMIT = 1000

  if True:
    request = {
      "jsonrpc": "2.0",
      "id": 0,
      "method": "account_history_api.get_transaction",
      "params": { "id": trx.strip(), "include_reversible": True }
      }

    with ThreadPoolExecutor(max_workers=2) as executor:
      future1 = executor.submit(hived_call, url1, data=request, max_tries=max_tries, timeout=timeout)
      future2 = executor.submit(hived_call, url2, data=request, max_tries=max_tries, timeout=timeout)

    status1, json1 = future1.result()
    status2, json2 = future2.result()

    json1 = json.loads(json1) if isinstance(json1, str) else json1
    json2 = json.loads(json2) if isinstance(json2, str) else json2

    if status1 == False or status2 == False or json1 != json2:
      print("Comparison failed for trx: {};".format(trx))

      filename1 = wdir / (trx.strip() + "_ref.json")
      filename2 = wdir / (trx.strip() + "_tested.json")

      req = json.dumps(request)
      with filename1.open("w") as file:
        file.write(f'{url1}|{req}' + '\n')
        json.dump(json1, file, indent=2, sort_keys=True, default=vars)

      with filename2.open("w") as file:
        file.write(f'{url2}|{req}' + '\n')
        json.dump(json2, file, indent=2, sort_keys=True, default=vars)

      return False

  return True


if __name__ == "__main__":
  main()
