import json

from server.bean.base_model import BaseModel


class Role(BaseModel):
    def __init__(self, category: str = '默认', name: str = None):
        self.category = category  # 分类
        self.name = name  # 名称

    def to_dict(self):
        return {
            'category': self.category,
            'name': self.name
        }

    def to_json_string(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json_string(cls, json_str):
        data = json.loads(json_str)
        return cls(category=data['category'], name=data['name'])

    def __repr__(self):
        return f"Role(category='{self.category}', name='{self.name}')"
