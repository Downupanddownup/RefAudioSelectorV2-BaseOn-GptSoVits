import os
import shutil
import uuid
from typing import Dict

import librosa

from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudio, ObjReferenceAudioFilter
from server.dao.data_base_manager import db_config
from server.dao.reference_audio.reference_audio_dao import ReferenceAudioDao
from server.common.log_config import logger


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
    def convert_from_list(list_file: str) -> list[ObjReferenceAudio]:

        audio_list = []

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

                category = 'default'

                # 检查音频文件是否存在
                if not os.path.exists(audio_path):
                    logger.info(f"Audio file does not exist: {audio_path}")
                    item = ObjReferenceAudio(audio_name=os.path.basename(audio_path), audio_path='',
                                             content=transcription, language=language, category=category,
                                             audio_length=0, valid_or_not=0)
                    audio_list.append(item)
                    continue

                # 直接计算音频文件的时长（单位：秒）
                duration = librosa.get_duration(filename=audio_path)

                if not check_audio_duration(duration):
                    # 复制音频文件到output目录并重命名
                    category = '无效'
                    logger.info(f"File copied and renamed to: {new_path}")

                shutil.copy2(audio_path, new_path)
                item = ObjReferenceAudio(audio_name=os.path.basename(audio_path), audio_path=new_path,
                                         content=transcription, language=language, category=category,
                                         audio_length=duration, valid_or_not=1)
                audio_list.append(item)

            except Exception as e:
                logger.error(f"An error occurred while processing: {audio_path}")
                logger.error(e)

        logger.info("Processing complete.")
        return audio_list

    @staticmethod
    def insert_reference_audio_list(audio_list: list[ObjReferenceAudio]) -> int:
        return ReferenceAudioDao.batch_insert_reference_audio(audio_list)

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
    def update_reference_audio(audio):
        ReferenceAudioDao.update_reference_audio(audio)


def check_audio_duration(duration, min_duration=3, max_duration=10):
    # 判断时长是否在3s至10s之间
    if min_duration <= duration <= max_duration:
        return True
    else:
        return False
