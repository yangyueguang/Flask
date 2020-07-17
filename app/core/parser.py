# coding: utf-8
# @date: 2019-11-10

from flask_restful import abort as original_abort
from webargs.flaskparser import FlaskParser as OriginalFlaskParser


def bind(**kwargs):
    def wrapper(func):
        for key, val in kwargs.items():
            if getattr(func, key, None):
                raise RuntimeError()
            setattr(func, key, val)
        return func
    return wrapper


class Parser(OriginalFlaskParser):
    def handle_invalid_json_error(self, error, req, *args, **kwargs):
        abort(422, message={"json": ["Invalid JSON body."]})


def parse_error(e, *args, **kwargs):
    abort(422, message=getattr(e, 'message', str(e)))


def abort(*args, **kwargs):
    original_abort(*args, **kwargs)


parser = Parser(error_handler=parse_error)
parse = parser.use_args
