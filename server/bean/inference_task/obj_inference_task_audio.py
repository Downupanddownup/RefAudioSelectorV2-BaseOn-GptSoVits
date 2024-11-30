from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import ValidationUtils


class ObjInferenceTaskAudio(BaseModel):
    def __init__(self, id=None, task_id=None, audio_id=None, audio_name=None,audio_length=0,
                 audio_path=None, audio_content=None, audio_language=None, audio_category=None, create_time=None):
        self.id = id  # 主键ID，允许从外部传入
        self.task_id = task_id  # 推理任务id
        self.audio_id = audio_id  # 音频id
        self.audio_name = audio_name  # 音频名称
        self.audio_path = audio_path  # 音频路径
        self.audio_content = audio_content  # 音频内容
        self.audio_language = audio_language  # 音频语种
        self.audio_category = audio_category  # 音频分类
        self.audio_length = audio_length  # 音频时长
        self.create_time = create_time  # 创建时间，默认为当前时间

    def __str__(self):
        return (f"Id: {self.id}, TaskId: {self.task_id}, "
                f"AudioId: {self.audio_id}, AudioName: {self.audio_name}, AudioLength: {self.audio_length},"
                f"AudioPath: {self.audio_path}, AudioContent: {self.audio_content}, AudioCategory: {self.audio_category},"
                f"AudioLanguage: {self.audio_language}, CreateTime: {self.create_time}")

class ObjInferenceTaskAudioFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.ids = form_data.get('ids')
        self.task_id = form_data.get('task_id')
        self.result_audio_id = form_data.get('result_audio_id')

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
        
        if not ValidationUtils.is_empty(self.result_audio_id):
            sql += f" and exists (select 1 from tab_obj_inference_task_result_audio where AudioId = ta.Id and Id = ? ) "
            condition.append(f"{self.result_audio_id}")

        return sql, tuple(condition)