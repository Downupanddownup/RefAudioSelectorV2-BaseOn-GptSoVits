import sys
import os

sys.path.append(os.getcwd())

from server.tool.speaker_verification.audio_compare import compare

import argparse
import server.common.log_config as log_config
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter
from server.bean.reference_audio.obj_reference_audio_compare_detail import ObjReferenceAudioCompareDetail
from server.common.time_util import timeit_decorator

from server.service.reference_audio.reference_audio_compare_sevice import ReferenceAudioCompareService
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.util.util import str_to_int
from server.dao.data_base_manager import db_config
from server.bean.system.role import Role


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
        'categories': task.category_names
    }))

    if len(compare_audio_list) == 0:
        log_config.logger.error(f'category:{task.category_names} not found')
        ReferenceAudioCompareService.update_task_to_fail(task_id)
        return

    ReferenceAudioCompareService.update_task_to_start(task_id)

    reference_audio_path = audio.audio_path

    # Step 2: 用参考音频依次比较音频目录下的每个音频，获取相似度分数及对应路径
    all_count = len(compare_audio_list)
    has_processed_count = 0
    detail_list = []
    for audio in compare_audio_list:
        score = compare(reference_audio_path, audio.audio_path)
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
    parser.add_argument("-c", "--role_category", type=str, required=True,
                        help="Path to the role category.")

    # Reference audio path
    parser.add_argument("-t", "--task_id", type=str, required=True,
                        help="Path to the task id.")

    return parser.parse_args()


if __name__ == '__main__':
    cmd = parse_arguments()
    db_config.update_db_path(Role(category=cmd.role_category, name=cmd.role_name))
    compare_audio_and_generate_report(
        task_id=str_to_int(cmd.task_id)
    )

    # compare_audio_and_generate_report(
    #     reference_audio_path="D:/tt/渡鸦/refer_audio_all/也对，你的身份和我们不同吗？.wav",
    #     comparison_dir_path='D:/tt/渡鸦/refer_audio_all',
    #     output_file_path='D:/tt/渡鸦/test.txt',
    # )
