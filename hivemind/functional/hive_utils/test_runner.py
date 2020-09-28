#!/usr/bin/python3
import sys

from .hivemind import *
from .hive_node import *
from .common import wait_for_string_in_file

from uuid import uuid4
from time import sleep
import logging
import os

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)-15s - %(name)s - %(levelname)s - %(message)s"
MAIN_LOG_PATH = "test_runner.log"
log_dir = os.environ.get("TEST_LOG_DIR", None)
if log_dir is not None:
    MAIN_LOG_PATH = log_dir + "/" + MAIN_LOG_PATH
else:
    MAIN_LOG_PATH = "./" + MAIN_LOG_PATH

MODULE_NAME = "test_runner"
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

class TestRunner(object):
    def __init__(self, hived_path, wif, node_url, working_dir, config_path):
        self.logger = logging.getLogger(MODULE_NAME + ".TestRunner")
        self.hived_node = None
        self.hived_node_client = None
        self.hivemind_sync = None
        self.hivemind_server = None
        self.hived_keys = [wif]

        self.hived_path = hived_path
        self.hived_wif = wif
        self.hived_node_url = node_url
        self.hived_working_dir = working_dir
        self.hived_config_path = config_path

    def on_before_hived_run(self):
        pass

    def on_before_hivemind_sync_run(self):
        pass

    def on_before_hivemind_server_run(self):
        pass

    def on_after_hivemind_server_run(self):
        from time import sleep
        sleep(60)

    def run(self):
        self.logger.info("Executing before hived run hook")
        self.on_before_hived_run()

        if self.hived_path:
            self.logger.info("Running hived via {} in {} with config {}".format(self.hived_path, 
                self.hived_working_dir, 
                self.hived_config_path)
            )
            
            self.hived_node = HiveNodeInScreen(
                self.hived_path, 
                self.hived_working_dir, 
                self.hived_config_path
            )

        if self.hived_node is not None:
            self.hived_node.run_hive_node(["--enable-stale-production"])
        try:
            if self.hived_node.is_running():
                self.hived_node_client = Hive(node = [self.hived_node_url], no_broadcast = False, 
                    keys = self.hived_keys
                )

                self.logger.info("Chain prefix is: {}".format(self.hived_node_client.prefix))
                self.logger.info("Chain ID is: {}".format(self.hived_node_client.get_config()["HIVE_CHAIN_ID"]))

                self.logger.info("Executing before hivemind initial sync run hook")
                self.on_before_hivemind_sync_run()

                self.logger.info("Start hivemind instance and perform initial sync")
                self.hivemind_sync = HivemindInScreen("hive", "sync", 8080, "postgresql://hive@localhost:5432/hive3", "/tmp")
                self.hivemind_sync.run_hivemind()
                wait_for_string_in_file(self.hivemind_sync.log_file_name, "Initial sync complete", None)
                self.logger.info("Initial sync complete, switching to live sync mode")

                self.logger.info("Executing before hivemind server run hook")
                self.on_before_hivemind_server_run()

                self.logger.info("Start hivemind instance as server")
                self.hivemind_server = HivemindInScreen("hive", "server", 8081, "postgresql://hive@localhost:5432/hive3", "/tmp")
                self.hivemind_server.run_hivemind()

                self.logger.info("Executing after hivemind server run hook")
                self.on_after_hivemind_server_run()

                self.logger.info("Stopping hived and all hivemind instances")
                if self.hivemind_server is not None:
                    self.hivemind_server.stop_hivemind()
                
                if self.hivemind_sync is not None:
                    self.hivemind_sync.stop_hivemind()

                if self.hived_node is not None:
                    self.hived_node.stop_hive_node()

                return True
            return False
        except Exception as ex:
            self.logger.exception("Exception: {}".format(ex))
            if self.hivemind_server is not None:
                self.hivemind_server.stop_hivemind()

            if self.hivemind_sync is not None:
                self.hivemind_sync.stop_hivemind()

            if self.hived_node is not None: 
                self.hived_node.stop_hive_node()
            raise ex

