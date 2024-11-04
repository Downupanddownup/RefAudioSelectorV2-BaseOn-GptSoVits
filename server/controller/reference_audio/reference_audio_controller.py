import sys
import os
import librosa
import uuid
import time
from fastapi import APIRouter, Request

from server.bean.reference_audio.obj_inference_category import ObjInferenceCategory
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter, ObjReferenceAudio
from server.bean.reference_audio.obj_reference_audio_compare_task import ObjReferenceAudioCompareTask
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.reference_audio.reference_audio_compare_sevice import ReferenceAudioCompareService
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.service.reference_audio.reference_category_service import ReferenceCategoryService
from server.util.util import ValidationUtils, clean_path, str_to_int, str_to_float, save_file
from server.common.log_config import logger
from subprocess import Popen

python_exec = sys.executable or "python"

router = APIRouter(prefix="/audio")

p_similarity = None


@router.post("/load_audio_list_file")
async def load_audio_list_file(request: Request):
    form_data = await request.form()
    audio_list_file = form_data.get("audioListFile")
    if ValidationUtils.is_empty(audio_list_file):
        return ResponseResult(code=1, msg="audioListFile is empty")
    audio_list_file = clean_path(audio_list_file)

    audio_list = ReferenceAudioService.convert_from_list(audio_list_file)
    count = ReferenceAudioService.insert_reference_audio_list(audio_list)

    return ResponseResult(msg=f'导入{count}个音频')


@router.post("/get_reference_audio_list")
async def get_reference_audio_list(request: Request):
    form_data = await request.form()
    audio_filter = ObjReferenceAudioFilter(form_data)

    count = ReferenceAudioService.find_count(audio_filter)
    audio_list = ReferenceAudioService.find_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/get_compare_audio_detail_list")
async def get_compare_audio_detail_list(request: Request):
    form_data = await request.form()
    audio_id = str_to_int(form_data.get('audioId'))
    if ValidationUtils.is_empty(audio_id):
        return ResponseResult(code=1, msg="audioId is empty")

    last_task = ReferenceAudioCompareService.get_last_finish_task_by_audio_id(audio_id)

    if last_task is None:
        return ResponseResult(msg='没有完成比较的音频')

    compare_audio_detail_list = ReferenceAudioCompareService.get_compare_detail_list_by_task_id(
        last_task.id)

    return ResponseResult(data=compare_audio_detail_list)


@router.post("/change_audio_category")
async def change_audio_category(request: Request):
    form_data = await request.form()
    audio_id = str_to_int(form_data.get('audioId'))
    target_category = form_data.get('targetCategory')
    limit_score = str_to_float(form_data.get('limitScore'))
    if ValidationUtils.is_empty(audio_id):
        return ResponseResult(code=1, msg="audioId is empty")
    if ValidationUtils.is_empty(target_category):
        return ResponseResult(code=1, msg="请输入目标分类")
    if ValidationUtils.is_empty(limit_score):
        return ResponseResult(code=1, msg="请输入分割值")

    last_task = ReferenceAudioCompareService.get_last_finish_task_by_audio_id(audio_id)

    if last_task is None:
        return ResponseResult(msg='没有完成比较的音频')

    change_count = ReferenceAudioCompareService.change_audio_category(last_task.id, target_category, limit_score)

    return ResponseResult(msg=f'修改{change_count}个音频分类')


@router.post("/get_audio_category_list")
async def get_audio_category_list(request: Request):
    form_data = await request.form()

    audio_category_list = ReferenceCategoryService.get_category_list()

    return ResponseResult(data=audio_category_list)


@router.post("/start_compare_audio")
async def start_compare_audio(request: Request):
    form_data = await request.form()
    audio_id = form_data.get('audioId')
    category_name = form_data.get('categoryName')

    if ValidationUtils.is_empty(audio_id) or ValidationUtils.is_empty(category_name):
        return ResponseResult(code=1, msg='参数错误')

    global p_similarity
    if p_similarity is not None:
        return ResponseResult(code=1, msg='正在比较音频，请稍后再试')

    task = ObjReferenceAudioCompareTask(audio_id=audio_id, category_name=category_name)
    task_id = ReferenceAudioCompareService.insert_task(task)

    cmd = f'"{python_exec}" server/tool/speaker_verification/voice_similarity.py '
    cmd += f' -t "{task_id}"'
    cmd += f' -r "{db_config.role_name}"'

    logger.info(cmd)
    p_similarity = Popen(cmd, shell=True)
    p_similarity.wait()

    p_similarity = None

    return ResponseResult(msg='完成音频比较')


@router.post("/update_reference_audio")
async def update_reference_audio(request: Request):
    form_data = await request.form()

    audio = ObjReferenceAudio(
        id=str_to_int(form_data.get('id'), 0),
        audio_name=form_data.get('audioName'),
        content=form_data.get('content'),
        language=form_data.get('language'),
        category=form_data.get('category'),
    )

    if audio.id < 1:
        return ResponseResult(code=1, msg='参数错误')
    ReferenceAudioService.update_reference_audio(audio)

    return ResponseResult()


@router.post("/add_reference_audio")
async def add_reference_audio(request: Request):
    form_data = await request.form()

    file = form_data.get('file')

    audio = ObjReferenceAudio(
        audio_name=form_data.get('audioName'),
        content=form_data.get('content'),
        language=form_data.get('language'),
        category=form_data.get('category'),
    )

    new_path = ReferenceAudioService.get_new_reference_audio_path()

    audio.audio_path = new_path

    await save_file(file, new_path)

    # 直接计算音频文件的时长（单位：秒）
    audio.audio_length = librosa.get_duration(filename=new_path)

    ReferenceCategoryService.add_category(audio.category)

    ReferenceAudioService.add_reference_audio(audio)

    return ResponseResult()
