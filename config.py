from os import environ

class Config:
    WorkersCount = 4
    MaximumTasks = 11

    class Path:
        Cookie = 'data/workers/'
        Database = 'data/bmstu.db'

    class Url:
        Site = 'https://e-learning.bmstu.ru/kaluga/'
        GetCookie = 'https://proxy.bmstu.ru:8443/cas/login?service=https://e-learning.bmstu.ru/kaluga/login/index.php?authCAS=CAS'
        Login = 'https://proxy.bmstu.ru:8443/cas/login?service=https%3A%2F%2Fe-learning.bmstu.ru%2Fkaluga%2Flogin%2Findex.php%3FauthCAS%3DCAS'

    class Env:
        @staticmethod
        def GetLogin():
            return environ.get("BMSTULogin")
        @staticmethod
        def GetPassword():
            return environ.get("BMSTUPassword")

