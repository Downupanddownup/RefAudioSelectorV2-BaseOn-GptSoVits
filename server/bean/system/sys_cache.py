class SysCache:
    def __init__(self, type=None, key_name=None, value=None):
        self.type = type  # 类型
        self.key_name = key_name  # key
        self.value = value  # 值

    def __repr__(self):
        return f"TabSysCache(type='{self.type}', key_name='{self.key_name}', value='{self.value}')"