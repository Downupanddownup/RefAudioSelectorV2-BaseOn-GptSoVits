import os
import uuid
import time
from fastapi import UploadFile

from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudioFilter, ObjSoundFusionAudio
from server.dao.data_base_manager import db_config
from server.dao.sound_fusion.sound_fusion_dao import SoundFusionDao


class SoundFusionService:
    @staticmethod
    def find_count(audio_filter: ObjSoundFusionAudioFilter) -> int:
        return SoundFusionDao.find_count(audio_filter)

    @staticmethod
    def find_list(audio_filter: ObjSoundFusionAudioFilter) -> list[ObjSoundFusionAudio]:
        return SoundFusionDao.find_list(audio_filter)

    @staticmethod
    def batch_add_sound_fusion_audio(sound_fusion_audio_list: list[ObjSoundFusionAudio]):
        return SoundFusionDao.batch_add_sound_fusion_audio(sound_fusion_audio_list)

    @staticmethod
    def add_sound_fusion_audio(audio: ObjSoundFusionAudio):
        return SoundFusionDao.batch_add_sound_fusion_audio([audio])

    @staticmethod
    def update_sound_fusion_audio(audio: ObjSoundFusionAudio):
        return SoundFusionDao.update_sound_fusion_audio(audio)

    @staticmethod
    def delete_sound_fusion_audio_by_id(audio_id: int):
        return SoundFusionDao.delete_sound_fusion_audio_by_id(audio_id)

    @staticmethod
    def get_new_sound_fusion_path():
        output_dir = f'{db_config.get_master_db_dir()}\\sound_fusion_audio'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unique_id_time_based = uuid.uuid1()
        new_filename = str(unique_id_time_based) + '.wav'
        new_path = os.path.join(output_dir, new_filename)
        return new_path
