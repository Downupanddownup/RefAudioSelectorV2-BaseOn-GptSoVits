import sys
import os
import signal
import subprocess
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

print("Current working directory:", os.getcwd())
# 将项目根目录添加到 sys.path
sys.path.append(os.getcwd())

from server.api.inference_params_manager import InferenceParamsManager, InferenceParams
import server.common.config_params as params

# 获取当前脚本所在的绝对路径
current_dir = os.getcwd()

print('gsv2_dir', params.gsv2_dir)
# 计算上上级目录的绝对路径
api_dir = os.path.join(current_dir, params.gsv2_dir)

# 将上上级目录添加到模块搜索路径中
sys.path.append(api_dir)

sys.path.append("%s/GPT_SoVITS" % api_dir)

# 传递命令行参数
sys.argv.extend(["--hubert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-hubert-base")])
sys.argv.extend(["--bert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")])
sys.argv.extend(["--sovits_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s2G488k.pth")])
sys.argv.extend(["--gpt_path",
                 os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt")])

# sys.argv.extend(["--stream_mode", 'normal'])
# sys.argv.extend(["--media_type", 'aac'])

# 设置环境变量
os.environ['g2pw_model_dir'] = os.path.join(api_dir, "GPT_SoVITS/text/G2PWModel")
os.environ['g2pw_model_source'] = os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")

inference_params_manager = InferenceParamsManager()

# 导入模块中的所有内容
from api import *
import api

logger.info(f'stream_mode={api.stream_mode}；media_type={api.media_type}')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


@app.get("/status")
async def status():
    # 发送 SIGINT 信号给当前进程
    return {"message": "server is running"}


@app.post("/ras/set_default_params")
async def set_default_params(request: Request):
    json_post_raw = await request.json()
    inference_params_manager.set_default_params(InferenceParams(
        refer_wav_path=json_post_raw.get("refer_wav_path"),
        prompt_text=json_post_raw.get("prompt_text"),
        prompt_language=json_post_raw.get("prompt_language"),
        cut_punc=json_post_raw.get("cut_punc"),
        top_k=json_post_raw.get("top_k", None),
        top_p=json_post_raw.get("top_p", None),
        temperature=json_post_raw.get("temperature", None),
        speed=json_post_raw.get("speed", None),
        inp_refs=json_post_raw.get("inp_refs", []),
    ))

    temp_stream_mode = json_post_raw.get("stream_mode", None)
    temp_media_type = json_post_raw.get("media_type", None)

    logger.info(f'stream_mode={temp_stream_mode}；media_type={temp_media_type}')

    if temp_stream_mode is not None:
        temp_stream_mode = int(temp_stream_mode)
        # 流式返回模式
        if temp_stream_mode == 1:
            api.stream_mode = "normal"
            logger.info("流式返回已开启")
        else:
            api.stream_mode = "close"
            logger.info("流式返回已关闭")
    if temp_media_type is not None:
        # global media_type
        # 音频编码格式
        if temp_media_type.lower() in ["aac", "ogg"]:
            api.media_type = temp_media_type.lower()
        elif api.stream_mode == "close":
            api.media_type = "wav"
        else:
            api.media_type = "ogg"
        logger.info(f"编码格式: {api.media_type}")

    print(inference_params_manager.default_params)
    return 'ok'


@app.post("/ras")
async def tts_endpoint(request: Request):
    json_post_raw = await request.json()
    params = inference_params_manager.get_real_params(InferenceParams(
        refer_wav_path=json_post_raw.get("refer_wav_path"),
        prompt_text=json_post_raw.get("prompt_text"),
        prompt_language=json_post_raw.get("prompt_language"),
        cut_punc=json_post_raw.get("cut_punc"),
        top_k=json_post_raw.get("top_k", None),
        top_p=json_post_raw.get("top_p", None),
        temperature=json_post_raw.get("temperature", None),
        speed=json_post_raw.get("speed", None),
        inp_refs=json_post_raw.get("inp_refs", [])
    ))
    print(params)
    print(f'text:{json_post_raw.get("text")};text_language:{json_post_raw.get("text_language")}')
    return handle(
        refer_wav_path=params.refer_wav_path,
        prompt_text=params.prompt_text,
        prompt_language=params.prompt_language,
        text=json_post_raw.get("text"),
        text_language=json_post_raw.get("text_language"),
        cut_punc=params.cut_punc,
        top_k=params.top_k,
        top_p=params.top_p,
        temperature=params.temperature,
        speed=params.speed,
        inp_refs=params.inp_refs,
        sample_steps=32,
        if_sr=True
    )


@app.get("/ras")
async def tts_endpoint(
        refer_wav_path: str = None,
        prompt_text: str = None,
        prompt_language: str = None,
        text: str = None,
        text_language: str = None,
        cut_punc: str = None,
        top_k: int = None,
        top_p: float = None,
        temperature: float = None,
        speed: float = None,
        inp_refs: list = Query(default=[])
):
    params = inference_params_manager.get_real_params(InferenceParams(
        refer_wav_path=refer_wav_path,
        prompt_text=prompt_text,
        prompt_language=prompt_language,
        cut_punc=cut_punc,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        speed=speed,
        inp_refs=inp_refs
    ))
    print(params)
    print(f'text:{text};text_language:{text_language}')
    # text = '这个提纲提供了故事的基本框架，包含了冲突、转折点以及最终的解决办法，旨在探索人类的本质以及与环境的关系。'
    return handle(
        refer_wav_path=params.refer_wav_path,
        prompt_text=params.prompt_text,
        prompt_language=params.prompt_language,
        text=text,
        text_language=text_language,
        cut_punc=params.cut_punc,
        top_k=params.top_k,
        top_p=params.top_p,
        temperature=params.temperature,
        speed=params.speed,
        inp_refs=params.inp_refs,
        sample_steps=32,
        if_sr=True
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(params.api_port), workers=1)
