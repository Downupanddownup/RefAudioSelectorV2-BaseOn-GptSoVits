from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import str_to_int, ValidationUtils


class ObjTtsCorrectionTaskDetail(BaseModel):
    def __init__(self, id=0, task_id=None, text_content=None, text_index=None, status=None,
                 audio_path=None, asr_text=None, asr_text_similarity=None, audio_status=None, create_time=None):
        self.id = id  # 自增编号
        self.task_id = task_id  # 任务id
        self.text_content = text_content  # 待推理的文本内容
        self.text_index = text_index  # 文本序号
        self.status = status  # 推理状态 0 待推理；1 推理中；2 已完成；3 失败
        self.audio_path = audio_path  # 音频路径
        self.asr_text = asr_text  # asr文本
        self.asr_text_similarity = asr_text_similarity  # 文本相似度
        self.audio_status = audio_status  # 音频状态 0 未校验；1 推理正确；2 推理不正确
        self.create_time = create_time  # 创建时间

    def __str__(self):
        return (f"TabObjTtsCorrectionTaskDetail(id={self.id}, task_id={self.task_id}, "
                f"text_content='{self.text_content}', text_index={self.text_index}, "
                f"status={self.status}, audio_path='{self.audio_path}', "
                f"asr_text='{self.asr_text}', asr_text_similarity={self.asr_text_similarity}, "
                f"audio_status={self.audio_status}, create_time='{self.create_time}')")


class ObjTtsCorrectionTaskDetailFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.task_id = form_data.get('task_id')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.task_id):
            sql += f" and task_id = ? "
            condition.append(f"{self.task_id}")

        return sql, tuple(condition)
