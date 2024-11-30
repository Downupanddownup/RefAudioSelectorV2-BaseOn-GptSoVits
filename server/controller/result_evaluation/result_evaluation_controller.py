from fastapi import APIRouter, Request

from server.bean.result_evaluation.obj_inference_task_result_audio import ObjInferenceTaskResultAudioFilter, \
    ObjInferenceTaskResultAudio
from server.common.response_result import ResponseResult
from server.service.inference_task.inference_task_service import InferenceTaskService
from server.service.result_evaluation.result_evaluation_service import ResultEvaluationService
from server.util.util import ValidationUtils

router = APIRouter(prefix="/evaluation")


@router.post("/get_result_evaluation_of_task_list")
async def get_result_evaluation_of_task_list(request: Request):
    form_data = await request.form()
    audio_filter = ObjInferenceTaskResultAudioFilter(form_data)

    if audio_filter.task_id is None:
        return ResponseResult(code=1, msg="task_id is required")

    count = ResultEvaluationService.find_count(audio_filter)
    audio_list = ResultEvaluationService.find_list(audio_filter)
    task = InferenceTaskService.find_whole_inference_task_by_id(audio_filter.task_id)

    return ResponseResult(data={
        "task": task,
        "audioList": audio_list
    }, count=count)


@router.post("/get_result_evaluation_list")
async def get_result_evaluation_list(request: Request):
    form_data = await request.form()
    audio_filter = ObjInferenceTaskResultAudioFilter(form_data)

    count = ResultEvaluationService.find_count(audio_filter)
    audio_list = ResultEvaluationService.find_whole_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/get_inference_task_result_audio_list")
async def get_inference_task_result_audio_list(request: Request):
    form_data = await request.form()
    audio_filter = ObjInferenceTaskResultAudioFilter(form_data)

    count = ResultEvaluationService.find_count(audio_filter)
    audio_list = ResultEvaluationService.find_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/get_inference_task_result_audio_list2")
async def get_inference_task_result_audio_list2(request: Request):
    form_data = await request.form()
    audio_filter = ObjInferenceTaskResultAudioFilter(form_data)

    count = ResultEvaluationService.find_count(audio_filter)
    audio_list = ResultEvaluationService.find_list2(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/update_result_audio_score")
async def update_result_audio_score(request: Request):
    form_data = await request.form()
    result_audio_id = form_data.get('id')
    score = form_data.get('score')

    if ValidationUtils.is_empty(result_audio_id):
        return ResponseResult(code=1, msg="id is required")
    if ValidationUtils.is_empty(score):
        return ResponseResult(code=1, msg="score is required")

    ResultEvaluationService.update_result_audio_score(result_audio_id, score)

    return ResponseResult()


@router.post("/update_result_audio_long_text_score")
async def update_result_audio_long_text_score(request: Request):
    form_data = await request.form()
    result_audio_id = form_data.get('id')
    long_text_score = form_data.get('long_text_score')

    if ValidationUtils.is_empty(result_audio_id):
        return ResponseResult(code=1, msg="id is required")
    if ValidationUtils.is_empty(long_text_score):
        return ResponseResult(code=1, msg="long_text_score is required")

    ResultEvaluationService.update_result_audio_long_text_score(result_audio_id, long_text_score)

    return ResponseResult()


@router.post("/update_result_audio_remark")
async def update_result_audio_remark(request: Request):
    form_data = await request.form()
    result_audio_id = form_data.get('id')
    remark = form_data.get('remark')

    if ValidationUtils.is_empty(result_audio_id):
        return ResponseResult(code=1, msg="id is required")

    ResultEvaluationService.update_result_audio_remark(result_audio_id, remark)

    return ResponseResult()


@router.post("/get_inference_task_result_audio_detail")
async def get_inference_task_result_audio_detail(request: Request):
    form_data = await request.form()
    result_audio_id = form_data.get('id')

    if ValidationUtils.is_empty(result_audio_id):
        return ResponseResult(code=1, msg="id is required")

    result_audio = ResultEvaluationService.find_one_by_id(result_audio_id)

    if not result_audio:
        return ResponseResult(code=1, msg="无此记录")

    task = InferenceTaskService.find_whole_inference_task_by_id(result_audio.task_id)

    result_audio.obj_task = task
    result_audio.obj_text = next((text for text in task.text_list if result_audio.text_id == text.id), None)
    result_audio.obj_audio = next((audio for audio in task.audio_list if result_audio.audio_id == audio.id), None)
    result_audio.obj_param = next((param for param in task.param_list if result_audio.compare_param_id == param.id),
                                  None)

    task.text_list = []
    task.audio_list = []
    task.param_list = []

    return ResponseResult(data=result_audio)
