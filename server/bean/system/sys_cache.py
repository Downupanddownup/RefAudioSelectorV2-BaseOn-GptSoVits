class SysCache:
    def __init__(self, type=None, key_name=None, value=None):
        self.id = None  # 自增编号，由数据库处理
        self.type = type  # 类型
        self.key_name = key_name  # key
        self.value = value  # 值

    def __repr__(self):
        return f"TabSysCache(id={self.id}, type='{self.type}', key_name='{self.key_name}', value='{self.value}')"