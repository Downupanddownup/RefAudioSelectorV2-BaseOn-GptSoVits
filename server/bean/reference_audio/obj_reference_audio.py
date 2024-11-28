from server.bean.base_model import BaseModel
from server.common.filter import Filter
from server.util.util import ValidationUtils, str_to_int


class ObjReferenceAudio(BaseModel):
    def __init__(self, id=None, audio_name=None, audio_path=None, content=None,
                 language=None, category=None, audio_length=None,
                 valid_or_not=None, md5_value=None, is_manual_calib=None, file_size=None,
                 score=None, long_text_score=None, remark=None,
                 create_time=None):
        self.id = id  # 主键ID，允许从外部传入
        self.audio_name = audio_name  # 音频名称
        self.audio_path = audio_path  # 音频路径
        self.content = content  # 音频内容
        self.language = language  # 音频语种
        self.category = category  # 音频分类
        self.audio_length = audio_length  # 音频时长
        self.valid_or_not = valid_or_not # 是否有效 1 有效 0 无效
        self.md5_value = md5_value # md5值
        self.is_manual_calib = is_manual_calib # 是否人工校准 1 是； 0 否
        self.file_size = file_size # 文件大小
        self.score = score  # 评分
        self.long_text_score = long_text_score  # 长文评分
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间，默认为当前时间

    def __str__(self):
        return (f"Id: {self.id}, AudioName: {self.audio_name}, "
                f"AudioPath: {self.audio_path}, Content: {self.content}, "
                f"Language: {self.language}, Category: {self.category},"
                f"ValidOrNot: {self.valid_or_not}, Md5Value: {self.md5_value}, "
                f"IsManualCalib: {self.is_manual_calib}, FileSize: {self.file_size}, "
                f"Score: {self.score}, LongTextScore: {self.long_text_score}, remark: {self.remark}, "
                f"AudioLength: {self.audio_length}, CreateTime: {self.create_time}")


class ObjReferenceAudioFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.audio_ids_str = form_data.get('audio_ids_str')
        self.audio_name = form_data.get('audio_name')
        self.content = form_data.get('content')
        self.category = form_data.get('category')
        self.valid = str_to_int(form_data.get('valid'),0)
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
        if not ValidationUtils.is_empty(self.audio_name):
            sql += f" and AudioName like ? "
            condition.append(f"%{self.audio_name}%")
        if not ValidationUtils.is_empty(self.content):
            sql += f" and content like ? "
            condition.append(f"%{self.content}%")
        if not ValidationUtils.is_empty(self.category):
            sql += f" and category = ? "
            condition.append(f"{self.category}")
        if self.valid == 1:
            sql += f" and category <> '无效' "
        if not ValidationUtils.is_empty(self.category_list_str):
            sql += f" and category in ({self.category_list_str}) "
        if not ValidationUtils.is_empty(self.language):
            sql += f" and language = ? "
            condition.append(f"{self.language}")
        return sql, tuple(condition)
