import time
import sys
from subprocess import Popen

from fastapi import APIRouter, Request

from server.bean.inference_task.obj_inference_task import ObjInferenceTaskFilter, ObjInferenceTask
from server.bean.inference_task.obj_inference_task_audio import ObjInferenceTaskAudio
from server.bean.inference_task.obj_inference_task_compare_params import ObjInferenceTaskCompareParams
from server.bean.inference_task.obj_inference_task_text import ObjInferenceTaskText
from server.bean.inference_task.obj_inference_text import ObjInferenceTextFilter, ObjInferenceText
from server.common.custom_exception import CustomException
from server.common.log_config import logger
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.inference_task.inference_task_service import InferenceTaskService
from server.service.inference_task.inference_text_service import InferenceTextService
from server.service.inference_task.model_manager_service import ModelManagerService
from server.service.reference_audio.reference_category_service import ReferenceCategoryService
from server.util.util import str_to_int, open_file, ValidationUtils

python_exec = sys.executable or "python"

router = APIRouter(prefix="/task")

inference_task_audio_analysis = None
inference_task_asr_analysis = None
inference_task_asr_text_analysis = None

@router.post("/get_inference_text_list")
async def get_inference_text_list(request: Request):
    form_data = await request.form()
    text_filter = ObjInferenceTextFilter(form_data)

    count = InferenceTextService.find_count(text_filter)
    text_list = InferenceTextService.find_list(text_filter)
    return ResponseResult(data=text_list, count=count)


@router.post("/save_inference_text")
async def update_inference_text(request: Request):
    form_data = await request.form()
    text = ObjInferenceText(
        id=str_to_int(form_data.get('id')),
        category=form_data.get('category'),
        text_content=form_data.get('textContent'),
        text_language=form_data.get('textLanguage')
    )
    if text.id > 0:
        InferenceTextService.update_inference_text_by_id(text)
        text_id = text.id
    else:
        text_id = InferenceTextService.insert_inference_text(text)

    return ResponseResult(data={"text_id": text_id})


@router.post("/delete_inference_text")
async def delete_inference_text(request: Request):
    form_data = await request.form()
    text_id = str_to_int(form_data.get('text_id'))
    if text_id < 1:
        return ResponseResult(code=1, msg="text_id is invalid")

    result = InferenceTextService.delete_inference_text_by_id(text_id)

    return ResponseResult(data={"result": result})


@router.post("/get_inference_task_list")
async def get_inference_task_list(request: Request):
    form_data = await request.form()
    task_filter = ObjInferenceTaskFilter(form_data)

    count = InferenceTaskService.find_count(task_filter)
    task_list = InferenceTaskService.find_list(task_filter)

    return ResponseResult(data=task_list, count=count)


def get_inference_task_from_json(form_data: dict) -> ObjInferenceTask:
    task = ObjInferenceTask(
        id=form_data.get('id'),
        task_name=form_data.get('taskName'),
        compare_type=form_data.get('compareType'),
        gpt_sovits_version=form_data.get('gptSovitsVersion'),
        gpt_model_name=form_data.get('gptModelName'),
        vits_model_name=form_data.get('vitsModelName'),
        top_k=form_data.get('topK'),
        top_p=form_data.get('topP'),
        temperature=form_data.get('temperature'),
        text_delimiter=form_data.get('textDelimiter'),
        speed=form_data.get('speed'),
        other_parameters=form_data.get('otherParameters'),
    )

    audio_list = form_data.get('taskAudioList')
    text_list = form_data.get('taskTextList')
    param_list = form_data.get('compareParams')

    task_audio_list = []
    for audio in audio_list:
        task_audio_list.append(ObjInferenceTaskAudio(
            audio_id=audio.get('audioId'),
            audio_name=audio.get('audioName'),
            audio_path=audio.get('audioPath'),
            audio_content=audio.get('audioContent'),
            audio_language=audio.get('audioLanguage'),
            audio_length=audio.get('audioLength'),
            audio_category=audio.get('audioCategory')
        ))
    task.audio_list = task_audio_list

    task_text_list = []
    for text in text_list:
        task_text_list.append(ObjInferenceTaskText(
            text_id=text.get('textId'),
            category=text.get('category'),
            text_content=text.get('textContent'),
            text_language=text.get('textLanguage')
        ))
    task.text_list = task_text_list

    task_param_list = []
    for param in param_list:
        task_param_list.append(ObjInferenceTaskCompareParams(
            audio_category=param.get('audioCategory'),
            gpt_sovits_version=param.get('gptSovitsVersion'),
            gpt_model_name=param.get('gptModelName'),
            vits_model_name=param.get('vitsModelName'),
            top_k=param.get('topK'),
            top_p=param.get('topP'),
            temperature=param.get('temperature'),
            text_delimiter=param.get('textDelimiter'),
            speed=param.get('speed'),
            other_parameters=param.get('otherParameters')
        ))
    task.param_list = task_param_list
    return task


@router.post("/save_inference_task")
async def save_inference_task(request: Request):
    form_data = await request.json()

    task = get_inference_task_from_json(form_data)
    task_id = 0
    if task.id > 0:
        result = InferenceTaskService.save_inference_task(task)
        if result:
            task_id = task.id
    else:
        task_id = InferenceTaskService.add_inference_task(task)

    return ResponseResult(data={"task_id": task_id})


@router.post("/load_inference_task_detail")
async def load_inference_task_detail(request: Request):
    form_data = await request.form()
    task_id = str_to_int(form_data.get('task_id'))
    task = None
    if task_id > 0:
        task = InferenceTaskService.find_whole_inference_task_by_id(task_id)

    category_list = ReferenceCategoryService.get_category_list()
    gpt_model_list = ModelManagerService.get_gpt_model_list()
    vits_model_list = ModelManagerService.get_vits_model_list()

    return ResponseResult(data={
        "task": task,
        "categoryList": category_list,
        "gptModels": gpt_model_list,
        "vitsModels": vits_model_list
    })


@router.post("/load_model_list")
async def load_model_list(request: Request):

    gpt_model_list = ModelManagerService.get_gpt_model_list()
    vits_model_list = ModelManagerService.get_vits_model_list()

    return ResponseResult(data={
        "gptModels": gpt_model_list,
        "vitsModels": vits_model_list
    })


@router.post("/start_execute_inference_task")
async def start_execute_inference_task(request: Request):
    form_data = await request.form()
    task_id = str_to_int(form_data.get('task_id'))
    if task_id < 0:
        raise CustomException("task_id is invalid")
    task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
    if task is None:
        raise CustomException("未找到task")

    start_time = time.perf_counter()  # 使用 perf_counter 获取高精度计时起点

    InferenceTaskService.start_execute_inference_task(task)

    end_time = time.perf_counter()  # 获取计时终点
    elapsed_time = end_time - start_time  # 计算执行耗时

    # 记录日志内容
    log_message = f"执行耗时: {elapsed_time:.6f} 秒"
    logger.info(log_message)

    return ResponseResult()


@router.post("/open_model_file")
async def open_model_file(request: Request):
    open_file(filepath=db_config.get_model_dir())
    return ResponseResult()


@router.post("/start_task_audio_analysis")
async def start_task_audio_analysis(request: Request):
    form_data = await request.form()
    task_id = str_to_int(form_data.get('task_id'))
    if task_id < 0:
        raise CustomException("task_id is invalid")
    task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
    if task is None:
        raise CustomException("未找到task")

    global inference_task_audio_analysis
    if inference_task_audio_analysis is not None:
        return ResponseResult(code=1, msg='正在执行音频分析，请稍后再试')

    cmd = f'"{python_exec}" server/tool/speaker_verification/inference_task_voice_similarity.py '
    cmd += f' -t "{task_id}"'
    cmd += f' -r "{db_config.role_name}"'

    logger.info(cmd)
    inference_task_audio_analysis = Popen(cmd, shell=True)
    inference_task_audio_analysis.wait()

    inference_task_audio_analysis = None

    return ResponseResult(msg='完成音频分析')


@router.post("/start_task_asr_analysis")
async def start_task_asr_analysis(request: Request):
    form_data = await request.form()
    task_id = str_to_int(form_data.get('task_id'))
    if task_id < 0:
        raise CustomException("task_id is invalid")
    task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
    if task is None:
        raise CustomException("未找到task")

    global inference_task_asr_analysis
    if inference_task_asr_analysis is not None:
        return ResponseResult(code=1, msg='正在执行音频asr，请稍后再试')

    cmd = f'"{python_exec}" server/tool/asr/inference_task_asr.py '
    cmd += f' -t "{task_id}"'
    cmd += f' -r "{db_config.role_name}"'

    logger.info(cmd)
    inference_task_asr_analysis = Popen(cmd, shell=True)
    inference_task_asr_analysis.wait()

    inference_task_asr_analysis = None

    return ResponseResult(msg='完成音频asr')


@router.post("/start_task_text_similarity_analysis")
async def start_task_text_similarity_analysis(request: Request):
    form_data = await request.form()
    task_id = str_to_int(form_data.get('task_id'))
    if task_id < 0:
        raise CustomException("task_id is invalid")
    task = InferenceTaskService.find_whole_inference_task_by_id(task_id)
    if task is None:
        raise CustomException("未找到task")

    global inference_task_asr_text_analysis
    if inference_task_asr_text_analysis is not None:
        return ResponseResult(code=1, msg='正在执行音频文本相似度分析，请稍后再试')

    cmd = f'"{python_exec}" server/tool/text_comparison/asr_text_process.py '
    cmd += f' -t "{task_id}"'
    cmd += f' -r "{db_config.role_name}"'

    logger.info(cmd)
    inference_task_asr_text_analysis = Popen(cmd, shell=True)
    inference_task_asr_text_analysis.wait()

    inference_task_asr_text_analysis = None

    return ResponseResult(msg='完成音频文本相似度分析')