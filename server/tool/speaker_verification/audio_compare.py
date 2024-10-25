import os
import sys
import traceback
from modelscope.pipelines import pipeline
sys.path.append(os.getcwd())
from server.common.log_config import logger

speaker_verification_models = {
    'speech_campplus_sv_zh-cn_16k-common': {
        'task': 'speaker-verification',
        'model': 'server/tool/speaker_verification/models/speech_campplus_sv_zh-cn_16k-common',
        'model_revision': 'v1.0.0'
    },
    'speech_eres2net_sv_zh-cn_16k-common': {
        'task': 'speaker-verification',
        'model': 'server/tool/speaker_verification/models/speech_eres2net_sv_zh-cn_16k-common',
        'model_revision': 'v1.0.5'
    }
}


def init_model(model_type='speech_campplus_sv_zh-cn_16k-common'):
    models = speaker_verification_models
    return pipeline(
        task=models[model_type]['task'],
        model=models[model_type]['model'],
        model_revision=models[model_type]['model_revision']
    )


sv_pipeline = init_model()


def compare(audio_path_1, audio_path_2):
    try:
        return sv_pipeline([audio_path_1, audio_path_2])['score']
    except:
        logger.error(traceback.format_exc())
