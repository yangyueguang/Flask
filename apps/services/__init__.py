# coding: utf-8
# @date: 2019-11-10

from flask import Blueprint
from .baseResp import *
from .upload import *
apptest = Blueprint("services", __name__)