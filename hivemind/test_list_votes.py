#!/usr/bin/env python3
"""
Usage: __name__ jobs url1 url2 [nr_cycles [working_dir [comments_file]]]
  Example: script_name 4 http://127.0.0.1:8090 http://127.0.0.1:8091 [20 my_comments_data_dir [comments]]
  by default: nr_cycles = 3; set nr_cycles to 0 if you want to use all comments
  set jobs to 0 if you want use all processors
  url1 is reference url for list_comments
"""

import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

from jsonsocket import hived_call
from list_comment import list_comments

wdir = Path()
errors = 0
nr_cycles = 3


def future_end_cb(future):
    global errors
    if future.result() is False:
        errors += 1


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 7:
        print("Usage: __name__ jobs url1 url2 [nr_cycles [working_dir [comments_file]]]")
        print("  Example: __name__ 4 http://127.0.0.1:8090 http://127.0.0.1:8091 [ 20 my_comments_data_dir [comments]]")
        print("  by default: nr_cycles = 3; set nr_cycles to 0 if you want to use all comments )")
        print("  set jobs to 0 if you want use all processors")
        print("  url1 is reference url for list_comments")
        exit()

    global wdir
    global errors
    global nr_cycles

    jobs = int(sys.argv[1])
    if jobs <= 0:
        import multiprocessing

        jobs = multiprocessing.cpu_count()

    url1 = sys.argv[2]
    url2 = sys.argv[3]

    if len(sys.argv) > 4:
        nr_cycles = int(sys.argv[4])

    if len(sys.argv) > 5:
        wdir = Path(sys.argv[5])

    comments_file = sys.argv[6] if len(sys.argv) > 6 else ""

    if comments_file != "":
        try:
            with open(comments_file) as file:
                comments = file.readlines()
        except OSError:
            exit("Cannot open file: " + comments_file)
    else:
        comments = list_comments(url1)

    length = len(comments)

    if length == 0:
        exit("There are no any comment!")

    create_wdir()

    print(str(length) + " comments")

    if jobs > length:
        jobs = length

    print("setup:")
    print(f"  jobs: {jobs}")
    print(f"  url1: {url1}")
    print(f"  url2: {url2}")
    print(f"  wdir: {wdir}")
    print(f"  comments_file: {comments_file}")

    if jobs > 1:
        first = 0
        last = length
        comments_per_job = length // jobs

        with ProcessPoolExecutor(max_workers=jobs) as executor:
            for _i in range(jobs - 1):
                future = executor.submit(compare_results, url1, url2, comments[first : first + comments_per_job])
                future.add_done_callback(future_end_cb)
                first = first + comments_per_job
            future = executor.submit(compare_results, url1, url2, comments[first:last])
            future.add_done_callback(future_end_cb)
    else:
        errors = compare_results(url1, url2, comments) is False

    exit(errors)


def create_wdir():
    global wdir

    if wdir.exists():
        if wdir.is_file():
            os.remove(wdir)

    if wdir.exists() is False:
        wdir.mkdir(parents=True)


def compare_results(url1, url2, comments, max_tries=10, timeout=0.1):
    success = True
    print(f"Compare comments: [{comments[0]}..{comments[ nr_cycles - 1 if nr_cycles > 0 else -1 ]}]")

    if nr_cycles > 0 and nr_cycles < len(comments):
        chosen_comments = comments[0:nr_cycles]
    else:
        chosen_comments = comments

    for comment_line in chosen_comments:
        if list_votes(url1, url2, comment_line, max_tries, timeout) is False:
            success = False
            break

    print(
        "Compare comments: [{}..{}] {}".format(
            comments[0], comments[nr_cycles - 1 if nr_cycles > 0 else -1], "finished" if success else "break with error"
        )
    )
    return success


def list_votes(url1, url2, comment_line, max_tries=10, timeout=0.1):
    global wdir
    LIMIT = 1000

    comment_array = comment_line.split(';')
    permlink = comment_array[0]
    author = comment_array[1]
    voter = ""

    print(f"PERMLINK: {permlink}, AUTHOR: {author}")

    while True:
        request = (
            bytes(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 0,
                        "method": "database_api.list_votes",
                        "params": {"start": [author, permlink, voter], "limit": LIMIT, "order": "by_comment_voter"},
                    }
                ),
                "utf-8",
            )
            + b"\r\n"
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(hived_call, url1, data=request, max_tries=max_tries, timeout=timeout)
            future2 = executor.submit(hived_call, url2, data=request, max_tries=max_tries, timeout=timeout)

        status1, json1 = future1.result()
        status2, json2 = future2.result()
        # status1, json1 = hived_call(url1, data=request, max_tries=max_tries, timeout=timeout)
        # status2, json2 = hived_call(url2, data=request, max_tries=max_tries, timeout=timeout)

        if status1 is False or status2 is False or json1 != json2:
            print(f"Comparison failed for permlink: {permlink}; author: {author}; limit: {LIMIT}")

            filename = wdir / permlink
            try:
                file = filename.open("w")
            except OSError:
                print("Cannot open file:", filename)
                return False

            file.write("Comparison failed:\n")
            file.write(f"{url1} response:\n")
            json.dump(json1, file, indent=2, sort_keys=True)
            file.write("\n")
            file.write(f"{url2} response:\n")
            json.dump(json2, file, indent=2, sort_keys=True)
            file.write("\n")
            file.close()
            return False

        votes = json1["result"]["votes"]
        votes_length = len(votes)
        if votes_length > 0:
            actual_permlink = votes[-1]["permlink"]
            actual_author = votes[-1]["author"]
            actual_voter = votes[-1]["voter"]

            if actual_permlink == permlink and actual_author == author and actual_voter == voter:
                break
            else:
                permlink = actual_permlink
                author = actual_author
                voter = actual_voter
        else:
            break

    # while True

    return True


if __name__ == "__main__":
    main()
