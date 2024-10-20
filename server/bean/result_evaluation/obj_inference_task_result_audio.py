import os

from server.bean.base_model import BaseModel
from server.bean.inference_task.obj_inference_task import ObjInferenceTask
from server.bean.inference_task.obj_inference_task_audio import ObjInferenceTaskAudio
from server.bean.inference_task.obj_inference_task_compare_params import ObjInferenceTaskCompareParams
from server.bean.inference_task.obj_inference_task_text import ObjInferenceTaskText
from server.common.filter import Filter
from server.common.ras_api_monitor import InferenceParams
from server.dao.data_base_manager import db_config
from server.util.util import ValidationUtils


class ObjInferenceTaskResultAudio(BaseModel):
    def __init__(self, id=None, task_id=None, text_id=None, audio_id=None, compare_param_id=None,
                 path=None, audio_length=None, asr_text=None, asr_similar_score=None, status=0,
                 audio_similar_score=None, score=None, long_text_score=None, remark=None, create_time=None,
                 obj_task: ObjInferenceTask = None, obj_text: ObjInferenceTaskText = None,
                 obj_audio: ObjInferenceTaskAudio = None, obj_param: ObjInferenceTaskCompareParams = None):
        self.id = id  # 自增编号，通常在数据库中自动管理
        self.task_id = task_id  # 推理任务id
        self.text_id = text_id  # 推理文本id
        self.audio_id = audio_id  # 参考音频id
        self.compare_param_id = compare_param_id  # 比对参数id
        self.path = path  # 音频地址
        self.audio_length = audio_length  # 时长
        self.status = status  # 生成状态 1 成功；2 失败
        self.asr_text = asr_text  # asr文本
        self.asr_similar_score = asr_similar_score  # 文本相似度
        self.audio_similar_score = audio_similar_score  # 音频相似度
        self.score = score  # 评分
        self.long_text_score = long_text_score  # 长文评分
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间，在实例化时设置，默认为当前时间
        self.obj_task = obj_task
        self.obj_text = obj_text
        self.obj_audio = obj_audio
        self.obj_param = obj_param

    def get_audio_directory(self) -> str:
        return os.path.join(db_config.get_work_dir(), "inference_audio", f'task_{self.task_id}',
                            f'compare_param_{self.compare_param_id}', f'text_{self.text_id}')

    def get_audio_file_path(self) -> str:
        return os.path.join(self.get_audio_directory(), f'audio_{self.audio_id}.wav')

    def get_inference_params(self):
        return InferenceParams(
            refer_wav_path=self.obj_audio.audio_path,
            prompt_text=self.obj_audio.audio_content,
            prompt_language=self.obj_audio.audio_language,
            text=self.obj_text.text_content,
            text_language=self.obj_text.text_language,
            cut_punc=self.obj_param.text_delimiter if self.obj_task.compare_type == 'text_delimiter' else self.obj_task.text_delimiter,
            top_k=self.obj_param.top_k if self.obj_task.compare_type == 'top_k' else self.obj_task.top_k,
            top_p=self.obj_param.top_p if self.obj_task.compare_type == 'top_p' else self.obj_task.top_p,
            temperature=self.obj_param.temperature if self.obj_task.compare_type == 'temperature' else self.obj_task.temperature,
            speed=self.obj_param.speed if self.obj_task.compare_type == 'speed' else self.obj_task.speed
        )

    def equals(self, exist_cell: 'ObjInferenceTaskResultAudio'):
        return self.task_id == exist_cell.task_id and self.text_id == exist_cell.text_id and \
            self.audio_id == exist_cell.audio_id and self.compare_param_id == exist_cell.compare_param_id


class ObjInferenceTaskResultAudioFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.task_id = form_data.get('taskId')
        self.compare_param_ids = form_data.get('compareParamIds')
        self.audio_ids = form_data.get('audioIds')
        self.text_ids = form_data.get('textIds')
        self.audio_length_start = form_data.get('audioLengthStart')
        self.audio_length_end = form_data.get('audioLengthEnd')
        self.asr_similar_score_start = form_data.get('asrSimilarScoreStart')
        self.asr_similar_score_end = form_data.get('asrSimilarScoreEnd')
        self.audio_similar_score_start = form_data.get('audioSimilarScoreStart')
        self.audio_similar_score_end = form_data.get('audioSimilarScoreEnd')
        self.score_start = form_data.get('scoreStart')
        self.score_end = form_data.get('scoreEnd')
        self.long_text_score_start = form_data.get('longTextScoreStart')
        self.long_text_score_end = form_data.get('longTextScoreEnd')
        self.remark = form_data.get('remark')

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")
        if not ValidationUtils.is_empty(self.task_id):
            sql += f" and taskId = ? "
            condition.append(f"{self.task_id}")
        if not ValidationUtils.is_empty(self.compare_param_ids):
            sql += f" and compareParamId in ({self.compare_param_ids}) "
        if not ValidationUtils.is_empty(self.audio_ids):
            sql += f" and audioId in ({self.audio_ids}) "
        if not ValidationUtils.is_empty(self.text_ids):
            sql += f" and textId in ({self.text_ids}) "
        if not ValidationUtils.is_empty(self.audio_length_start):
            sql += f" and audioLength >= ? "
            condition.append(f"{self.audio_length_start}")
        if not ValidationUtils.is_empty(self.audio_length_end):
            sql += f" and audioLength <= ? "
            condition.append(f"{self.audio_length_end}")
        if not ValidationUtils.is_empty(self.asr_similar_score_start):
            sql += f" and asrSimilarScore >= ? "
            condition.append(f"{self.asr_similar_score_start}")
        if not ValidationUtils.is_empty(self.asr_similar_score_end):
            sql += f" and asrSimilarScore <= ? "
            condition.append(f"{self.asr_similar_score_end}")
        if not ValidationUtils.is_empty(self.audio_similar_score_start):
            sql += f" and audioSimilarScore >= ? "
            condition.append(f"{self.audio_similar_score_start}")
        if not ValidationUtils.is_empty(self.audio_similar_score_end):
            sql += f" and audioSimilarScore <= ? "
            condition.append(f"{self.audio_similar_score_end}")
        if not ValidationUtils.is_empty(self.score_start):
            sql += f" and score >= ? "
            condition.append(f"{self.score_start}")
        if not ValidationUtils.is_empty(self.score_end):
            sql += f" and score <= ? "
            condition.append(f"{self.score_end}")
        if not ValidationUtils.is_empty(self.long_text_score_start):
            sql += f" and longTextScore >= ? "
            condition.append(f"{self.long_text_score_start}")
        if not ValidationUtils.is_empty(self.long_text_score_end):
            sql += f" and longTextScore <= ? "
            condition.append(f"{self.long_text_score_end}")
        if not ValidationUtils.is_empty(self.remark):
            sql += f" and remark like ? "
            condition.append(f"%{self.remark}%")

        return sql, tuple(condition)
