from server.bean.inference_task.obj_inference_task import ObjInferenceTask
from server.bean.result_evaluation.obj_inference_task_result_audio import ObjInferenceTaskResultAudio, \
    ObjInferenceTaskResultAudioFilter
from server.dao.result_evaluation.result_evaluation_dao import ResultEvaluationDao


class ResultEvaluationService:
    @staticmethod
    def find_task_result_audio_list_by_task_id(task: ObjInferenceTask) -> list[ObjInferenceTaskResultAudio]:
        result_audio_list = ResultEvaluationDao.find_task_result_audio_list_by_task_id(task.id)
        return ResultEvaluationService.combine_audios_and_task(task, result_audio_list)

    @staticmethod
    def combine_audios_and_task(task: ObjInferenceTask, result_audio_list: list[ObjInferenceTaskResultAudio]):
        if task and result_audio_list:
            param_list = task.param_list
            audio_list = task.audio_list
            text_list = task.text_list
            for result_audio in result_audio_list:
                for param in param_list:
                    if result_audio.compare_param_id == param.id:
                        result_audio.obj_param = param
                        break
                for audio in audio_list:
                    if result_audio.audio_id == audio.id:
                        result_audio.obj_audio = audio
                        break
                for text in text_list:
                    if result_audio.text_id == text.id:
                        result_audio.obj_text = text
                        break
                result_audio.obj_task = task
            task.param_list = []
            task.audio_list = []
            task.text_list = []
            return result_audio_list
        return []

    @staticmethod
    def batch_insert_task_result_audio(result_audio_list: list[ObjInferenceTaskResultAudio]):
        return ResultEvaluationDao.batch_insert_task_result_audio(result_audio_list)

    @staticmethod
    def batch_update_task_result_audio_status_file_length(task_result_audio_list: list[ObjInferenceTaskResultAudio]):
        return ResultEvaluationDao.batch_update_task_result_audio_status_file_length(task_result_audio_list)

    @staticmethod
    def find_count(audio_filter: ObjInferenceTaskResultAudioFilter) -> int:
        return ResultEvaluationDao.find_count(audio_filter)

    @staticmethod
    def find_list(audio_filter: ObjInferenceTaskResultAudioFilter) -> list[ObjInferenceTaskResultAudio]:
        return ResultEvaluationDao.find_list(audio_filter)

    @staticmethod
    def find_whole_list(audio_filter: ObjInferenceTaskResultAudioFilter) -> list[ObjInferenceTaskResultAudio]:
        from server.service.inference_task.inference_task_service import InferenceTaskService
        result_list = []
        audio_list = ResultEvaluationDao.find_list(audio_filter)
        if audio_list is None:
            return result_list
        task_id_set = set([audio.task_id for audio in audio_list])
        for task_id in task_id_set:
            task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
            task_audio_list = [audio for audio in audio_list if audio.task_id == task_id]
            result_list = result_list + ResultEvaluationService.combine_audios_and_task(task, task_audio_list)
        return result_list

    @staticmethod
    def update_result_audio_score(result_audio_id: int, score: int) -> int:
        return ResultEvaluationDao.update_result_audio_score(result_audio_id, score)

    @staticmethod
    def update_result_audio_long_text_score(result_audio_id: int, long_text_score: int) -> int:
        return ResultEvaluationDao.update_result_audio_long_text_score(result_audio_id, long_text_score)

    @staticmethod
    def update_result_audio_remark(result_audio_id: int, remark: str) -> int:
        return ResultEvaluationDao.update_result_audio_remark(result_audio_id, remark)
