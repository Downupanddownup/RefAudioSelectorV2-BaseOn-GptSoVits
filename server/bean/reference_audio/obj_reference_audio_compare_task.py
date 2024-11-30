from server.bean.base_model import BaseModel


class ObjReferenceAudioCompareTask(BaseModel):
    def __init__(self, id=None, audio_id=None, category_names=None, status=0, remark='', create_time=None):
        self.id = id  # 自增编号
        self.audio_id = audio_id  # 音频id
        self.category_names = category_names  # 比对目录名称
        self.status = status  # 任务状态：0 待执行 1 执行中 2 已完成 3 失败
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间，默认为当前时间

    def __repr__(self):
        return f"ReferenceAudioCompareTask(id={self.id}, audio_id={self.audio_id}, status={self.status}, remark='{self.remark}', " \
               f"category_names='{self.category_names}', create_time='{self.create_time}')"
