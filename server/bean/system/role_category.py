from server.bean.base_model import BaseModel
from server.bean.system.role import Role


class RoleCategory(BaseModel):
    def __init__(self, category: str = '默认', role_list: list[Role] = None):
        self.category = category  # 分类
        self.role_list = role_list  # 角色列表

    def __repr__(self):
        return f"Role(category='{self.category}')"
