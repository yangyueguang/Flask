#!/usr/bin/env python
import logging
import logging.handlers
import app.config as conf
import colorama
import threading
from logging import RootLogger


class LogFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, fmt='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def format(self, record):
        fmt = '%(color)s[%(asctime)s %(module)s.%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        color_config = {
            logging.DEBUG: colorama.Fore.BLUE,
            logging.INFO: colorama.Fore.GREEN,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.ERROR: colorama.Fore.RED
        }
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        record.color = color_config.get(record.levelno, colorama.Fore.GREEN)
        record.end_color = colorama.Fore.LIGHTGREEN_EX
        formatted = fmt % record.__dict__
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted += record.exc_text
        return formatted


class Dlog(RootLogger):
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not Dlog._instance:
            with Dlog._instance_lock:
                handler = logging.handlers.TimedRotatingFileHandler(filename=conf.LOG_PATH, when="D", backupCount=100)
                handler.suffix = "%Y-%m-%d.log"
                fmt = LogFormatter()
                handler.setFormatter(fmt)
                log = logging.getLogger()
                log.setLevel(logging.INFO)
                log.addHandler(handler)
                if conf.IS_DEBUG:
                    console = logging.StreamHandler()
                    console.setFormatter(fmt)
                    log.addHandler(console)
                Dlog._instance = log
        return Dlog._instance


logger_obj = Dlog()


def dlog(message, is_error=False, *args, **kwargs):
    if is_error:
        logger_obj.error(message, *args, **kwargs)
    else:
        logger_obj.info(message, *args, **kwargs)

