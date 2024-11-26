import urllib.parse
import os
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import StreamingResponse

from server.bean.finished_product.finished_product_manager import ObjFinishedProductManagerFilter, \
    ObjFinishedProductManager
from server.bean.finished_product.product_param_config_template import ProductParamConfigTemplate
from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudio
from server.common.response_result import ResponseResult
from server.dao.data_base_manager import db_config
from server.service.finished_product.finished_product_service import FinishedProductService
from server.service.inference_task.model_manager_service import ModelManagerService
from server.util.util import str_to_int, delete_directory

router = APIRouter(prefix="/product")


@router.post("/get_finished_product_list")
async def get_finished_product_list(request: Request):
    form_data = await request.form()
    audio_filter = ObjFinishedProductManagerFilter(form_data)

    count = FinishedProductService.find_count(audio_filter)
    audio_list = FinishedProductService.find_list(audio_filter)

    return ResponseResult(data=audio_list, count=count)


@router.post("/load_finished_product_detail")
async def load_finished_product_detail(request: Request):
    form_data = await request.form()

    product = None

    product_id = str_to_int(form_data.get('product_id'))
    if product_id > 0:
        product = FinishedProductService.find_by_id(product_id)

    gpt_model_list = ModelManagerService.get_gpt_model_list()
    vits_model_list = ModelManagerService.get_vits_model_list()

    return ResponseResult(data={
        "product": product,
        "gptModels": gpt_model_list,
        "vitsModels": vits_model_list
    })


def get_finished_product_from_json(form_data: dict) -> ObjFinishedProductManager:
    sound_fusion_str_list = form_data.get('inpRefs')
    sound_fusion_list = []
    for sound_fusion_str in sound_fusion_str_list:
        sound_fusion_list.append(ObjSoundFusionAudio(
            id=sound_fusion_str.get('id'),
            role_name=sound_fusion_str.get('roleName'),
            audio_name=sound_fusion_str.get('audioName'),
            audio_path=sound_fusion_str.get('audioPath'),
            content=sound_fusion_str.get('content'),
            language=sound_fusion_str.get('language'),
            category=sound_fusion_str.get('category'),
            audio_length=sound_fusion_str.get('audioLength'),
            remark=sound_fusion_str.get('remark')
        ))

    product = ObjFinishedProductManager(
        id=str_to_int(form_data.get('id'), 0),
        name=form_data.get('name'),
        category=form_data.get('category'),
        gpt_sovits_version=form_data.get('gptSovitsVersion'),
        gpt_model_name=form_data.get('gptModelName'),
        gpt_model_path=form_data.get('gptModelPath'),
        vits_model_name=form_data.get('vitsModelName'),
        vits_model_path=form_data.get('vitsModelPath'),
        audio_id=str_to_int(form_data.get('audioId'), 0),
        audio_name=form_data.get('audioName'),
        audio_path=form_data.get('audioPath'),
        content=form_data.get('content'),
        language=form_data.get('language'),
        audio_length=str_to_int(form_data.get('audioLength'), 0),
        top_k=form_data.get('topK'),
        top_p=form_data.get('topP'),
        temperature=form_data.get('temperature'),
        text_delimiter=form_data.get('textDelimiter'),
        speed=form_data.get('speed'),
        score=form_data.get('score'),
        remark=form_data.get('remark')
    )

    product.set_sound_fusion_list(sound_fusion_list)

    return product


@router.post("/save_finished_product")
async def save_finished_product(request: Request):
    form_data = await request.json()

    product = get_finished_product_from_json(form_data)

    product_id = product.id

    if product_id is None or product_id < 1:
        product_id = FinishedProductService.add_finished_product(product)
    else:
        result = FinishedProductService.update_finished_product(product)
        if result == 0:
            return ResponseResult(code=1, msg="修改失败")

    return ResponseResult(data={"product_id": product_id}, msg="保存成功")


@router.post("/generate_finished_product_zip")
async def generate_finished_product_zip(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    product_ids = form_data.get('product_ids')
    is_merge = str_to_int(form_data.get('is_merge'), 0)
    need_model = str_to_int(form_data.get('need_model'), 1)

    product_list = FinishedProductService.find_list(ObjFinishedProductManagerFilter({'ids': product_ids}))

    config_template = ProductParamConfigTemplate(db_config.role.name, is_merge == 1, need_model == 1, product_list)
    temp_dir, zip_file_path = config_template.generate_zip_file()

    return ResponseResult(data={
        "temp_dir": temp_dir,
        "zip_file_path": zip_file_path,
    }, msg="生成成功")


@router.post("/download_product_file")
async def download_product_file(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    file_path = form_data.get('file_path')
    temp_dir = form_data.get('temp_dir')
    file_name = form_data.get('file_name')

    if not file_name.endswith(".zip"):
        file_name += ".zip"

    # 文件读取生成器
    def file_iterator(file_path: str):
        with open(file_path, "rb") as f:
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
