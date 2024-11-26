from fastapi import APIRouter, Request

from server.common.ras_api_monitor import RasApiMonitor
from server.common.response_result import ResponseResult
from server.service.inference_task.model_manager_service import ModelManagerService
from server.util.util import str_to_int

router = APIRouter(prefix="/inference")


@router.post("/start_ras_api")
async def start_ras_api(request: Request):
    data_form = await request.form()
    stream_mode = str_to_int(data_form.get('streamMode'),0)
    media_type = data_form.get('mediaType')
    if RasApiMonitor.start_service(stream_mode == 1, media_type):
        return ResponseResult(msg="api服务已启动")
    return ResponseResult(msg="api服务启动失败")


@router.post("/stop_ras_api")
async def stop_ras_api():
    if RasApiMonitor.stop_service():
        return ResponseResult(msg="api服务已关闭")
    return ResponseResult(msg="api服务关闭失败")


@router.post("/load_models")
async def load_models(request: Request):

    gpt_model_list = ModelManagerService.get_gpt_model_list()
    vits_model_list = ModelManagerService.get_vits_model_list()

    return ResponseResult(data={
        "gptModels": gpt_model_list,
        "vitsModels": vits_model_list
    })