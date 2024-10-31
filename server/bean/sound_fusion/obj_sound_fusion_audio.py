import datetime

from server.bean.base_model import BaseModel


class ObjSoundFusionAudio(BaseModel):
    def __init__(self, id=None, role_name='', audio_name='', audio_path='',
                 content='', language='', category='', audio_length=0,
                 remark='', create_time=None):
        self.id = id  # 自增编号
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
        return f"TabObjSoundFusionAudio(id={self.id}, role_name='{self.role_name}', " \
               f"audio_name='{self.audio_name}', audio_path='{self.audio_path}', " \
               f"content='{self.content}', language='{self.language}', " \
               f"category='{self.category}', audio_length={self.audio_length}, " \
               f"remark='{self.remark}', create_time={self.create_time})"
