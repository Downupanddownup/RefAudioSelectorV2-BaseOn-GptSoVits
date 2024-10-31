import datetime

from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import ValidationUtils


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


class ObjSoundFusionAudioFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.audio_ids_str = form_data.get('audio_ids_str')
        self.role_name = form_data.get('role_name')
        self.audio_name = form_data.get('audio_name')
        self.content = form_data.get('content')
        self.category = form_data.get('category')
        self.language = form_data.get('language')
        self.category_list_str = form_data.get('category_list_str')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")
        if not ValidationUtils.is_empty(self.audio_ids_str):
            sql += f" and id in ({self.audio_ids_str}) "
        if not ValidationUtils.is_empty(self.role_name):
            sql += f" and RoleName like ? "
            condition.append(f"%{self.role_name}%")
        if not ValidationUtils.is_empty(self.audio_name):
            sql += f" and AudioName like ? "
            condition.append(f"%{self.audio_name}%")

        if not ValidationUtils.is_empty(self.content):
            sql += f" and content like ? "
            condition.append(f"%{self.content}%")

        if not ValidationUtils.is_empty(self.category):
            sql += f" and category = ? "
            condition.append(f"{self.category}")
        if not ValidationUtils.is_empty(self.category_list_str):
            sql += f" and category in ({self.category_list_str}) "

        if not ValidationUtils.is_empty(self.language):
            sql += f" and language = ? "
            condition.append(f"{self.language}")

        return sql, tuple(condition)