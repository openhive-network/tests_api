#!/usr/bin/python3

import sys
sys.path.append("../../")
import hive_utils

from uuid import uuid4
from time import sleep
import logging
import os


LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)-15s - %(name)s - %(levelname)s - %(message)s"
MAIN_LOG_PATH = "functional_example.log"
log_dir = os.environ.get("TEST_LOG_DIR", None)
if log_dir is not None:
    MAIN_LOG_PATH = log_dir + "/" + MAIN_LOG_PATH
else:
    MAIN_LOG_PATH = "./" + MAIN_LOG_PATH


MODULE_NAME = "Functional-Example"
logger = logging.getLogger(MODULE_NAME)
logger.setLevel(LOG_LEVEL)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(LOG_LEVEL)
ch.setFormatter(logging.Formatter(LOG_FORMAT))

fh = logging.FileHandler(MAIN_LOG_PATH)
fh.setLevel(LOG_LEVEL)
fh.setFormatter(logging.Formatter(LOG_FORMAT))

if not logger.hasHandlers():
  logger.addHandler(ch)
  logger.addHandler(fh)

try:
    from beem import Hive
except Exception as ex:
    logger.error("beem library is not installed.")
    sys.exit(1)

def create_accounts(node, creator, accounts):
    """ Create accounts given as a list using `creator` as a creator account """
    for account in accounts:
        logger.info("Creating account: {}".format(account['name']))
        node.create_account(account['name'], 
            owner_key=account['public_key'], 
            active_key=account['public_key'], 
            posting_key=account['public_key'],
            memo_key=account['public_key'],
            store_keys = False,
            creator=creator,
            asset='TESTS'
        )
    hive_utils.common.wait_n_blocks(node.rpc.url, 5)


def transfer_to_vesting(node, from_account, accounts, amount, asset):
    """ Transfer assets to vesting from `from_account` to accounts given in list """
    from beem.account import Account
    for acnt in accounts:
        logger.info("Transfer to vesting from {} to {} amount {} {}".format(
            from_account, acnt['name'], amount, asset)
        )
        acc = Account(from_account, hive_instance=node)
        acc.transfer_to_vesting(amount, to = acnt['name'], asset = asset)
    hive_utils.common.wait_n_blocks(node.rpc.url, 5)


def transfer_assets_to_accounts(node, from_account, accounts, amount, asset, wif=None):
    """ Transfer assets `from_account` to accounts given in list """
    from beem.account import Account
    for acnt in accounts:
        logger.info("Transfer from {} to {} amount {} {}".format(from_account, 
            acnt['name'], amount, asset)
        )
        acc = Account(from_account, hive_instance=node)
        acc.transfer(acnt['name'], amount, asset, memo = "initial transfer")
    if wif is not None:
        hive_utils.debug_generate_blocks(node.rpc.url, wif, 5)
    else:
        hive_utils.common.wait_n_blocks(node.rpc.url, 5)


def get_permlink(account):
    """ Helper for permlink creation """
    return "functional-example-title-{}".format(account)


def create_posts(node, accounts, wif=None):
    """ Create example posts - one post for one account. Accounts given in list format """
    logger.info("Creating posts...")
    for acnt in accounts:
        logger.info("New post ==> ({},{},{},{},{})".format(
            "Hivepy example post title [{}]".format(acnt['name']), 
            "Hivepy example post body [{}]".format(acnt['name']), 
            acnt['name'], 
            get_permlink(acnt['name']), 
            "example"
        ))
        node.post("Hivepy example post title [{}]".format(acnt['name']), 
            "Hivepy example post body [{}]".format(acnt['name']), 
            acnt['name'], 
            permlink = get_permlink(acnt['name']), 
            tags = "example")
    if wif is not None:
        hive_utils.debug_generate_blocks(node.rpc.url, wif, 5)
    else:
        hive_utils.common.wait_n_blocks(node.rpc.url, 5)

def print_balance(node, accounts):
    """ Print balance for accounts given as a list """
    from beem.account import Account
    balances = []
    balances_str = []
    for acnt in accounts:
        ret = Account(acnt['name'], hive_instance=node).json()
        hbd = ret.get('hbd_balance', None)
        if hbd is not None:
            hbd = hbd.get('amount')
        balances_str.append("{}:{}".format(acnt['name'], hbd))
        balances.append(hbd)
    logger.info("Balances ==> {}".format(",".join(balances_str)))
    return balances

class HivemindFunctionalRunner(hive_utils.test_runner.TestRunner):
    def __init__(self, creator, hived_path, wif, node_url, working_dir, config_path):
        super().__init__(hived_path, wif, node_url, working_dir, config_path)
        self.creator = creator
        self.accounts = [
            # place accounts here in the format: {'name' : name, 'private_key' : private-key, 'public_key' : public-key}
            {"name" : "tester001", "private_key" : "5KQeu7SdzxT1DiUzv7jaqwkwv1V8Fi7N8NBZtHugWYXqVFH1AFa", "public_key" : "TST8VfiahQsfS1TLcnBfp4NNfdw67uWweYbbUXymbNiDXVDrzUs7J"},
            {"name" : "tester002", "private_key" : "5KgfcV9bgEen3v9mxkoGw6Rhuf2giDRZTHZjzwisjkrpF4FUh3N", "public_key" : "TST5gQPYm5bs9dRPHpqBy6dU32M8FcoKYFdF4YWEChUarc9FdYHzn"},
            {"name" : "tester003", "private_key" : "5Jz3fcrrgKMbL8ncpzTdQmdRVHdxMhi8qScoxSR3TnAFUcdyD5N", "public_key" : "TST57wy5bXyJ4Z337Bo6RbinR6NyTRJxzond5dmGsP4gZ51yN6Zom"},
            {"name" : "tester004", "private_key" : "5KcmobLVMSAVzETrZxfEGG73Zvi5SKTgJuZXtNgU3az2VK3Krye", "public_key" : "TST8dPte853xAuLMDV7PTVmiNMRwP6itMyvSmaht7J5tVczkDLa5K"},
            {"name" : "tester005", "private_key" : "5Hy4vEeYmBDvmXipe5JAFPhNwCnx7NfsfyiktBTBURn9Qt1ihcA", "public_key" : "TST7CP7FFjvG55AUeH8riYbfD8NxTTtFH32ekQV4YFXmV6gU8uAg3"}
        ]
        keys = [account["private_key"] for account in self.accounts]
        self.hived_keys.extend(keys)

    def on_before_hived_run(self):
        pass

    def on_before_hivemind_sync_run(self):
        # create accounts
        create_accounts(self.hived_node_client, self.creator, self.accounts)
        # tranfer to vesting
        transfer_to_vesting(self.hived_node_client, self.creator, self.accounts, "300.000", 
            "TESTS"
        )
        
        # transfer assets to accounts
        transfer_assets_to_accounts(self.hived_node_client, self.creator, self.accounts, 
            "400.000", "TESTS"
        )

        transfer_assets_to_accounts(self.hived_node_client, self.creator, self.accounts, 
            "400.000", "TBD"
        )

        logger.info("Balances for accounts after initial transfer")
        print_balance(self.hived_node_client, self.accounts)
        
        create_posts(self.hived_node_client, self.accounts)

    def on_before_hivemind_server_run(self):
        pass

    def on_after_hivemind_server_run(self):
        from time import sleep
        sleep(60)


if __name__ == '__main__':
    logger.info("Performing tests...")
    import argparse
    parser = argparse.ArgumentParser(description="Usage: python3 exaple.py path/to/hived/executable")
    parser.add_argument("hived_path", help = "Path to hived executable.")
    parser.add_argument("--creator", dest="creator", default="initminer", help = "Account to create test accounts with")
    parser.add_argument("--wif", dest="wif", default="5JNHfZYKGaomSFvd4NUdQ9qMcEAC43kujbfjueTHpVapX1Kzq2n", help="Private key for creator account")
    parser.add_argument("--node-url", dest="node_url", default="http://127.0.0.1:8090", help="Url of working hive node")
    parser.add_argument("--working-dir", dest="hived_working_dir", default="/tmp/hived-data/", help = "Path to hived working directory")
    parser.add_argument("--config-path", dest="hived_config_path", default="../../hive_utils/resources/config.ini.in",help = "Path to source config.ini file")

    args = parser.parse_args()

    test_runner = HivemindFunctionalRunner(args.creator, args.hived_path, args.wif, args.node_url, args.hived_working_dir, args.hived_config_path)
    test_runner.run()
