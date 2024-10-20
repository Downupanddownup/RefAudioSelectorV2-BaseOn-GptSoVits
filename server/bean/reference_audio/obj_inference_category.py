from server.bean.base_model import BaseModel


class ObjInferenceCategory(BaseModel):
    def __init__(self, id=None, name=None, create_time=None):
        self.id = id
        self.name = name
        self.create_time = create_time  # 创建时间，默认为当前时间