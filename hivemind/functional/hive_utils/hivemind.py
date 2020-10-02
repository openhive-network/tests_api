#!/usr/bin/python3

import json
import logging
import sys
import os
import subprocess
import datetime

from .common import DEFAULT_LOG_FORMAT, DEFAULT_LOG_LEVEL

MODULE_NAME = "hivemind"

logger = logging.getLogger(MODULE_NAME)
logger.setLevel(DEFAULT_LOG_LEVEL)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(DEFAULT_LOG_LEVEL)
ch.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))

logger.addHandler(ch)

class HivemindInScreen(object):
  def __init__(self, hivemind_executable, mode, hivemind_port, database_url, working_dir = ".", hived_address="http://127.0.0.1", hived_port=8090):
    self.logger = logging.getLogger(MODULE_NAME + ".HivemindInScreen")
    self.logger.info("New hivemind instance")
    self.hivemind_executable = hivemind_executable
    assert mode in ['sync', 'server'], "Allowed modes are: `sync` and `server`"
    self.hivemind_mode = mode
    self.hivemind_port = hivemind_port
    self.hived_address = hived_address
    self.hived_port = hived_port
    self.hivemind_database_url = database_url
    self.working_dir = working_dir
    self.hivemind_running = False

  def get_address(self):
    return "http://{}:{}/".format("127.0.0.1", self.hivemind_port)

  def is_running(self):
    return self.hivemind_running

  def run_hivemind(self, params = []):
    from .common import detect_process_by_name, save_screen_cfg, save_pid_file, wait_for_string_in_file, kill_process
    from json import dumps
    start_params = [
      self.hivemind_executable,
      self.hivemind_mode,
      '--steemd-url',
      dumps({"default":"{}:{}".format(self.hived_address, self.hived_port)}),
      '--database-url',
      self.hivemind_database_url,
      '--http-server-port',
      str(self.hivemind_port)
    ]

    self.pid_file_name = "{0}/run_hivemind-{1}.pid".format(self.working_dir, self.hivemind_port)
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d")
    self.log_file_name = "{0}/{1}-{2}-{3}.log".format(self.working_dir, "hive", self.hivemind_port, current_time_str)
    screen_cfg_name = "{0}/hive_screen-{1}.cfg".format(self.working_dir, self.hivemind_port)

    start_params = start_params + params

    save_screen_cfg(screen_cfg_name, self.log_file_name)
    screen_params = [
      "screen",
      "-m",
      "-d",
      "-L",
      "-c",
      screen_cfg_name,
      "-S",
      "{0}-{1}-{2}".format("hive", self.hivemind_port, current_time_str)
    ]

    start_params = screen_params + start_params
    self.logger.info("Running hivemind with command: {0}".format(" ".join(start_params)))

    try:
      save_pid_file(self.pid_file_name, "hive", self.hivemind_port, current_time_str)
      subprocess.Popen(start_params)
      # we will allow for screen to setup and die maybe?
      from time import sleep
      sleep(5)
      # now it should be dead

      if not detect_process_by_name("hive", self.hivemind_executable, self.hivemind_port):
        msg = "{0} process is not running on {1}:{2}. Please check logs.".format("hive", "http://0.0.0.0", self.hivemind_port)
        raise ProcessLookupError(msg)

      self.hivemind_running = True
      self.logger.info("Hivemind at {0}:{1} in {2} is up and running...".format("http://0.0.0.0", self.hivemind_port, self.working_dir))
    except Exception as ex:
      self.logger.exception("Exception during hivemind run: {0}".format(ex))
      kill_process(self.pid_file_name, "hive", "http://0.0.0.0", self.hivemind_port)
      self.hivemind_running = False

  def stop_hivemind(self):
    from .common import kill_process
    self.logger.info("Stopping hivemind at {0}:{1}".format("http://0.0.0.0", self.hivemind_port))
    kill_process(self.pid_file_name, "hive", "http://0.0.0.0", self.hivemind_port)
    self.node_running = False

  def __enter__(self):
    self.run_hivemind()

  def __exit__(self, exc, value, tb):
    self.stop_hivemind()

if __name__ == "__main__":
  from time import sleep
  def main():
    hivemind = None
    try:
      hivemind = HivemindInScreen("hive", "sync", 8080, "postgresql://hive@localhost:5432/hive3", "/tmp")
      hivemind.run_hivemind()
      sleep(30)
      if hivemind is not None and hivemind.is_running():
        hivemind.stop_hivemind()
    except Exception as ex:
      if hivemind is not None and hivemind.is_running():
        hivemind.stop_hivemind()
      logger.exception("Exception: {}".format(ex))
      sys.exit(1)

  main()