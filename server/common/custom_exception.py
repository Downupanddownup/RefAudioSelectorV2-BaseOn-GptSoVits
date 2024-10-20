class CustomException(Exception):
    """自定义异常类"""

    def __init__(self, message):
        super().__init__(message)  # 调用基类的构造函数
        self.message = message
