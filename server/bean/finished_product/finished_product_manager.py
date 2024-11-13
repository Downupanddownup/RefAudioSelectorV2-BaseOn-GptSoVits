from server.bean.base_model import BaseModel


class ObjFinishedProductManager(BaseModel):
    """
    成品管理类，对应数据库表 tab_obj_finished_product_manager
    """

    def __init__(self,
                 id: str = None,  # 自增编号
                 name: str = None,  # 成品名称
                 category: str = None,  # 分类
                 gpt_sovits_version: str = None,  # 模型版本
                 gpt_model_name: str = None,  # GPT模型名称
                 gpt_model_path: str = None,  # GPT模型路径
                 vits_model_name: str = None,  # Vits模型名称
                 vits_model_path: str = None,  # Vits模型路径
                 top_k: str = None,  # top_k值
                 top_p: str = None,  # top_p值
                 temperature: str = None,  # 温度
                 text_delimiter: str = None,  # 文本分隔符
                 speed: str = None,  # 语速
                 inp_refs: str = None,  # 融合音频，json字符串
                 score: str = None,  # 评分
                 remark: str = None,  # 备注
                 create_time: str = None):  # 创建时间
        self.id = id  # 自增编号
        self.name = name  # 成品名称
        self.category = category  # 分类
        self.gpt_sovits_version = gpt_sovits_version  # 模型版本
        self.gpt_model_name = gpt_model_name  # GPT模型名称
        self.gpt_model_path = gpt_model_path  # GPT模型路径
        self.vits_model_name = vits_model_name  # Vits模型名称
        self.vits_model_path = vits_model_path  # Vits模型路径
        self.top_k = top_k  # top_k值
        self.top_p = top_p  # top_p值
        self.temperature = temperature  # 温度
        self.text_delimiter = text_delimiter  # 文本分隔符
        self.speed = speed  # 语速
        self.inp_refs = inp_refs  # 融合音频，json字符串
        self.score = score  # 评分
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间