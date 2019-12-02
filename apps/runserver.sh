#!/usr/bin/env bash
export AUTHLIB_INSECURE_TRANSPORT=true
python3 tasks/requestLogs.py &
#gunicorn -w 10  run:flask_app --reload
gunicorn -w 2 -b 0.0.0.0:5001 run:app
#python3 run.py runserver -h 0.0.0.0 -p 5001 --threaded
#状态上报端口18002绑定到域名http://zz57-report.datagrand.net/