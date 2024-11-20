from server.bean.base_model import BaseModel


class ObjTtsCorrectionTask(BaseModel):
    def __init__(self, id=0, task_name=None, text_id=None, product_id=None, inference_status=None, remark=None, create_time=None):
        self.id = id  # 自增编号
        self.task_name = task_name  # 任务名称
        self.text_id = text_id  # 推理文本id
        self.product_id = product_id  # 成品Id
        self.inference_status = inference_status  # 推理状态 0 待推理 1 推理中 2 推理完成
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间

    def __str__(self):
        return (f"TabObjTtsCorrectionTask(id={self.id}, task_name='{self.task_name}', "
                f"text_id={self.text_id}, product_id={self.product_id}, "
                f"inference_status={self.inference_status}, remark='{self.remark}', "
                f"create_time='{self.create_time}')")