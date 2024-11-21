from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import ValidationUtils


class ObjInferenceText(BaseModel):
    def __init__(self, id=None, category=None, text_content=None, text_language=None, create_time=None):
        self.id = id
        self.category = category  # 文本分类
        self.text_content = text_content  # 推理文本
        self.text_language = text_language  # 文本语种
        self.create_time = create_time

    def __repr__(self):
        return f"<TabObjInferenceText(Id={self.id}, Category='{self.category}', " \
               f"TextContent='{self.text_content[:20]}...'>, " \
               f"TextLanguage='{self.text_language}', CreateTime='{self.create_time}')>"


class ObjInferenceTextFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.ids = form_data.get('ids')
        self.category = form_data.get('category')
        self.text_content = form_data.get('text_content')
        self.text_language = form_data.get('text_language')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")
        if not ValidationUtils.is_empty(self.ids):
            sql += f" and id in ({self.ids}) "
        if not ValidationUtils.is_empty(self.text_content):
            sql += f" and TextContent like ? "
            condition.append(f"%{self.text_content}%")

        if not ValidationUtils.is_empty(self.category):
            sql += f" and category = ? "
            condition.append(f"{self.category}")

        if not ValidationUtils.is_empty(self.text_language):
            sql += f" and TextLanguage = ? "
            condition.append(f"{self.text_language}")

        return sql, tuple(condition)