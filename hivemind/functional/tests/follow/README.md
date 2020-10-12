1. `psql -U postgres`
2. `create database hive_test`
3. `python3 follow.py /path/to/testnet/hived/programs/hived/hived postgresql://hive@localhost:5432/hive_test`
4. Logs in /tmp

Run example:

```
$ python3 follow.py /home/dariusz-work/Builds/hive-testnet/programs/hived/hived postgresql://hive@localhost:5432/hive4
2020-10-12 19:36:43,630 - Functional-Follow - INFO - Performing tests...
2020-10-12 19:36:43,632 - test_runner.TestRunner - INFO - Executing before hived run hook
2020-10-12 19:36:43,632 - test_runner.TestRunner - INFO - Running hived via /home/dariusz-work/Builds/hive-testnet/programs/hived/hived in /tmp/hived-data/ with config ../../hive_utils/resources/config.ini.in
2020-10-12 19:36:43,632 - hive_node.HiveNodeInScreen - INFO - New hive node
2020-10-12 19:36:43,645 - hive_node.HiveNodeInScreen - INFO - *** START NODE at http://127.0.0.1:8090 in /tmp/hived-data/
2020-10-12 19:36:43,645 - hive_node.HiveNodeInScreen - INFO - Running hived with command: screen -m -d -L -c /tmp/hived-data//hive_screen-8090.cfg -S hived-8090-2020-10-12 /home/dariusz-work/Builds/hive-testnet/programs/hived/hived -d /tmp/hived-data/ --advanced-benchmark --sps-remove-threshold -1 --enable-stale-production
2020-10-12 19:37:03,706 - hive_node.HiveNodeInScreen - INFO - Node at http://127.0.0.1:8090 in /tmp/hived-data/ is up and running...
2020-10-12 19:37:04,320 - test_runner.TestRunner - INFO - Chain prefix is: TST
2020-10-12 19:37:04,320 - test_runner.TestRunner - INFO - Chain ID is: 18dcf0a285365fc58b71f18b3d3fec954aa0c141c44e4e5cb4cf777b9eab274e
2020-10-12 19:37:04,320 - test_runner.TestRunner - INFO - Executing before hivemind initial sync run hook
2020-10-12 19:37:04,320 - Functional-Follow - INFO - Creating account: tester001
2020-10-12 19:37:04,482 - Functional-Follow - INFO - Creating account: tester002
2020-10-12 19:37:04,613 - Functional-Follow - INFO - Creating account: tester003
2020-10-12 19:37:04,684 - Functional-Follow - INFO - Creating account: tester004
2020-10-12 19:37:04,755 - Functional-Follow - INFO - Creating account: tester005
2020-10-12 19:37:18,925 - Functional-Follow - INFO - Transfer to vesting from initminer to tester001 amount 300.000 TESTS
2020-10-12 19:37:19,063 - Functional-Follow - INFO - Transfer to vesting from initminer to tester002 amount 300.000 TESTS
2020-10-12 19:37:19,144 - Functional-Follow - INFO - Transfer to vesting from initminer to tester003 amount 300.000 TESTS
2020-10-12 19:37:19,224 - Functional-Follow - INFO - Transfer to vesting from initminer to tester004 amount 300.000 TESTS
2020-10-12 19:37:19,356 - Functional-Follow - INFO - Transfer to vesting from initminer to tester005 amount 300.000 TESTS
2020-10-12 19:37:34,528 - Functional-Follow - INFO - Transfer from initminer to tester001 amount 400.000 TESTS
2020-10-12 19:37:34,598 - Functional-Follow - INFO - Transfer from initminer to tester002 amount 400.000 TESTS
2020-10-12 19:37:34,669 - Functional-Follow - INFO - Transfer from initminer to tester003 amount 400.000 TESTS
2020-10-12 19:37:34,750 - Functional-Follow - INFO - Transfer from initminer to tester004 amount 400.000 TESTS
2020-10-12 19:37:34,882 - Functional-Follow - INFO - Transfer from initminer to tester005 amount 400.000 TESTS
2020-10-12 19:37:48,991 - Functional-Follow - INFO - Transfer from initminer to tester001 amount 400.000 TBD
2020-10-12 19:37:49,123 - Functional-Follow - INFO - Transfer from initminer to tester002 amount 400.000 TBD
2020-10-12 19:37:49,255 - Functional-Follow - INFO - Transfer from initminer to tester003 amount 400.000 TBD
2020-10-12 19:37:49,336 - Functional-Follow - INFO - Transfer from initminer to tester004 amount 400.000 TBD
2020-10-12 19:37:49,417 - Functional-Follow - INFO - Transfer from initminer to tester005 amount 400.000 TBD
2020-10-12 19:38:04,539 - Functional-Follow - INFO - Balances for accounts after initial transfer
2020-10-12 19:38:04,549 - Functional-Follow - INFO - Balances ==> tester001:400000,tester002:400000,tester003:400000,tester004:400000,tester005:400000
2020-10-12 19:38:04,549 - Functional-Follow - INFO - Creating posts...
2020-10-12 19:38:04,549 - Functional-Follow - INFO - New post ==> (Hivepy example post title [tester001],Hivepy example post body [tester001],tester001,functional-example-title-tester001,example)
2020-10-12 19:38:04,627 - Functional-Follow - INFO - New post ==> (Hivepy example post title [tester002],Hivepy example post body [tester002],tester002,functional-example-title-tester002,example)
2020-10-12 19:38:04,759 - Functional-Follow - INFO - New post ==> (Hivepy example post title [tester003],Hivepy example post body [tester003],tester003,functional-example-title-tester003,example)
2020-10-12 19:38:04,840 - Functional-Follow - INFO - New post ==> (Hivepy example post title [tester004],Hivepy example post body [tester004],tester004,functional-example-title-tester004,example)
2020-10-12 19:38:04,971 - Functional-Follow - INFO - New post ==> (Hivepy example post title [tester005],Hivepy example post body [tester005],tester005,functional-example-title-tester005,example)
2020-10-12 19:38:49,178 - test_runner.TestRunner - INFO - Start hivemind instance and perform initial sync
2020-10-12 19:38:49,178 - hivemind.HivemindInScreen - INFO - New hivemind instance
2020-10-12 19:38:49,178 - hivemind.HivemindInScreen - INFO - Running hivemind with command: screen -m -d -L -c /tmp/hive_screen-8080.cfg -S hive-8080-2020-10-12 hive sync --steemd-url {"default": "http://127.0.0.1:8090"} --database-url postgresql://hive@localhost:5432/hive4 --http-server-port 8080
2020-10-12 19:38:54,196 - hivemind.HivemindInScreen - INFO - Hivemind at http://0.0.0.0:8080 in /tmp is up and running...
2020-10-12 19:38:54,197 - common - INFO - Waiting for string "Initial sync complete" in file /tmp/hive-8080-2020-10-12.log
2020-10-12 19:38:55,198 - test_runner.TestRunner - INFO - Initial sync complete, switching to live sync mode
2020-10-12 19:38:55,198 - test_runner.TestRunner - INFO - Executing before hivemind server run hook
2020-10-12 19:38:55,198 - test_runner.TestRunner - INFO - Start hivemind instance as server
2020-10-12 19:38:55,198 - hivemind.HivemindInScreen - INFO - New hivemind instance
2020-10-12 19:38:55,198 - hivemind.HivemindInScreen - INFO - Running hivemind with command: screen -m -d -L -c /tmp/hive_screen-8081.cfg -S hive-8081-2020-10-12 hive server --steemd-url {"default": "http://127.0.0.1:8090"} --database-url postgresql://hive@localhost:5432/hive4 --http-server-port 8081
2020-10-12 19:39:00,212 - hivemind.HivemindInScreen - INFO - Hivemind at http://0.0.0.0:8081 in /tmp is up and running...
2020-10-12 19:39:00,212 - test_runner.TestRunner - INFO - Executing after hivemind server run hook
2020-10-12 19:39:30,360 - test_runner.TestRunner - INFO - Stopping hived and all hivemind instances
2020-10-12 19:39:30,360 - hivemind.HivemindInScreen - INFO - Stopping hivemind at http://0.0.0.0:8081
2020-10-12 19:39:30,360 - common - INFO - Terminating hive process running on port 8081
2020-10-12 19:39:30,381 - common - INFO - Done...
2020-10-12 19:39:30,381 - hivemind.HivemindInScreen - INFO - Stopping hivemind at http://0.0.0.0:8080
2020-10-12 19:39:30,381 - common - INFO - Terminating hive process running on port 8080
2020-10-12 19:39:30,403 - common - INFO - Done...
2020-10-12 19:39:30,403 - hive_node.HiveNodeInScreen - INFO - Stopping node at http://127.0.0.1:8090
2020-10-12 19:39:30,403 - common - INFO - Terminating hived process running on port 8090
2020-10-12 19:39:30,427 - common - INFO - Done...

```