# coding: utf-8
# @date: 2019-11-10
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
import datetime
import sqlalchemy as db

from sqlalchemy.exc import SQLAlchemyError
Base = declarative_base()

from app.utility.db import session

class Model(object):
    __schema__ = ModelSchema

    @classmethod
    def create(cls, **data):
        instance = cls(**data)
        session.add(instance)
        return instance

    def update(self, **data):
        pass

    def jsonify(self):
        pass

    def save(self):
        try:
            session.add(self)
            yield session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e




class BaseModel(Base, Model):
    __abstract__ = True


class DefaultModel(BaseModel):
    __abstract__ = True
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment="修改时间")
    is_delete = db.Column(db.BOOLEAN, default=db.true(), nullable=False)
    last_update_time = db.Column(db.DATETIME, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最近修改时间", index=True)


# class LogModel(DefaultModel):
#     __tablename__ = 'logs'
#     __table_args__ = ({"comment": "订单表"}, )
#     type = db.Column(db.INTEGER, default=0)# web=0 idps=1 nlp=2 ocr=3 merge=4
#     server = db.Column(db.String(255), nullable=False)
#     code = db.Column(db.INTEGER, nullable=False, default=500)
#     message = db.Column(db.String(255))
#     statistics = db.Column(db.JSON, default={}, doc='统计信息')