from fastapi import APIRouter, Request

from server.bean.system.sys_cache_constants import TextConstants
from server.bean.text.obj_inference_text import ObjInferenceTextFilter, ObjInferenceText
from server.common.response_result import ResponseResult
from server.service.inference_task.inference_text_service import InferenceTextService
from server.service.system.system_service import SystemService
from server.util.util import ValidationUtils, str_to_int

router = APIRouter(prefix="/text")



@router.post("/get_last_select_inference_text")
async def get_last_select_inference_text(request: Request):
    form_data = await request.form()

    text = None

    last_selected_id = SystemService.get_sys_cache(TextConstants.CACHE_TYPE, TextConstants.CACHE_KEY_LAST_SELECTED_ID)

    if last_selected_id:
        text = InferenceTextService.find_one_by_id(last_selected_id)

    return ResponseResult(data=text)


@router.post("/update_last_select_inference_text_id")
async def update_last_select_inference_text_id(request: Request):
    form_data = await request.form()

    text_id = form_data.get('text_id')

    SystemService.update_sys_cache(TextConstants.CACHE_TYPE, TextConstants.CACHE_KEY_LAST_SELECTED_ID, text_id)

    return ResponseResult()


@router.post("/get_inference_text_list")
async def get_inference_text_list(request: Request):
    form_data = await request.form()
    text_filter = ObjInferenceTextFilter(form_data)

    if ValidationUtils.is_empty(text_filter.order_by):
        text_filter.order_by = "id"
    if ValidationUtils.is_empty(text_filter.order_by_desc):
        text_filter.order_by_desc = "desc"

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
