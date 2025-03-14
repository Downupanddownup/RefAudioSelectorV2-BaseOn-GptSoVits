from server.bean.base_model import BaseModel
from server.bean.inference_task.obj_inference_task_audio import ObjInferenceTaskAudio
from server.bean.inference_task.obj_inference_task_compare_params import ObjInferenceTaskCompareParams
from server.bean.inference_task.obj_inference_task_text import ObjInferenceTaskText
from server.bean.sound_fusion.obj_inference_task_sound_fusion_audio import ObjInferenceTaskSoundFusionAudio
from server.common.filter import Filter
from server.util.util import ValidationUtils, str_to_int


class ObjInferenceTask(BaseModel):
    def __init__(self, id=None, task_name=None, compare_type=None, gpt_sovits_version=None,
                 gpt_model_name=None, vits_model_name=None, top_k=None,
                 top_p=None, temperature=None, text_delimiter=None,
                 speed=None, sample_steps=None, if_sr=None,
                 other_parameters=None, create_time=None,
                 inference_status=0, execute_text_similarity=0, execute_audio_similarity=0,
                 conclusion: str = None,
                 audio_list: list[ObjInferenceTaskAudio] = None, param_list: list[ObjInferenceTaskCompareParams] = None,
                 text_list: list[ObjInferenceTaskText] = None,
                 inp_refs_list: list[ObjInferenceTaskSoundFusionAudio] = None):
        self.id = id  # 主键ID，允许从外部传入
        self.task_name = task_name  # 任务名称
        self.compare_type = compare_type  # 比较类型
        self.gpt_sovits_version = gpt_sovits_version  # 模型版本
        self.gpt_model_name = gpt_model_name  # GPT模型名称
        self.vits_model_name = vits_model_name  # Vits模型名称
        self.top_k = top_k  # top_k值
        self.top_p = top_p  # top_p值
        self.temperature = temperature  # 温度
        self.text_delimiter = text_delimiter  # 文本分隔符
        self.speed = speed  # 语速
        self.sample_steps = sample_steps  # 采样步数
        self.if_sr = if_sr  # 是否超分
        self.other_parameters = other_parameters  # 其余参数
        self.inference_status = inference_status  # 推理状态 0 待推理 1 推理中 2 推理完成
        self.execute_text_similarity = execute_text_similarity  # 是否已执行文本相似度 0 否 1 是
        self.execute_audio_similarity = execute_audio_similarity  # 是否已执行音频相似度 0 否 1 是
        self.conclusion = conclusion  # 任务结论
        self.create_time = create_time  # 创建时间，默认为当前时间
        self.audio_list = audio_list
        self.param_list = param_list
        self.text_list = text_list
        self.inp_refs_list = inp_refs_list
        self.result_audio_count = 0

    def __str__(self):
        return (f"Id: {self.id}, TaskName: {self.task_name}, CompareType: {self.compare_type}, "
                f"GptSovitsVersion: {self.gpt_sovits_version}, "
                f"GptModelName: {self.gpt_model_name}, "
                f"VitsModelName: {self.vits_model_name}, "
                f"TopK: {self.top_k}, TopP: {self.top_p}, "
                f"Temperature: {self.temperature}, TextDelimiter: {self.text_delimiter}, "
                f"Speed: {self.speed}, OtherParameters: {self.other_parameters}, "
                f"InferenceStatus: {self.inference_status}, ExecuteTextSimilarity: {self.execute_text_similarity}, "
                f"ExecuteAudioSimilarity: {self.execute_audio_similarity}, "
                f"CreateTime: {self.create_time}")


class ObjInferenceTaskFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.ids = form_data.get('ids')
        self.task_name = form_data.get('task_name')
        self.compare_type = form_data.get('compare_type')
        self.inference_status = str_to_int(form_data.get('inference_status'))

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")

        if not ValidationUtils.is_empty(self.ids):
            sql += f" and id in ({self.ids}) "

        if not ValidationUtils.is_empty(self.task_name):
            sql += f" and TaskName like ? "
            condition.append(f"%{self.task_name}%")

        if not ValidationUtils.is_empty(self.compare_type):
            sql += f" and CompareType = ? "
            condition.append(f"{self.compare_type}")

        if self.inference_status is not None and self.inference_status > -1:
            sql += f" and InferenceStatus = ? "
            condition.append(f"{self.inference_status}")

        return sql, tuple(condition)
