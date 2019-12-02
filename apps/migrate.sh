#!/usr/bin/env bash

#数据迁移
python3 run.py db init
python3 run.py db migrate
python3 run.py db upgrade
python3 run.py db downgrade