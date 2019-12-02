# coding: utf-8
# @date: 2019-11-10
# @author: xuechao@datagrand.com

from sqlalchemy.util._collections import AbstractKeyedTuple
import datetime
import decimal


# 数据库返回数据列表 转 dict
def db_datalist_to_dict(res_obj, Model):
    if not res_obj:
        return None
    if isinstance(res_obj, list):  # 列表解析
        if len(res_obj) == 0:
            return None
        if isinstance(res_obj[0], AbstractKeyedTuple):  #
            dic_list = datalist_format([dict(zip(result.keys(), result)) for result in res_obj])
            if dic_list:
                for item in dic_list:
                    for key in item.keys():
                        if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                            item[key] = str(item[key])
            return dic_list
        elif isinstance(res_obj[0], Model):
            [item.__dict__.pop("_sa_instance_state") for item in res_obj]
            return datalist_format([item.__dict__ for item in res_obj])
        elif isinstance(res_obj[0], dict):  # 在db中存在json字段时返回的是dict
            return datalist_format(res_obj)
        else:
            return None
    else:
        return db_data_to_dict(res_obj, Model)


# 数据库返回单个数据 转 dict
def db_data_to_dict(res_obj, Model):
    if not res_obj:
        return None
    if isinstance(res_obj, dict):
        return res_obj
    elif isinstance(res_obj, AbstractKeyedTuple):
        # 转成字典
        dict_obj = data_format(dict(zip(res_obj.keys(), res_obj)))
        # 把null 转空字符串
        if res_obj and len(res_obj.keys()) > 0:
            for key in res_obj.keys():
                if not dict_obj[key]:
                    dict_obj[key] = ""
                if key.find("Id") >= 0 or key.find("uuid") >= 0 or key.find("_id") >= 0:
                    dict_obj[key] = str(dict_obj[key])

        return dict_obj
    elif isinstance(res_obj, Model):
        res_obj.__dict__.pop("_sa_instance_state")
        return data_format(res_obj.__dict__)
    else:
        return None


def datalist_format(reslist):
    """
    列表 中 时间格式datetime.datetime  转 [2018:12:12 10:10:56]
    """
    if not reslist or not isinstance(reslist, list):
        return reslist
    for item in reslist:
        for key in item.keys():
            if isinstance(item[key], datetime.datetime) \
                    or isinstance(item[key], datetime.date):
                item[key] = str(item[key])
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
    return reslist


def data_format(bean: dict):
    """
    对象 中 时间格式datetime.datetime  转 [2018:12:12 10:10:56]
    """
    if not bean or not isinstance(bean, dict):
        return bean
    for key in bean.keys():
        if isinstance(bean[key], datetime.datetime) or isinstance(bean[key], datetime.date):
            bean[key] = str(bean[key])
        if isinstance(bean[key], decimal.Decimal):
            bean[key] = float(bean[key])
    return bean
