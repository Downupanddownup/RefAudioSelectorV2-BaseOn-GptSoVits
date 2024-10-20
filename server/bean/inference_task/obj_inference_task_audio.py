from server.bean.base_model import BaseModel


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
