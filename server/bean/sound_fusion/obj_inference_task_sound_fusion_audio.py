from server.bean.base_model import BaseModel


class ObjInferenceTaskSoundFusionAudio(BaseModel):
    def __init__(self, id=None, task_id=0, compare_param_id=0, audio_id=0,
                 role_name='', audio_name='', audio_path='', content='',
                 language='', category='', audio_length=0, remark='',
                 create_time=None):
        self.id = id  # 自增编号
        self.task_id = task_id  # 任务ID
        self.compare_param_id = compare_param_id  # 对比参数ID
        self.audio_id = audio_id  # 融合音频ID
        self.role_name = role_name  # 角色名称
        self.audio_name = audio_name  # 音频名称
        self.audio_path = audio_path  # 音频路径
        self.content = content  # 音频内容
        self.language = language  # 音频语种
        self.category = category  # 音频分类
        self.audio_length = audio_length  # 音频时长
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间

    def __str__(self):
        return f"TabObjInferenceTaskSoundFusionAudio(id={self.id}, task_id={self.task_id}, " \
               f"compare_param_id={self.compare_param_id}, audio_id={self.audio_id}, " \
               f"role_name='{self.role_name}', audio_name='{self.audio_name}', " \
               f"audio_path='{self.audio_path}', content='{self.content}', " \
               f"language='{self.language}', category='{self.category}', " \
               f"audio_length={self.audio_length}, remark='{self.remark}', " \
               f"create_time={self.create_time})"
