# coding: utf-8
import os
import sys
import json
import datetime
import requests
from time import sleep
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(BASE_DIR)
sys.path.append(BASE_DIR)
from apps.utility.dlog import logger
from apps.tasks.sumLogs import *
from apps import config
from apps.tasks import utils
api = Report.get_config()
logger.info(api)
report = Report()


class LogHandler(object):
    def __init__(self):
        pass

    @property
    def time_interval(self):
        return 10

    def run(self):
        while True:
            print('hello')
            sleep(2)


if __name__ == '__main__':
    logHand = LogHandler()
    logHand.run()
