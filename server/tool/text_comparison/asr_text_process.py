import os
import sys

sys.path.append(os.getcwd())
from server.bean.result_evaluation.obj_inference_task_result_audio import ObjInferenceTaskResultAudio
from server.common import log_config
from server.dao.data_base_manager import db_config
from server.service.inference_task.inference_task_service import InferenceTaskService
from server.service.result_evaluation.result_evaluation_service import ResultEvaluationService
from server.tool.text_comparison.text_comparison import calculate_result
from server.util.util import str_to_int
import argparse


def process(task_id: int):
    task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
    if task is None:
        log_config.logger.error(f'task_id:{task_id} not found')
        return

    task_result_audio_list = ResultEvaluationService.find_task_result_audio_list_by_task_id(task)
    if task_result_audio_list is None or len(task_result_audio_list) == 0:
        log_config.logger.error(f'task_id:{task_id} result audio list is empty')
        return

    # Step 2: 用参考音频依次比较音频目录下的每个音频，获取相似度分数及对应路径
    all_count = len(task_result_audio_list)
    has_processed_count = 0
    detail_list = []
    for result_audio in task_result_audio_list:
        if result_audio.status != 1 or not result_audio.obj_text or not result_audio.asr_text:
            continue
        score = calculate_result(result_audio.asr_text, result_audio.obj_text.text_content)
        detail = ObjInferenceTaskResultAudio(
            id=result_audio.id,
            asr_similar_score=score
        )
        detail_list.append(detail)
        has_processed_count += 1
        log_config.logger.info(f'进度：{has_processed_count}/{all_count}')

    ResultEvaluationService.batch_update_result_asr_similar_score(detail_list)

    InferenceTaskService.update_task_execute_text_similarity(task_id, 1)


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
    process(
        task_id=str_to_int(cmd.task_id)
    )

    # compare_audio_and_generate_report(
    #     reference_audio_path="D:/tt/渡鸦/refer_audio_all/也对，你的身份和我们不同吗？.wav",
    #     comparison_dir_path='D:/tt/渡鸦/refer_audio_all',
    #     output_file_path='D:/tt/渡鸦/test.txt',
    # )
