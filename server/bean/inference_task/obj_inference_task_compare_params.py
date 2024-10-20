from server.bean.base_model import BaseModel


class ObjInferenceTaskCompareParams(BaseModel):
    def __init__(self, id=None, task_id=None, audio_category=None, gpt_sovits_version=None,
                 gpt_model_name=None, vits_model_name=None, top_k=None,
                 top_p=None, temperature=None, text_delimiter=None,
                 speed=None, other_parameters=None, create_time=None):
        self.id = id  # 主键ID，允许从外部传入
        self.task_id = task_id  # 任务id
        self.audio_category = audio_category  # 音频分类
        self.gpt_sovits_version = gpt_sovits_version  # 模型版本
        self.gpt_model_name = gpt_model_name  # GPT模型名称
        self.vits_model_name = vits_model_name  # Vits模型名称
        self.top_k = top_k  # top_k值
        self.top_p = top_p  # top_p值
        self.temperature = temperature  # 温度
        self.text_delimiter = text_delimiter  # 文本分隔符
        self.speed = speed  # 语速
        self.other_parameters = other_parameters  # 其余参数
        self.create_time = create_time  # 创建时间，默认为当前时间

    def __str__(self):
        return (f"Id: {self.id}, TaskId: {self.task_id}, AudioCategory: {self.audio_category},"
                f"GptSovitsVersion: {self.gpt_sovits_version}, "
                f"GptModelName: {self.gpt_model_name}, "
                f"VitsModelName: {self.vits_model_name}, "
                f"TopK: {self.top_k}, TopP: {self.top_p}, "
                f"Temperature: {self.temperature}, TextDelimiter: {self.text_delimiter}, "
                f"Speed: {self.speed}, OtherParameters: {self.other_parameters}, "
                f"CreateTime: {self.create_time}")