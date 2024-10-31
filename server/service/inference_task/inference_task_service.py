import numpy as np
import time
import os
import traceback
import librosa

from concurrent.futures import ProcessPoolExecutor

from server.bean.inference_task.obj_inference_task import ObjInferenceTaskFilter, ObjInferenceTask
from server.bean.inference_task.obj_inference_task_audio import ObjInferenceTaskAudio
from server.bean.inference_task.obj_inference_task_compare_params import ObjInferenceTaskCompareParams
from server.bean.inference_task.obj_inference_task_text import ObjInferenceTaskText
from server.bean.inference_task.task_cell import TaskCell
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter
from server.bean.result_evaluation.obj_inference_task_result_audio import ObjInferenceTaskResultAudio, \
    ObjInferenceTaskResultAudioFilter
from server.common.custom_exception import CustomException
from server.common.log_config import logger, p_logger
from server.common.ras_api_monitor import RasApiMonitor
from server.dao.data_base_manager import db_config
from server.dao.inference_task.inference_task_dao import InferenceTaskDao
from server.service.inference_task.model_manager_service import ModelManagerService
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.service.result_evaluation.result_evaluation_service import ResultEvaluationService
from server.util.util import ValidationUtils


class InferenceTaskService:
    @staticmethod
    def find_count(task_filter: ObjInferenceTaskFilter) -> int:
        return InferenceTaskDao.find_count(task_filter)

    @staticmethod
    def find_list(task_filter: ObjInferenceTaskFilter) -> list[ObjInferenceTask]:
        return InferenceTaskDao.find_list(task_filter)

    @staticmethod
    def add_inference_task(task: ObjInferenceTask) -> int:
        InferenceTaskService.check_inference_task(task)
        if task.compare_type == 'refer_audio':
            reference_audio_list = ReferenceAudioService.find_list(ObjReferenceAudioFilter({
                'category_list_str': ','.join(f'"{p.audio_category}"' for p in task.param_list)
            }))
            task.audio_list = [ObjInferenceTaskAudio(
                audio_id=audio.id,
                audio_name=audio.audio_name,
                audio_path=audio.audio_path,
                audio_content=audio.content,
                audio_language=audio.language,
                audio_category=audio.category,
                audio_length=audio.audio_length,
            ) for audio in reference_audio_list]

        task_id = InferenceTaskDao.insert_inference_task(task)
        if task_id < 1:
            raise CustomException("添加推理任务失败")
        for param in task.param_list:
            param.task_id = task_id
        InferenceTaskDao.batch_insert_task_param(task.param_list)
        for audio in task.audio_list:
            audio.task_id = task_id
        InferenceTaskDao.batch_insert_task_audio(task.audio_list)
        for text in task.text_list:
            text.task_id = task_id
        InferenceTaskDao.batch_insert_task_text(task.text_list)
        return task_id

    @staticmethod
    def check_inference_task(task: ObjInferenceTask) -> None:
        if ValidationUtils.is_empty(task.task_name):
            raise CustomException("任务名不能为空")
        if ValidationUtils.is_empty(task.compare_type):
            raise CustomException("比较类型不能为空")
        if len(task.param_list) == 0:
            raise CustomException("对比参数不能为空")
        if len(task.text_list) == 0:
            raise CustomException("推理文本不能为空")
        if task.compare_type != 'refer_audio' and len(task.audio_list) == 0:
            raise CustomException("音频列表不能为空")

    @staticmethod
    def find_whole_inference_task_by_id(task_id: int) -> ObjInferenceTask:
        task_list = InferenceTaskService.find_list(ObjInferenceTaskFilter({'id': task_id}))
        if len(task_list) == 0:
            return None
        task = task_list[0]
        task.param_list = InferenceTaskService.get_task_param_list_by_task_id(task_id)
        task.audio_list = InferenceTaskService.get_task_audio_list_by_task_id(task_id)
        task.text_list = InferenceTaskService.get_task_text_list_by_task_id(task_id)
        return task

    @staticmethod
    def get_task_param_list_by_task_id(task_id: int) -> list[ObjInferenceTaskCompareParams]:
        return InferenceTaskDao.get_task_param_list_by_task_id(task_id)

    @staticmethod
    def get_task_audio_list_by_task_id(task_id: int) -> list[ObjInferenceTaskAudio]:
        return InferenceTaskDao.get_task_audio_list_by_task_id(task_id)

    @staticmethod
    def get_task_text_list_by_task_id(task_id: int) -> list[ObjInferenceTaskText]:
        return InferenceTaskDao.get_task_text_list_by_task_id(task_id)

    @staticmethod
    def save_inference_task(task: ObjInferenceTask) -> int:
        if task.id < 1:
            raise CustomException("任务id不能为空")
        InferenceTaskService.check_inference_task(task)
        if task.compare_type == 'refer_audio':
            reference_audio_list = ReferenceAudioService.find_list(ObjReferenceAudioFilter({
                'category_list_str': ','.join(f'"{p.audio_category}"' for p in task.param_list)
            }))
            task.audio_list = [ObjInferenceTaskAudio(
                audio_id=audio.id,
                audio_name=audio.audio_name,
                audio_path=audio.audio_path,
                audio_content=audio.content,
                audio_language=audio.language,
                audio_category=audio.category,
                audio_length=audio.audio_length,
            ) for audio in reference_audio_list]

        task_id = task.id

        result = InferenceTaskDao.update_inference_task(task)
        if result < 1:
            raise CustomException("修改推理任务失败")

        InferenceTaskDao.delete_task_param_by_task_id(task_id)
        InferenceTaskDao.delete_task_audio_by_task_id(task_id)
        InferenceTaskDao.delete_task_text_by_task_id(task_id)

        for param in task.param_list:
            param.task_id = task_id
        InferenceTaskDao.batch_insert_task_param(task.param_list)
        for audio in task.audio_list:
            audio.task_id = task_id
        InferenceTaskDao.batch_insert_task_audio(task.audio_list)
        for text in task.text_list:
            text.task_id = task_id
        InferenceTaskDao.batch_insert_task_text(task.text_list)
        return result

    @staticmethod
    def start_execute_inference_task(task: ObjInferenceTask, num_processes: int):
        if task.inference_status != 2:
            if RasApiMonitor.start_service(False):
                RasApiMonitor.set_stream_mode_to_off()
                task_cell_list = create_task_cell_list_if_not_inference(task)
                result = True
                for task_cell in task_cell_list:
                    result = result and generate_audio_files_parallel(task_cell, num_processes)
                RasApiMonitor.stop_service()
                if result:
                    InferenceTaskService.change_inference_task_inference_status_to_finish_if_all_finish(task.id)
            else:
                raise CustomException("RAS API 服务启动失败")

    @staticmethod
    def change_inference_task_inference_status(task_id, inference_status: int) -> int:
        return InferenceTaskDao.change_inference_task_inference_status(task_id, inference_status)

    @staticmethod
    def change_inference_task_inference_status_to_finish_if_all_finish(task_id):
        audio_filter = ObjInferenceTaskResultAudioFilter({
            'taskId': task_id,
            'status': 0,
        })
        count = ResultEvaluationService.find_count(audio_filter)
        if count == 0:
            return InferenceTaskService.change_inference_task_inference_status(task_id, 2)

    @staticmethod
    def update_task_execute_audio_similarity(task_id: int, execute_audio_similarity: int):
        return InferenceTaskDao.update_task_execute_audio_similarity(task_id, execute_audio_similarity)

    @staticmethod
    def update_task_execute_text_similarity(task_id: int, execute_text_similarity: int):
        return InferenceTaskDao.update_task_execute_text_similarity(task_id, execute_text_similarity)


def create_task_cell_list_if_not_inference(task: ObjInferenceTask) -> list[TaskCell]:
    task_result_audio_list = create_task_result_audio_list_if_not_inference(task)
    task_cell_list = []

    param_list = task.param_list

    if task.compare_type == 'gpt_model':
        vits_model = ModelManagerService.get_vits_model_by_name(task.gpt_sovits_version, task.vits_model_name)
        for param in param_list:
            gpt_model = ModelManagerService.get_gpt_model_by_name(param.gpt_sovits_version, param.gpt_model_name)
            task_cell_list.append(TaskCell(gpt_model, vits_model, [audio for audio in task_result_audio_list if
                                                                   audio.compare_param_id == param.id]))
    elif task.compare_type == 'vits_model':
        gpt_model = ModelManagerService.get_gpt_model_by_name(task.gpt_sovits_version, task.gpt_model_name)
        for param in param_list:
            vits_model = ModelManagerService.get_vits_model_by_name(param.gpt_sovits_version, param.vits_model_name)
            task_cell_list.append(TaskCell(gpt_model, vits_model, [audio for audio in task_result_audio_list if
                                                                   audio.compare_param_id == param.id]))
    elif task.compare_type == 'gv':
        for param in param_list:
            gpt_model = ModelManagerService.get_gpt_model_by_name(param.gpt_sovits_version, param.gpt_model_name)
            vits_model = ModelManagerService.get_vits_model_by_name(param.gpt_sovits_version, param.vits_model_name)
            task_cell_list.append(TaskCell(gpt_model, vits_model, [audio for audio in task_result_audio_list if
                                                                   audio.compare_param_id == param.id]))
    elif task.compare_type == 'all':
        for param in param_list:
            gpt_model = ModelManagerService.get_gpt_model_by_name(param.gpt_sovits_version, param.gpt_model_name)
            vits_model = ModelManagerService.get_vits_model_by_name(param.gpt_sovits_version, param.vits_model_name)
            task_cell_list.append(TaskCell(gpt_model, vits_model, [audio for audio in task_result_audio_list if
                                                                   audio.compare_param_id == param.id]))
    else:
        gpt_model = ModelManagerService.get_gpt_model_by_name(task.gpt_sovits_version, task.gpt_model_name)
        vits_model = ModelManagerService.get_vits_model_by_name(task.gpt_sovits_version, task.vits_model_name)
        task_cell_list.append(TaskCell(gpt_model, vits_model, task_result_audio_list))

    return task_cell_list


def create_task_result_audio_list_if_not_inference(task: ObjInferenceTask) -> list[ObjInferenceTaskResultAudio]:
    task_result_audio_list = splicing_task_result_audio_list(task)
    exists_task_result_audio_list = ResultEvaluationService.find_task_result_audio_list_by_task_id(task)
    not_exists_list = []
    for task_result_audio in task_result_audio_list:
        exists = False
        for exist_cell in exists_task_result_audio_list:
            if task_result_audio.equals(exist_cell):
                exists = True
                break
        if not exists:
            not_exists_list.append(task_result_audio)
    ResultEvaluationService.batch_insert_task_result_audio(not_exists_list)

    result_audio_list = ResultEvaluationService.find_task_result_audio_list_by_task_id(task)
    return [audio for audio in result_audio_list if audio.status == 0]


def splicing_task_result_audio_list(task: ObjInferenceTask) -> list[ObjInferenceTaskResultAudio]:
    result_audio_list = []
    param_list = task.param_list
    audio_list = task.audio_list
    text_list = task.text_list
    for param in param_list:
        for audio in audio_list:
            if task.compare_type == 'refer_audio' and param.audio_category != audio.audio_category:
                continue
            for text in text_list:
                result_audio_list.append(ObjInferenceTaskResultAudio(
                    task_id=task.id,
                    text_id=text.id,
                    audio_id=audio.id,
                    compare_param_id=param.id,
                    status=0
                ))
    return result_audio_list


def generate_audio_files_parallel(task_cell: TaskCell, num_processes: int = 1) -> bool:
    switch = False
    try:
        RasApiMonitor.set_api_models(task_cell.gpt_model, task_cell.vits_model)
        switch = True
    except Exception as e:
        logger.error("模型切换异常: \n%s", traceback.format_exc())

    if switch is False:
        return False

    # 将emotion_list均匀分成num_processes个子集
    task_result_audio_list_list = np.array_split(task_cell.task_result_audio_list, num_processes)

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [
            executor.submit(generate_audio_files_for_group, db_config.role_name, task_result_audio_list)
            for task_result_audio_list in task_result_audio_list_list]
        for future in futures:
            future.result()  # 等待所有进程完成

    return True


def generate_audio_files_for_group(role_name: str, task_result_audio_list: list[ObjInferenceTaskResultAudio]):
    try:
        start_time = time.perf_counter()  # 使用 perf_counter 获取高精度计时起点

        db_config.update_db_path(role_name)

        all_count = len(task_result_audio_list)
        has_generated_count = 0

        for task_result_audio in task_result_audio_list:
            # Generate audio byte stream using the create_audio function
            output_dir = task_result_audio.get_audio_directory()
            os.makedirs(output_dir, exist_ok=True)
            audio_file_path = task_result_audio.get_audio_file_path()

            # 检查是否已经存在对应的音频文件，如果存在则跳过
            if os.path.exists(audio_file_path):
                has_generated_count += 1
                logger.info(f"进程ID: {os.getpid()}, 进度: {has_generated_count}/{all_count}")
                continue

            try:

                audio_bytes = RasApiMonitor.inference_audio_from_api_post(task_result_audio.get_inference_params())

                # Write audio bytes to the respective files
                with open(audio_file_path, 'wb') as f:
                    f.write(audio_bytes)

                    # Force data to be written to disk
                    os.fsync(f.fileno())
                    # Give some time for the filesystem to update if necessary
                    # 这里添加一个小的等待时间，根据实际情况调整
                    time.sleep(1)  # 可选

                    # 直接计算音频文件的时长（单位：秒）
                    task_result_audio.audio_length = librosa.get_duration(filename=audio_file_path)

                task_result_audio.status = 1

                task_result_audio.path = audio_file_path

            except Exception as e:
                task_result_audio.status = 0
                logger.error(f"生成音频文件失败: {e}")

            has_generated_count += 1
            logger.info(f"进程ID: {os.getpid()}, 进度: {has_generated_count}/{all_count}")

        ResultEvaluationService.batch_update_task_result_audio_status_file_length(task_result_audio_list)

        end_time = time.perf_counter()  # 获取计时终点
        elapsed_time = end_time - start_time  # 计算执行耗时
        # 记录日志内容
        log_message = f"进程ID: {os.getpid()}, generate_audio_files_for_emotion_group 执行耗时: {elapsed_time:.6f} 秒；推理数量: {has_generated_count}；"
        p_logger.info(log_message)
        logger.info(log_message)
    except Exception as e:
        p_logger.error(f"生成音频文件失败: {e}")
        logger.error(f"生成音频文件失败: {e}")
