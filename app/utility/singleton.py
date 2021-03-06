import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


# demo
# class Foo(metaclass=SingletonType):
#     def __init__(self, name):
#         self.name = name

