FROM python:3.7
MAINTAINER xuechao <2829969299@qq.com>
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ADD app /app
ADD setup.py /setup.py
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip
RUN pip install -r /apps/requirs.txt -i https://pypi.douban.com/simple/

WORKDIR /app
# 加密py
#RUN c && rm /flask/setup.py

EXPOSE 5000
CMD gunicorn run:app -c config.py
#ENTRYPOINT celery -A tasks worker --loglevel=info
#CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]
#数据迁移
#CMD sh migrate.sh