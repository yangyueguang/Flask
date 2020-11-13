import traceback
from .dlog import dlog
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor


def request(method, url, params=None, data=None, retry=1, message="", timeout=60 * 10, **kwargs):
    res = None
    while retry > 0:
        try:
            with Session() as session:
                res = session.request(method=method, url=url, params=params, data=data, timeout=timeout, **kwargs)
            if res.status_code == 200:
                break
        except Exception as e:
            dlog(e, True)
            dlog(traceback.format_exc(), True)
        finally:
            retry += 1
    if res:
        dlog(res.json())
    if not res or res.status_code != 200:
        dlog(message, True)
    return res


def get(url, params, **kwargs):
    url += '&'.join([f'{k}={v}' for k, v in params]) if params else ''
    return request('GET', url, **kwargs)


def post(url, data=None, **kwargs):
    return request('POST', url, data=data, **kwargs)


def request_all(method, url, param_list, thread=5, **kwargs):
    with ThreadPoolExecutor(thread) as executor:
        for p in param_list:
            executor.submit(request, method, url, p, **kwargs)









