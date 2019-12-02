# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com

from flask import Blueprint
from .baseResp import *
from .upload import *
apptest = Blueprint("services", __name__)