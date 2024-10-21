from fastapi import APIRouter, Request

from server.common.ras_api_monitor import RasApiMonitor
from server.common.response_result import ResponseResult

router = APIRouter(prefix="/inference")


@router.post("/start_ras_api")
async def start_ras_api():
    if RasApiMonitor.start_service():
        return ResponseResult(msg="api服务已启动")
    return ResponseResult(msg="api服务启动失败")


@router.post("/stop_ras_api")
async def stop_ras_api():
    if RasApiMonitor.stop_service():
        return ResponseResult(msg="api服务已关闭")
    return ResponseResult(msg="api服务关闭失败")
