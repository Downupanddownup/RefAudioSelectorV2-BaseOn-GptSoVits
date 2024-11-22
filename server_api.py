import os
import sys
import time
import webbrowser

from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudio

sys.path.append(os.getcwd())
from server.bean.finished_product.finished_product_manager import ObjFinishedProductManager
from server.bean.finished_product.product_param_config_template import ProductParamConfigTemplate

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

# Mount static files directory
app.mount("/static", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    import uvicorn

    product_list = []
    product = ObjFinishedProductManager(
        name="test",
        gpt_sovits_version="v1.0",
        gpt_model_name="gpt_model_name",
        gpt_model_path="gpt_model_path",
        vits_model_name="vits_model_name",
        vits_model_path="vits_model_path",
        audio_id=1,
        audio_name="audio_name",
        audio_path="audio_path",
        content="content",
        language="zh",
        audio_length=1,
        top_k=1,
        top_p=1,
        temperature=1,
        text_delimiter="text_delimiter",
        speed=1,
        score=1,
        remark="remark",
    )
    sound_fusion_list = []
    sound_fusion = ObjSoundFusionAudio(
        audio_name="audio_name",
        audio_path="audio_path",
        content="content",
        language="zh",
        audio_length=1,
        remark="remark",
    )
    sound_fusion_list.append(sound_fusion)
    product.set_sound_fusion_list(sound_fusion_list)

    product_list.append(product)

    url = f"http://localhost:{config_params.service_port}/static/main.html?apiPort={config_params.api_port}"
    print(f"Open url: {url}")
    # webbrowser.open(url)
    # 测试
    db_config.init_master_db_path()
    role = SystemService.get_valid_role()
    if role:
        db_config.update_db_path(role)

    config_template = ProductParamConfigTemplate(db_config.role.name, False, True, product_list)
    zip_in_memory = config_template.generate_zip_file()

    # uvicorn.run(app, host="0.0.0.0", port=int(config_params.service_port))
