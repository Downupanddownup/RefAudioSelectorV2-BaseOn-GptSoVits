# -*- coding:utf-8 -*-
import os
import sys
import traceback
from funasr import AutoModel

sys.path.append(os.getcwd())

from server.common.log_config import logger
import server.common.config_params as params


class LanguageModel:
    def __init__(self, language='zh'):
        if not language:
            raise ValueError(f'Unsupported language: {language}')
        language = language.lower()
        if language.lower() not in ['zh', 'yue']:
            raise ValueError(f'Unsupported language: {language}')
        self.model = init(language)

    def generate(self, path):
        try:
            return self.model.generate(input=path)[0]["text"]
        except:
            logger.error(traceback.format_exc())


def init(language):
    # model_dir = 'server/tool/asr/models/'
    # 获取当前脚本所在的绝对路径
    current_dir = os.getcwd()
    # 计算上上级目录的绝对路径
    api_dir = os.path.join(current_dir, params.gsv2_dir)
    model_dir = api_dir+'/tools/asr/models/'
    path_vad = model_dir + 'speech_fsmn_vad_zh-cn-16k-common-pytorch'
    path_punc = model_dir + 'punc_ct-transformer_zh-cn-common-vocab272727-pytorch'
    path_vad = path_vad if os.path.exists(path_vad) else "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
    path_punc = path_punc if os.path.exists(path_punc) else "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"
    vad_model_revision = punc_model_revision = "v2.0.4"

    if (language == "zh"):
        path_asr = model_dir + 'speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch'
        path_asr = path_asr if os.path.exists(
            path_asr) else "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
        model_revision = "v2.0.4"
    else:
        path_asr = model_dir + 'speech_UniASR_asr_2pass-cantonese-CHS-16k-common-vocab1468-tensorflow1-online'
        path_asr = path_asr if os.path.exists(
            path_asr) else "iic/speech_UniASR_asr_2pass-cantonese-CHS-16k-common-vocab1468-tensorflow1-online"
        model_revision = "master"
        path_vad = path_punc = vad_model_revision = punc_model_revision = None  # ##友情提示：粤语带VAD识别可能会有少量shape
        # 不对报错的，但是不带VAD可以.不带vad只能分阶段单独加标点。不过标点模型对粤语效果真的不行…

    return AutoModel(
        model=path_asr,
        model_revision=model_revision,
        vad_model=path_vad,
        vad_model_revision=vad_model_revision,
        punc_model=path_punc,
        punc_model_revision=punc_model_revision,
    )
