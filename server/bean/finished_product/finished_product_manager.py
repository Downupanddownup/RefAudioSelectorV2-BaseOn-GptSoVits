import json
from server.bean.base_model import BaseModel
from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudio
from server.common.filter import Filter
from server.util.util import ValidationUtils


class ObjFinishedProductManager(BaseModel):
    """
    成品管理类，对应数据库表 tab_obj_finished_product_manager
    """

    def __init__(self,
                 id: int = None,  # 自增编号
                 name: str = None,  # 成品名称
                 category: str = None,  # 分类
                 gpt_sovits_version: str = None,  # 模型版本
                 gpt_model_name: str = None,  # GPT模型名称
                 gpt_model_path: str = None,  # GPT模型路径
                 vits_model_name: str = None,  # Vits模型名称
                 vits_model_path: str = None,  # Vits模型路径
                 audio_id: int = None,  # 音频id
                 audio_name: str = None,  # 音频名称
                 audio_path: str = None,  # 音频路径
                 content: str = None,  # 音频内容
                 language: str = None,  # 语言
                 audio_length: int = None,  # 音频长度
                 top_k: int = None,  # top_k值
                 top_p: float = None,  # top_p值
                 temperature: float = None,  # 温度
                 text_delimiter: str = None,  # 文本分隔符
                 speed: float = None,  # 语速
                 inp_refs: str = None,  # 融合音频，json字符串
                 score: int = None,  # 评分
                 remark: str = None,  # 备注
                 create_time=None):  # 创建时间
        self.id = id  # 自增编号
        self.name = name  # 成品名称
        self.category = category  # 分类
        self.gpt_sovits_version = gpt_sovits_version  # 模型版本
        self.gpt_model_name = gpt_model_name  # GPT模型名称
        self.gpt_model_path = gpt_model_path  # GPT模型路径
        self.vits_model_name = vits_model_name  # Vits模型名称
        self.vits_model_path = vits_model_path  # Vits模型路径
        self.audio_id = audio_id  # 音频id
        self.audio_name = audio_name  # 音频名称
        self.audio_path = audio_path  # 音频路径
        self.content = content  # 音频内容
        self.language = language  # 语言
        self.audio_length = audio_length  # 音频长度
        self.top_k = top_k  # top_k值
        self.top_p = top_p  # top_p值
        self.temperature = temperature  # 温度
        self.text_delimiter = text_delimiter  # 文本分隔符
        self.speed = speed  # 语速
        self.inp_refs = inp_refs  # 融合音频，json字符串
        self.sound_fusion_list = []  # 融合音频
        self.score = score  # 评分
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间
        self.set_sound_fusion_list_from_json(self.inp_refs)

    def set_sound_fusion_list(self, sound_fusion_list: list[ObjSoundFusionAudio]):
        self.sound_fusion_list = sound_fusion_list
        if sound_fusion_list is not None:
            self.inp_refs = json.dumps([x.to_dict() for x in sound_fusion_list])
        else:
            self.inp_refs = None

    def set_sound_fusion_list_from_json(self, inp_refs: str):
        if inp_refs is not None:
            dict_list = json.loads(inp_refs)
            self.sound_fusion_list = [ObjSoundFusionAudio.from_json_string(d) for d in dict_list]
        else:
            self.sound_fusion_list = []


class ObjFinishedProductManagerFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.ids = form_data.get('ids')
        self.category = form_data.get('category')
        self.category_list_str = form_data.get('category_list_str')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")
        if not ValidationUtils.is_empty(self.ids):
            sql += f" and id in ({self.ids}) "
        if not ValidationUtils.is_empty(self.category):
            sql += f" and category = ? "
            condition.append(f"{self.category}")
        if not ValidationUtils.is_empty(self.category_list_str):
            sql += f" and category in ({self.category_list_str}) "

        return sql, tuple(condition)
