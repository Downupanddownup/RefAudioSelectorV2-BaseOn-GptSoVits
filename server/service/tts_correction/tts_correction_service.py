import os
import time
import traceback
from io import BytesIO

import numpy as np
import librosa
from concurrent.futures import ProcessPoolExecutor

from server.bean.finished_product.finished_product_manager import ObjFinishedProductManagerFilter
from server.bean.text.obj_inference_text import ObjInferenceTextFilter
from server.bean.system.role import Role
from server.bean.tts_correction.obj_tts_correction_task import ObjTtsCorrectionTask, ObjTtsCorrectionTaskFilter
from server.bean.tts_correction.obj_tts_correction_task_detail import ObjTtsCorrectionTaskDetailFilter, \
    ObjTtsCorrectionTaskDetail
from server.common.custom_exception import CustomException
from server.common.log_config import logger, p_logger
from server.common.ras_api_monitor import RasApiMonitor
from server.dao.data_base_manager import db_config
from server.dao.tts_correction.tts_correction_dao import TtsCorrectionDao
from server.service.finished_product.finished_product_service import FinishedProductService
from server.service.inference_task.inference_text_service import InferenceTextService
from server.util.util import merge_audio_files, zip_directory, read_zip_to_memory, delete_directory


class TtsCorrectionService:
    @staticmethod
    def find_count(task_filter: ObjTtsCorrectionTaskFilter) -> int:
        return TtsCorrectionDao.find_count(task_filter)

    @staticmethod
    def find_list(task_filter: ObjTtsCorrectionTaskFilter) -> list[ObjTtsCorrectionTask]:
        task_list = TtsCorrectionDao.find_list(task_filter)
        if task_list is None or len(task_list) == 0:
            return task_list
        text_ids = []
        product_ids = []
        for task in task_list:
            text_ids.append(str(task.text_id))
            product_ids.append(str(task.product_id))

        text_list = InferenceTextService.find_list(ObjInferenceTextFilter({
            'ids': ','.join(text_ids),
        }))
        if task_list is not None:
            for task in task_list:
                for text in text_list:
                    if str(text.id) == str(task.text_id):
                        task.text_obj = text
                        break
        product_list = FinishedProductService.find_list(ObjFinishedProductManagerFilter({
            'ids': ','.join(product_ids),
        }))
        if product_list is not None:
            for task in task_list:
                for product in product_list:
                    if str(product.id) == str(task.product_id):
                        task.product = product
                        break
        return task_list

    @staticmethod
    def find_detail_count(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> int:
        return TtsCorrectionDao.find_detail_count(detail_filter)

    @staticmethod
    def find_detail_list(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> list[ObjTtsCorrectionTaskDetail]:
        return TtsCorrectionDao.find_detail_list(detail_filter)

    @staticmethod
    def find_task_by_id(task_id: int) -> ObjTtsCorrectionTask:
        task_filter = ObjTtsCorrectionTaskFilter({
            'id': task_id
        })
        task_list = TtsCorrectionService.find_list(task_filter)

        if task_list is None or len(task_list) == 0:
            return None

        task = task_list[0]

        detail_list = TtsCorrectionService.find_detail_list(ObjTtsCorrectionTaskDetailFilter({
            'task_id': task_id
        }))

        task.detail_list = detail_list

        return task

    @staticmethod
    def add_tts_correction_task(task: ObjTtsCorrectionTask) -> int:
        return TtsCorrectionDao.add_tts_correction_task(task)

    @staticmethod
    def batch_add_tts_correction_task_detail(task_detail_list: list[ObjTtsCorrectionTaskDetail]) -> int:
        return TtsCorrectionDao.batch_add_tts_correction_task_detail(task_detail_list)

    @staticmethod
    def start_execute_tts_correction_task(task: ObjTtsCorrectionTask, inference_process_num: int):
        if RasApiMonitor.start_service(False, 'wav'):
            RasApiMonitor.set_stream_mode_to_off()
            TtsCorrectionService.change_task_status_to_start(task.id)
            generate_audio_files_parallel(task, inference_process_num)
            TtsCorrectionService.change_task_status_to_finish(task.id)
        else:
            raise CustomException("RAS API 服务启动失败")

    @staticmethod
    def change_task_status_to_start(id: int):
        return TtsCorrectionDao.change_task_status(id, 1)

    @staticmethod
    def change_task_status_to_finish(id: int):
        return TtsCorrectionDao.change_task_status(id, 2)

    @staticmethod
    def generate_srt(task: ObjTtsCorrectionTask, output_dir: str) -> str:

        output_file = os.path.join(output_dir, f'{task.task_name}.srt')

        """
        根据音频数据生成SRT字幕文件。

        :param audio_data: 包含音频地址、文本内容和时长的数组
        :param output_file: 输出的SRT文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            start_time = 0.0  # 初始时间为0秒
            for i, entry in enumerate(task.detail_list, start=1):
                duration = entry['audio_length']
                end_time = start_time + duration

                # 格式化时间戳
                start_time_str = format_time(start_time)
                end_time_str = format_time(end_time)

                # 写入SRT文件
                f.write(f"{i}\n")
                f.write(f"{start_time_str} --> {end_time_str}\n")
                f.write(f"{entry['text_content']}\n")
                f.write("\n")

                # 更新开始时间
                start_time = end_time
        return output_file

    @staticmethod
    def generate_txt(task: ObjTtsCorrectionTask, output_dir: str) -> str:

        output_file = os.path.join(output_dir, f'{task.task_name}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            context = ''.join([entry['text_content'] for entry in task.detail_list]).replace('<br>', '\n')
            f.write(context)

        return output_file

    @staticmethod
    def generate_audio(task: ObjTtsCorrectionTask, output_dir: str) -> str:
        output_file = os.path.join(output_dir, f'{task.task_name}.wav')
        audio_files = [detail.audio_path for detail in task.detail_list]
        merge_audio_files(audio_files, output_file)
        return output_file

    @staticmethod
    def generate_zip(task: ObjTtsCorrectionTask) -> BytesIO:

        output_dir = f'{db_config.workspace}/temp/tts_correction/task_{task.id}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            TtsCorrectionService.generate_srt(task, output_dir)

            TtsCorrectionService.generate_txt(task, output_dir)

            TtsCorrectionService.generate_audio(task, output_dir)

            zip_file_path = f'{output_dir}/{task.task_name}.zip'
            zip_directory(output_dir, zip_file_path)

            zip_in_memory = read_zip_to_memory(zip_file_path)
        finally:
            delete_directory(output_dir)

        return zip_in_memory


def format_time(seconds):
    """
    将秒数转换为SRT格式的时间戳。

    :param seconds: 秒数
    :return: SRT格式的时间戳字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def generate_audio_files_parallel(task: ObjTtsCorrectionTask, num_processes: int = 1) -> bool:
    switch = False
    try:
        RasApiMonitor.set_api_models(task.product.get_gpt_model(), task.product.get_vits_model())
        switch = True
    except Exception as e:
        logger.error("模型切换异常: \n%s", traceback.format_exc())

    if switch is False:
        return False

    # 将emotion_list均匀分成num_processes个子集
    task_detail_list_list = np.array_split(task.detail_list, num_processes)

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [
            executor.submit(generate_audio_for_group, db_config.role, detail_list)
            for detail_list in task_detail_list_list]
        for future in futures:
            future.result()  # 等待所有进程完成

    return True


def generate_audio_for_group(role: Role, task: ObjTtsCorrectionTask):
    try:

        detail_list = task.detail_list

        start_time = time.perf_counter()  # 使用 perf_counter 获取高精度计时起点

        db_config.update_db_path(role)

        all_count = len(detail_list)
        has_generated_count = 0

        for detail in detail_list:
            # Generate audio byte stream using the create_audio function
            output_dir = detail.get_audio_directory()
            os.makedirs(output_dir, exist_ok=True)
            audio_file_path = detail.get_audio_file_path()

            # 检查是否已经存在对应的音频文件，如果存在则跳过
            if os.path.exists(audio_file_path):
                has_generated_count += 1
                logger.info(f"进程ID: {os.getpid()}, 进度: {has_generated_count}/{all_count}")
                continue

            try:

                audio_bytes = RasApiMonitor.inference_audio_from_api_post(
                    detail.get_inference_params(task.product, task.text_obj))

                # Write audio bytes to the respective files
                with open(audio_file_path, 'wb') as f:
                    f.write(audio_bytes)

                    # Force data to be written to disk
                    os.fsync(f.fileno())
                    # Give some time for the filesystem to update if necessary
                    # 这里添加一个小的等待时间，根据实际情况调整
                    time.sleep(1)  # 可选

                detail.status = 2

                detail.audio_path = audio_file_path

            except Exception as e:
                detail.status = 3
                logger.error(f"生成音频文件失败: {e}")

            has_generated_count += 1
            logger.info(f"进程ID: {os.getpid()}, 进度: {has_generated_count}/{all_count}")

        for detail in detail_list:
            if detail.status == 2:
                # 直接计算音频文件的时长（单位：秒）
                detail.audio_length = librosa.get_duration(filename=detail.audio_path)

        TtsCorrectionDao.batch_update_tts_correction_detail_status_file_length(detail_list)

        end_time = time.perf_counter()  # 获取计时终点
        elapsed_time = end_time - start_time  # 计算执行耗时
        # 记录日志内容
        log_message = f"进程ID: {os.getpid()}, generate_audio_for_group 执行耗时: {elapsed_time:.6f} 秒；推理数量: {has_generated_count}；"
        p_logger.info(log_message)
        logger.info(log_message)
    except Exception as e:
        p_logger.error(f"生成音频文件失败: {e}")
        logger.error(f"生成音频文件失败: {e}")
