import time
import os
import shutil
import uuid
from typing import Dict

import librosa

from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudio, ObjReferenceAudioFilter
from server.dao.data_base_manager import db_config
from server.dao.reference_audio.reference_audio_dao import ReferenceAudioDao
from server.common.log_config import logger
from server.util.util import get_file_size, calculate_md5, zip_directory, write_text_to_file


class ReferenceAudioService:
    @staticmethod
    def find_count(audio_filter: ObjReferenceAudioFilter) -> int:
        return ReferenceAudioDao.find_count(audio_filter)

    @staticmethod
    def find_list(audio_filter: ObjReferenceAudioFilter) -> list[ObjReferenceAudio]:
        return ReferenceAudioDao.find_list(audio_filter)

    @staticmethod
    def get_reference_dir():
        output_dir = f'{db_config.get_role_work_dir()}\\refer_audio'
        # 创建输出目录，如果它不存在的话
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    @staticmethod
    def get_new_reference_audio_path():
        unique_id_time_based = uuid.uuid1()
        new_filename = str(unique_id_time_based) + '.wav'
        new_path = os.path.join(ReferenceAudioService.get_reference_dir(), new_filename)
        return new_path

    @staticmethod
    def convert_from_list(list_file: str, category: str, is_manual_calib: int, write_policy: str) \
            -> list[ObjReferenceAudio]:
        from server.service.reference_audio.reference_category_service import ReferenceCategoryService

        add_audio_list = []
        update_audio_list = []

        ReferenceCategoryService.add_category(category)

        # 解析.list文件，并操作文件
        with open(list_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split('|')
            if len(parts) != 4:
                logger.error(f"Line format incorrect: {line}")
                continue

            audio_path, _, language, transcription = parts

            new_path = ReferenceAudioService.get_new_reference_audio_path()

            # 如果目标文件已存在，不要覆盖
            if os.path.exists(new_path):
                logger.info(f"File already exists: {new_path}")
                continue

            try:

                # 检查音频文件是否存在
                if not os.path.exists(audio_path):
                    logger.info(f"Audio file does not exist: {audio_path}")
                    continue

                audio_name = os.path.basename(audio_path)

                exists = ReferenceAudioService.get_audio_by_name(audio_name)

                if exists:
                    if write_policy == 'skip':
                        continue

                shutil.copy2(audio_path, new_path)

                # 直接计算音频文件的时长（单位：秒）
                duration = librosa.get_duration(filename=new_path)

                valid_or_not = 1

                if not ReferenceAudioService.check_audio_duration(duration):
                    # 复制音频文件到output目录并重命名
                    valid_or_not = 0
                    logger.info(f"File copied and renamed to: {new_path}")

                file_size = get_file_size(new_path)

                md5_value = calculate_md5(new_path)

                id = 0

                if exists:
                    if write_policy == 'overwrite':
                        id = exists.id
                    elif write_policy == 'rename':
                        # 获取当前时间的纳秒数
                        nanoseconds = time.time_ns()
                        # 使用 os.path.splitext 拆分文件名
                        name, ext = os.path.splitext(audio_name)
                        audio_name = f"{name}_{nanoseconds}{ext}"

                item = ObjReferenceAudio(id=id, audio_name=audio_name, audio_path=new_path,
                                         content=transcription, language=language.lower(), category=category,
                                         valid_or_not=valid_or_not, md5_value=md5_value,
                                         is_manual_calib=is_manual_calib,
                                         file_size=file_size, score=0, long_text_score=0, remark='',
                                         audio_length=duration)
                if id > 0:
                    update_audio_list.append(item)
                else:
                    add_audio_list.append(item)

            except Exception as e:
                logger.error(f"An error occurred while processing: {audio_path}")
                logger.error(e)

        logger.info("Processing complete.")
        return add_audio_list, update_audio_list

    @staticmethod
    def insert_reference_audio_list(audio_list: list[ObjReferenceAudio]) -> int:
        return ReferenceAudioDao.batch_insert_reference_audio(audio_list)


    @staticmethod
    def update_reference_audio_list(audio_list: list[ObjReferenceAudio]) -> int:
        return ReferenceAudioDao.update_reference_audio_list(audio_list)

    @staticmethod
    def get_audio_by_id(audio_id: int) -> ObjReferenceAudio:
        audio_list = ReferenceAudioDao.find_list(ObjReferenceAudioFilter({
            'id': audio_id
        }))
        if len(audio_list) > 0:
            return audio_list[0]
        return None

    @staticmethod
    def update_audio_category(change_audio_id_str: str, target_category: str) -> int:
        return ReferenceAudioDao.update_audio_category(change_audio_id_str, target_category)

    @staticmethod
    def add_reference_audio(audio: ObjReferenceAudio):
        ReferenceAudioService.insert_reference_audio_list([audio])

    @staticmethod
    def update_reference_audio(audio: ObjReferenceAudio):
        ReferenceAudioDao.update_reference_audio(audio)

    @staticmethod
    def update_audio_content(audio_id: int, content: str):
        return ReferenceAudioDao.update_audio_content(audio_id, content)

    @staticmethod
    def update_audio_remark(audio_id: int, remark: str):
        return ReferenceAudioDao.update_audio_remark(audio_id, remark)

    @staticmethod
    def delete_reference_audio(audio_id: int):
        return ReferenceAudioDao.delete_reference_audio(audio_id)

    @staticmethod
    def check_audio_duration(duration, min_duration=3, max_duration=10):
        # 判断时长是否在3s至10s之间
        if min_duration <= duration <= max_duration:
            return True
        else:
            return False

    @staticmethod
    def update_audio_score_by_task_result_id(result_audio_id: int):
        return ReferenceAudioDao.update_audio_score_by_task_result_id(result_audio_id)

    @staticmethod
    def update_audio_long_text_score_by_task_result_id(result_audio_id: int):
        return ReferenceAudioDao.update_audio_long_text_score_by_task_result_id(result_audio_id)

    @staticmethod
    def generate_audio_list_zip(audio_list: list[ObjReferenceAudio]):
        if len(audio_list) == 0:
            return None

        temp_dir = f'{db_config.workspace}/temp/{uuid.uuid1()}'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        role_dir = os.path.join(temp_dir, db_config.role.name)
        if not os.path.exists(role_dir):
            os.makedirs(role_dir)

        try:

            ReferenceAudioService.export_audio_list(audio_list, role_dir)

            zip_directory(role_dir, role_dir)

            zip_file_path = f'{role_dir}.zip'
        finally:
            pass

        return temp_dir, zip_file_path

    @staticmethod
    def export_audio_list(audio_list: list[ObjReferenceAudio], role_dir: str):
        dir_name = 'refer_audio'
        reference_dir = os.path.join(role_dir, dir_name)
        if not os.path.exists(reference_dir):
            os.makedirs(reference_dir)
        list_file = []
        for audio in audio_list:
            if audio.audio_path is not None and os.path.exists(audio.audio_path):
                new_path = os.path.join(reference_dir, audio.audio_name)
                shutil.copy2(audio.audio_path, new_path)
                list_file.append(f'{os.path.join(dir_name,audio.audio_name)}|{dir_name}|{audio.language.upper()}|{audio.content}')
        list_file_path = os.path.join(role_dir, db_config.role.name + '.list')
        write_text_to_file('\n'.join(list_file), list_file_path)
        explain_file = '只保存了音频相对路径，实际使用时，请更改为绝对路径.txt'
        write_text_to_file('', os.path.join(role_dir, explain_file))

    @staticmethod
    def get_audio_by_name(audio_name: str) -> ObjReferenceAudio:
        if not audio_name:
            return None
        audio_filter = ObjReferenceAudioFilter({
            'audio_name': audio_name
        })
        audio_list = ReferenceAudioDao.find_list(audio_filter)
        audio = None
        for item in audio_list:
            if item.audio_name == audio_name:
                audio = item
                break
        return audio
