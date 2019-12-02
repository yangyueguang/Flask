# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
import datetime
import sqlalchemy as db
Base = declarative_base()


class Model(object):
    __schema__ = ModelSchema

    @classmethod
    def create(cls, **data):
        pass

    def update(self, **data):
        pass

    def jsonify(self):
        pass


class BaseModel(Base, Model):
    __abstract__ = True


class DefaultModel(BaseModel):
    __abstract__ = True
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    is_delete = db.Column(db.INTEGER, default=0)


# class LogModel(DefaultModel):
#     __tablename__ = 'logs'
#     type = db.Column(db.INTEGER, default=0)# web=0 idps=1 nlp=2 ocr=3 merge=4
#     server = db.Column(db.String(255), nullable=False)
#     code = db.Column(db.INTEGER, nullable=False, default=500)
#     message = db.Column(db.String(255))
#     statistics = db.Column(db.JSON, default={}, doc='统计信息')