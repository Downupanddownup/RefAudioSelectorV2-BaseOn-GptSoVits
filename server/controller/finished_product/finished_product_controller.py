from fastapi import APIRouter, Request

from server.bean.finished_product.finished_product_manager import ObjFinishedProductManagerFilter, \
    ObjFinishedProductManager
from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudio
from server.common.response_result import ResponseResult
from server.service.finished_product.finished_product_service import FinishedProductService
from server.service.inference_task.model_manager_service import ModelManagerService
from server.util.util import str_to_int

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
    product_id = str_to_int(form_data.get('product_id'))
    if product_id < 1 or product_id is None:
        return ResponseResult(code=1, msg="参数错误")

    product = FinishedProductService.find_by_id(product_id)
    if product is None:
        return ResponseResult(code=1, msg="未找到相关数据")

    gpt_model_list = ModelManagerService.get_gpt_model_list()
    vits_model_list = ModelManagerService.get_vits_model_list()

    return ResponseResult(data={
        "task": product,
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


@router.post("/add_finished_product")
async def add_finished_product(request: Request):
    form_data = await request.json()

    product = get_finished_product_from_json(form_data)

    product_id = FinishedProductService.add_finished_product(product)

    return ResponseResult(data={"product_id": product_id})


@router.post("/update_finished_product")
async def update_finished_product(request: Request):
    form_data = await request.json()

    product = get_finished_product_from_json(form_data)
    if product.id is None or product.id < 1:
        return ResponseResult(code=1, msg="参数错误")

    result = FinishedProductService.update_finished_product(product)

    if result == 0:
        return ResponseResult(code=1, msg="修改失败")

    return ResponseResult(msg="修改成功")
