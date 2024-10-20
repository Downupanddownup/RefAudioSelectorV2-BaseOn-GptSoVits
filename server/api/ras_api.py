import sys
import os
import signal
import subprocess
import uvicorn

# 获取当前脚本所在的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 计算上上级目录的绝对路径
api_dir = os.path.join(current_dir, "../../../GPT-SoVITS-v2-240807")

# 将上上级目录添加到模块搜索路径中
sys.path.append(api_dir)

sys.path.append("%s/GPT_SoVITS" % api_dir)

# 传递命令行参数
sys.argv.extend(["--hubert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-hubert-base")])
sys.argv.extend(["--bert_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")])
sys.argv.extend(["--sovits_path", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s2G488k.pth")])
sys.argv.extend(["--gpt_path",
                 os.path.join(api_dir, "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt")])
sys.argv.extend(["--g2pw_model_dir", os.path.join(api_dir, "GPT_SoVITS/text/G2PWModel")])
sys.argv.extend(["--g2pw_model_source", os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")])


# 设置环境变量
os.environ['g2pw_model_dir'] = os.path.join(api_dir, "GPT_SoVITS/text/G2PWModel")
os.environ['g2pw_model_source'] = os.path.join(api_dir, "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large")

# 导入模块中的所有内容
from api import *


@app.get("/status")
async def status():
    # 发送 SIGINT 信号给当前进程
    return {"message": "server is running"}


@app.get("/stop")
async def stop_service():
    # 发送 SIGINT 信号给当前进程
    os.kill(os.getpid(), signal.SIGTERM)


@app.post("/ras")
async def tts_endpoint(request: Request):
    json_post_raw = await request.json()
    print(json_post_raw)
    return handle(
        json_post_raw.get("refer_wav_path"),
        json_post_raw.get("prompt_text"),
        json_post_raw.get("prompt_language"),
        json_post_raw.get("text"),
        json_post_raw.get("text_language"),
        json_post_raw.get("cut_punc"),
        json_post_raw.get("top_k", 10),
        json_post_raw.get("top_p", 1.0),
        json_post_raw.get("temperature", 1.0),
        json_post_raw.get("speed", 1.0)
    )


@app.get("/ras")
async def tts_endpoint(
        refer_wav_path: str = None,
        prompt_text: str = None,
        prompt_language: str = None,
        text: str = None,
        text_language: str = None,
        cut_punc: str = None,
        top_k: int = 10,
        top_p: float = 1.0,
        temperature: float = 1.0,
        speed: float = 1.0
):
    return handle(refer_wav_path, prompt_text, prompt_language, text, text_language, cut_punc, top_k, top_p,
                  temperature, speed)


if __name__ == "__main__":
    print(f'ras_api的进程pid{os.getpid()}')
    uvicorn.run(app, host="0.0.0.0", port=8001, workers=1)
