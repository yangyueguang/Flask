#!/usr/bin/env python
"""
This module named dlog means datagrand's log, It's based on  facebook tornado log.
useage:
from dlog import TNLog
logger = TNLog(path="./")
logger.info("Just for test...")
"""
from __future__ import absolute_import, division, print_function

import logging
import logging.handlers
import sys, os
import apps.config as st

from numpy import unicode

try:
    import colorama
except ImportError:
    colorama = None

try:
    import curses  # type: ignore
except ImportError:
    curses = None

def _stderr_supports_color():
    try:
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            if curses:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    return True
            elif colorama:
                if sys.stderr is getattr(colorama.initialise, 'wrapped_stderr',
                                         object()):
                    return True
    except Exception:
        # Very broad exception handling because it's always better to
        # fall back to non-colored logs than to break at startup.
        pass
    return False


class LogFormatter(logging.Formatter):
    """Log formatter used in Tornado.

    Key features of this formatter are:

    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.

    This formatter is enabled automatically by
    `tornado.options.parse_command_line` or `tornado.options.parse_config_file`
    (unless ``--logging=none`` is used).

    Color support on Windows versions that do not support ANSI color codes is
    enabled by use of the colorama__ library. Applications that wish to use
    this must first initialize colorama with a call to ``colorama.init``.
    See the colorama documentation for details.

    __ https://pypi.python.org/pypi/colorama

    .. versionchanged:: 4.5
       Added support for ``colorama``. Changed the constructor
       signature to be compatible with `logging.config.dictConfig`.
    """
    DEFAULT_FORMAT = '%(color)s[%(levelname)5.5s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT,
                 style='%', color=True, colors=DEFAULT_COLORS):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.

        .. versionchanged:: 3.2

           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt

        self._colors = {}
        if color and _stderr_supports_color():
            if curses is not None:
                fg_color = (curses.tigetstr("setaf") or
                            curses.tigetstr("setf") or "")
                if (3, 0) < sys.version_info < (3, 2, 3):
                    fg_color = unicode(fg_color, "ascii")

                for levelno, code in colors.items():
                    self._colors[levelno] = unicode(curses.tparm(fg_color, code), "ascii")
                self._normal = unicode(curses.tigetstr("sgr0"), "ascii")
            else:
                # If curses is not present (currently we'll only get here for
                # colorama on windows), assume hard-coded ANSI color codes.
                for levelno, code in colors.items():
                    self._colors[levelno] = '\033[2;3%dm' % code
                self._normal = '\033[0m'
        else:
            self._normal = ''

    def format(self, record):
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to _safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def ensure_log_file(filename, log_name="tnlog"):
    if os.path.isfile(filename): return filename
    return os.path.join(filename, log_name + ".log" if not log_name.endswith(".log") else log_name)


def Dlog(**args):
    log = args.get('logger')
    if log is None:
        log = logging.getLogger()
        log.setLevel(getattr(logging, args.get('logging', 'info').upper()))
    if args.get("filename"):
        log_file_prefix = ensure_log_file(args.get('filename'), args.get('name'))
        if args.get('rotate_mode') == 'time':
            channel = logging.handlers.TimedRotatingFileHandler(
                filename=log_file_prefix,
                when=args.get('rotate_when', 'H'),
                interval=args.get('interval', 1),
                backupCount=args.get('backupcount', 3))
        else:
            channel = logging.handlers.RotatingFileHandler(
                filename=log_file_prefix,
                maxBytes=args.get('maxbytes', 500 * 1024 * 1024),
                backupCount=args.get('backupcount') or 5)
        channel.setFormatter(LogFormatter(color=False))
        log.addHandler(channel)
    if args.get('stdout', False) or not log.handlers:
        channel = logging.StreamHandler()
        channel.setFormatter(LogFormatter())
        log.addHandler(channel)
    return log


logger = Dlog(filename=st.LOG_PATH, name='logs')
