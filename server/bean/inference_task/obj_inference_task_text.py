from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import ValidationUtils


class ObjInferenceTaskText(BaseModel):
    def __init__(self, id=None, task_id=None, text_id=None, text_content=None, category=None,
                 text_language=None, create_time=None):
        self.id = id  # 主键ID，允许从外部传入
        self.task_id = task_id  # 推理任务id
        self.text_id = text_id  # 推理文本id
        self.category = category  # 文本分类
        self.text_content = text_content  # 推理文本
        self.text_language = text_language  # 文本语种
        self.create_time = create_time  # 创建时间，默认为当前时间

    def __str__(self):
        return (f"Id: {self.id}, TaskId: {self.task_id}, Category: {self.category}, "
                f"TextId: {self.text_id}, TextContent: {self.text_content}, "
                f"TextLanguage: {self.text_language}, CreateTime: {self.create_time}")


class ObjInferenceTaskTextFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.ids = form_data.get('ids')
        self.task_id = form_data.get('task_id')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")

        if not ValidationUtils.is_empty(self.ids):
            sql += f" and id in ({self.ids}) "

        if not ValidationUtils.is_empty(self.task_id):
            sql += f" and taskId = ? "
            condition.append(f"{self.task_id}")

        return sql, tuple(condition)