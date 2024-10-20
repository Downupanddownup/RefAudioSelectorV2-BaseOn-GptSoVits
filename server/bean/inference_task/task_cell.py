from server.bean.inference_task.gpt_model import GptModel
from server.bean.inference_task.vits_model import VitsModel
from server.bean.result_evaluation.obj_inference_task_result_audio import ObjInferenceTaskResultAudio


class TaskCell:
    def __init__(self, gpt_model: GptModel = None, vits_model: VitsModel = None,
                 task_result_audio_list: list[ObjInferenceTaskResultAudio] = None):
        self.gpt_model = gpt_model
        self.vits_model = vits_model
        self.task_result_audio_list = task_result_audio_list
