import urllib.parse
import sys
import os
import librosa
import uuid
import time
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import StreamingResponse

from server.bean.reference_audio.obj_inference_category import ObjInferenceCategory
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter, ObjReferenceAudio
from server.bean.reference_audio.obj_reference_audio_compare_task import ObjReferenceAudioCompareTask
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.reference_audio.reference_audio_compare_sevice import ReferenceAudioCompareService
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.service.reference_audio.reference_category_service import ReferenceCategoryService
from server.util.util import ValidationUtils, clean_path, str_to_int, str_to_float, save_file, get_file_size, \
    calculate_md5, delete_directory
from server.common.log_config import logger
from subprocess import Popen

python_exec = sys.executable or "python"

router = APIRouter(prefix="/audio")

p_similarity = None


@router.post("/load_audio_list_file")
async def load_audio_list_file(request: Request):
    form_data = await request.form()
    audio_list_file = form_data.get("audioListFile")
    category = form_data.get("category")
    is_manual_calib = str_to_int(form_data.get("isManualCalib"), 0)
    write_policy = form_data.get("writePolicy")
    if ValidationUtils.is_empty(audio_list_file):
        return ResponseResult(code=1, msg="audioListFile is empty")

    if write_policy not in ['overwrite', 'skip', 'rename']:
        return ResponseResult(code=1, msg="writePolicy is invalid")

    audio_list_file = clean_path(audio_list_file)

    add_audio_list, update_audio_list = ReferenceAudioService.convert_from_list(audio_list_file, category,
                                                                                is_manual_calib, write_policy)

    add_count = 0
    overwrite_count = 0

    if len(add_audio_list) > 0:
        add_count = ReferenceAudioService.insert_reference_audio_list(add_audio_list)
    if len(update_audio_list) > 0:
        overwrite_count = ReferenceAudioService.update_reference_audio_list(update_audio_list)

    return ResponseResult(msg=f'新增{add_count}个音频；覆盖{overwrite_count}个音频')


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
    category_names = form_data.get('categoryNames')

    if ValidationUtils.is_empty(audio_id) or ValidationUtils.is_empty(category_names):
        return ResponseResult(code=1, msg='参数错误')

    global p_similarity
    if p_similarity is not None:
        return ResponseResult(code=1, msg='正在比较音频，请稍后再试')

    task = ObjReferenceAudioCompareTask(audio_id=audio_id, category_names=category_names)
    task_id = ReferenceAudioCompareService.insert_task(task)

    cmd = f'"{python_exec}" server/tool/speaker_verification/voice_similarity.py '
    cmd += f' -t "{task_id}"'
    cmd += f' -r "{db_config.role.name}"'
    cmd += f' -c "{db_config.role.category}"'

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
        remark=form_data.get('remark'),
        is_manual_calib=form_data.get('isManualCalib'),
    )

    if audio.id < 1:
        return ResponseResult(code=1, msg='参数错误')

    ReferenceCategoryService.add_category(audio.category)

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
        remark=form_data.get('remark'),
        is_manual_calib=form_data.get('isManualCalib'),
    )

    new_path = ReferenceAudioService.get_new_reference_audio_path()

    audio.audio_path = new_path

    await save_file(file, new_path)

    # 直接计算音频文件的时长（单位：秒）
    audio.audio_length = librosa.get_duration(filename=new_path)

    valid_or_not = 0
    if ReferenceAudioService.check_audio_duration(audio.audio_length):
        valid_or_not = 1

    audio.valid_or_not = valid_or_not

    audio.file_size = get_file_size(new_path)

    audio.md5_value = calculate_md5(new_path)

    ReferenceCategoryService.add_category(audio.category)

    ReferenceAudioService.add_reference_audio(audio)

    return ResponseResult()


@router.post("/update_audio_content")
async def update_audio_content(request: Request):
    form_data = await request.form()

    audio_id = str_to_int(form_data.get('id'), 0)

    content = form_data.get('content')

    if audio_id < 1:
        return ResponseResult(code=1, msg='参数错误')
    ReferenceAudioService.update_audio_content(audio_id, content)

    return ResponseResult()


@router.post("/update_audio_remark")
async def update_audio_remark(request: Request):
    form_data = await request.form()

    audio_id = str_to_int(form_data.get('id'), 0)

    remark = form_data.get('remark')

    if audio_id < 1:
        return ResponseResult(code=1, msg='参数错误')
    ReferenceAudioService.update_audio_remark(audio_id, remark)

    return ResponseResult()


@router.post("/update_audio_is_manual_calib")
async def update_audio_is_manual_calib(request: Request):
    form_data = await request.form()

    audio_id = str_to_int(form_data.get('id'), 0)

    is_manual_calib = form_data.get('isManualCalib')

    if audio_id < 1:
        return ResponseResult(code=1, msg='参数错误')
    ReferenceAudioService.update_audio_is_manual_calib(audio_id, is_manual_calib)

    return ResponseResult()


@router.post("/update_audio_category")
async def update_audio_category(request: Request):
    form_data = await request.form()

    audio_id = str_to_int(form_data.get('id'), 0)

    category = form_data.get('category')

    if audio_id < 1:
        return ResponseResult(code=1, msg='参数错误')

    ReferenceCategoryService.add_category(category)

    ReferenceAudioService.update_audio_category(str(audio_id), category)

    return ResponseResult()


@router.post("/add_category")
async def add_category(request: Request):
    form_data = await request.form()

    category = form_data.get('category')

    ReferenceCategoryService.add_category(category)

    return ResponseResult()


@router.post("/delete_reference_audio")
async def delete_reference_audio(request: Request):
    form_data = await request.form()
    audio_id = str_to_int(form_data.get('id'), 0)

    if audio_id < 1:
        return ResponseResult(code=1, msg='参数错误')

    ReferenceAudioService.delete_reference_audio(audio_id)

    return ResponseResult()


@router.post("/generate_audio_list_zip")
async def generate_audio_list_zip(request: Request):
    form_data = await request.form()
    audio_filter = ObjReferenceAudioFilter(form_data)
    audio_filter.page = 0
    audio_filter.limit = 0

    audio_list = ReferenceAudioService.find_list(audio_filter)

    temp_dir, zip_file_path = ReferenceAudioService.generate_audio_list_zip(audio_list)

    return ResponseResult(data={
        "temp_dir": temp_dir,
        "zip_file_path": zip_file_path,
    }, msg="生成成功")


@router.post("/download_audio_list_zip")
async def download_audio_list_zip(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    file_path = form_data.get('file_path')
    temp_dir = form_data.get('temp_dir')
    file_name = form_data.get('file_name')

    if not file_name.endswith(".zip"):
        file_name += ".zip"

    # 文件读取生成器
    def file_iterator(file_path2: str):
        with open(file_path2, "rb") as f:
            while chunk := f.read(8192):  # 每次读取 8KB
                yield chunk

    # 在响应完成后删除文件
    background_tasks.add_task(delete_directory, temp_dir)

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # URL 编码 UTF-8 文件名
    encoded_filename = urllib.parse.quote(file_name)

    # 修复响应头
    headers = {
        'Content-Disposition': f'attachment; filename="{file_name.encode("ascii", "ignore").decode()}";'
                               f' filename*=UTF-8\'\'{encoded_filename}',
        'Content-Type': 'application/zip',
        'Content-Length': str(file_size),  # 文件总大小
    }

    # 使用 StreamingResponse 返回 BytesIO 对象
    return StreamingResponse(file_iterator(file_path), headers=headers)
