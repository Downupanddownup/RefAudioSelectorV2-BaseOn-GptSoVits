import os
import sys
import time
import webbrowser

sys.path.append(os.getcwd())

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from server.common.custom_exception import CustomException
from server.common.log_config import logger
from server.common.ras_api_monitor import RasApiMonitor
from server.common.response_result import ResponseResult
from server.controller.reference_audio.reference_audio_controller import router as audio_router
from server.controller.inference_task.inference_task_controller import router as task_router
from server.controller.long_text_inference.long_text_inference_controller import router as long_text_router
from server.controller.result_evaluation.result_evaluation_controller import router as result_evaluation_router
from server.controller.finished_product.finished_product_controller import router as finished_product_router
from server.controller.system.system_controller import router as system_router
from server.controller.sound_fusion.sound_fusion_controller import router as sound_fusion_router
from server.controller.tts_correction.tts_correction_controller import router as tts_correction_router
from server.controller.text.text_controller import router as text_controller
from server.dao.data_base_manager import db_config
from server.common import config_params
from server.service.system.system_service import SystemService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


# 自定义异常处理器
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    result = ResponseResult(code=1, msg=exc.message)
    return JSONResponse(content=result.to_dict(), status_code=200)


# 注册默认的异常处理器
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc: Exception):
    logger.error(exc)
    result = ResponseResult(code=1, msg=str(exc))
    return JSONResponse(content=result.to_dict(), status_code=500)


# 注册路由
app.include_router(audio_router)
app.include_router(task_router)
app.include_router(long_text_router)
app.include_router(result_evaluation_router)
app.include_router(finished_product_router)
app.include_router(system_router)
app.include_router(sound_fusion_router)
app.include_router(tts_correction_router)
app.include_router(text_controller)

# Mount static files directory
app.mount("/static", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    import uvicorn

    url = f"http://localhost:{config_params.service_port}/static/main.html?apiPort={config_params.api_port}"
    print(f"Open url: {url}")
    webbrowser.open(url)
    # 测试
    db_config.init_master_db_path()
    role = SystemService.get_valid_role()
    if role:
        db_config.update_db_path(role)
    uvicorn.run(app, host="127.0.0.1", port=config_params.service_port)
