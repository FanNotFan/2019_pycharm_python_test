# 自定义异常 继承 Exception
class NoneParameterException(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status
