from server.bean.base_model import BaseModel
from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudio


class ObjReferenceAudioCompareDetail(BaseModel):
    def __init__(self, id=None, task_id=None, compare_audio_id=None, score=None, create_time=None,
                 compare_audio: ObjReferenceAudio = None):
        self.id = id  # 自增编号
        self.task_id = task_id  # 比对任务id
        self.compare_audio_id = compare_audio_id  # 被比较的音频id
        self.score = score  # 相似度分值
        self.create_time = create_time  # 创建时间，默认为当前时间
        self.compare_audio = compare_audio

    def __repr__(self):
        return f"ReferenceAudioCompareDetail(id={self.id}, task_id={self.task_id}, " \
               f"compare_audio_id={self.compare_audio_id}, score={self.score}, " \
               f"create_time='{self.create_time}')"
