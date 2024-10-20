import sys
import os

# 获取当前脚本所在的目录
current_script_directory = os.path.dirname(__file__)

# 构建上级目录的路径
parent_directory_path = os.path.join(current_script_directory, '..\\..\\..')

# 将构建的路径插入到sys.path列表的开头
sys.path.insert(0, parent_directory_path)

import argparse
import torchaudio
import torchaudio.transforms as T
import platform
import server.common.config_params as params
import server.common.log_config as log_config
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter
from server.bean.reference_audio.obj_reference_audio_compare_detail import ObjReferenceAudioCompareDetail
from server.bean.reference_audio.obj_reference_audio_compare_task import ObjReferenceAudioCompareTask
from server.common.time_util import timeit_decorator

from modelscope.pipelines import pipeline

from server.service.reference_audio.reference_audio_compare_sevice import ReferenceAudioCompareService
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.util.util import str_to_int
from server.dao.data_base_manager import db_config

speaker_verification_models = {
    'speech_campplus_sv_zh-cn_16k-common': {
        'task': 'speaker-verification',
        'model': 'server/tool/speaker_verification/models/speech_campplus_sv_zh-cn_16k-common',
        'model_revision': 'v1.0.0'
    },
    'speech_eres2net_sv_zh-cn_16k-common': {
        'task': 'speaker-verification',
        'model': 'server/tool/speaker_verification/models/speech_eres2net_sv_zh-cn_16k-common',
        'model_revision': 'v1.0.5'
    }
}


def init_model(model_type='speech_campplus_sv_zh-cn_16k-common'):
    models = speaker_verification_models
    return pipeline(
        task=models[model_type]['task'],
        model=models[model_type]['model'],
        model_revision=models[model_type]['model_revision']
    )


@timeit_decorator
def compare_audio_and_generate_report(task_id: int):
    task = ReferenceAudioCompareService.get_task_by_id(task_id)
    if task is None:
        log_config.logger.error(f'task_id:{task_id} not found')
        return

    audio = ReferenceAudioService.get_audio_by_id(task.audio_id)
    if audio is None:
        log_config.logger.error(f'audio_id:{task.audio_id} not found')
        ReferenceAudioCompareService.update_task_to_fail(task_id)
        return

    compare_audio_list = ReferenceAudioService.find_list(ObjReferenceAudioFilter({
        'category': task.category_name
    }))

    if len(compare_audio_list) == 0:
        log_config.logger.error(f'category:{task.category_name} not found')
        ReferenceAudioCompareService.update_task_to_fail(task_id)
        return

    ReferenceAudioCompareService.update_task_to_start(task_id)

    sv_pipeline = init_model()

    reference_audio_path = audio.audio_path

    # Step 2: 用参考音频依次比较音频目录下的每个音频，获取相似度分数及对应路径
    all_count = len(compare_audio_list)
    has_processed_count = 0
    detail_list = []
    for audio in compare_audio_list:
        score = sv_pipeline([reference_audio_path, audio.audio_path])['score']
        detail = ObjReferenceAudioCompareDetail(
            task_id=task_id,
            compare_audio_id=audio.id,
            score=score
        )
        detail_list.append(detail)
        has_processed_count += 1
        log_config.logger.info(f'进度：{has_processed_count}/{all_count}')

    ReferenceAudioCompareService.batch_insert_task_detail(detail_list)

    ReferenceAudioCompareService.update_task_to_finish(task_id)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Audio processing script arguments")

    # Reference audio path
    parser.add_argument("-r", "--role_name", type=str, required=True,
                        help="Path to the role name.")

    # Reference audio path
    parser.add_argument("-t", "--task_id", type=str, required=True,
                        help="Path to the task id.")

    return parser.parse_args()


if __name__ == '__main__':
    cmd = parse_arguments()
    db_config.update_db_path(cmd.role_name)
    compare_audio_and_generate_report(
        task_id=str_to_int(cmd.task_id)
    )

    # compare_audio_and_generate_report(
    #     reference_audio_path="D:/tt/渡鸦/refer_audio_all/也对，你的身份和我们不同吗？.wav",
    #     comparison_dir_path='D:/tt/渡鸦/refer_audio_all',
    #     output_file_path='D:/tt/渡鸦/test.txt',
    # )
