import os
import time
import webbrowser

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
from server.controller.audio_packaging.audio_packaging_controller import router as audio_packaging_router
from server.controller.common_controller import router as common_router

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
app.include_router(audio_packaging_router)
app.include_router(common_router)

# Mount static files directory
app.mount("/static", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    import uvicorn

    url = "http://localhost:8000/static/main.html"
    # webbrowser.open(url)
    uvicorn.run(app, host="0.0.0.0", port=8000)
