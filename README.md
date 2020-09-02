# 这是日志数据上报系统
[接口文档](https://my.apipost.cn/doc?project_id=35275#195056)
[Flask](https://dormousehole.readthedocs.io/en/latest/)

*************
### 静态扫描
`sonar-scanner -Dproject.settings=./sonar.properties`
### 性能测试
#### 默认启动方式性能测试
Mac上执行命令安装siege, 并发测试命令。
`brew install siege`
`siege -c 10 -r 10 http://127.0.0.1:5001/demo/test`
执行结果如下
```
Transactions:		         100 hits
Availability:		      100.00 %
Elapsed time:		     1000.54 secs
Data transferred:	        0.01 MB
Response time:		       95.55 secs
Transaction rate:	        0.10 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		        9.55
Successful transactions:         100
Failed transactions:	           0
Longest transaction:	      100.09
Shortest transaction:	       10.01
```
#### 会话保持
Flask 中可以采用装饰器，在缓存redis中判定用户是否登陆或者存在, 参考代码如下：
```python
from functools import wraps
from flask import session, abort
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not 'user' in session:
            abort(401)
        return func(*args, **kwargs)
    return decorated_function
```

