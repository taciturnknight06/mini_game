"""单例模式

Desc:
    实现了一个作为元类使用的Singleton,原理是重载了__call__方法,每次调用xx()创建对象时返回单例对象

"""

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]