from server.bean.base_model import BaseModel
from server.bean.finished_product.finished_product_manager import ObjFinishedProductManager
from server.bean.inference_task.obj_inference_text import ObjInferenceText
from server.bean.tts_correction.obj_tts_correction_task_detail import ObjTtsCorrectionTaskDetail
from server.common.filter import Filter
from server.util.util import str_to_int, ValidationUtils


class ObjTtsCorrectionTask(BaseModel):
    def __init__(self, id=0, task_name=None, text_id=None, product_id=None, inference_status=None, remark=None,
                 create_time=None,detail_list: list[ObjTtsCorrectionTaskDetail] = None,
                 product: ObjFinishedProductManager = None, text_obj: ObjInferenceText = None):
        self.id = id  # 自增编号
        self.task_name = task_name  # 任务名称
        self.text_id = text_id  # 推理文本id
        self.product_id = product_id  # 成品Id
        self.inference_status = inference_status  # 推理状态 0 待推理 1 推理中 2 推理完成
        self.remark = remark  # 备注
        self.create_time = create_time  # 创建时间
        self.detail_count = 0
        self.detail_list = detail_list
        self.product = product
        self.text_obj = text_obj

    def __str__(self):
        return (f"TabObjTtsCorrectionTask(id={self.id}, task_name='{self.task_name}', "
                f"text_id={self.text_id}, product_id={self.product_id}, "
                f"inference_status={self.inference_status}, remark='{self.remark}', "
                f"create_time='{self.create_time}')")


class ObjTtsCorrectionTaskFilter(Filter):
    def __init__(self, form_data):
        super().__init__(form_data)
        self.id = form_data.get('id')
        self.task_name = form_data.get('task_name')
        self.inference_status = str_to_int(form_data.get('inference_status'))

    def make_sql(self) -> []:
        sql = ''
        condition = []
        if not ValidationUtils.is_empty(self.id):
            sql += f" and id = ? "
            condition.append(f"{self.id}")

        if not ValidationUtils.is_empty(self.task_name):
            sql += f" and TaskName like ? "
            condition.append(f"%{self.task_name}%")

        if self.inference_status is not None and self.inference_status > -1:
            sql += f" and InferenceStatus = ? "
            condition.append(f"{self.inference_status}")

        return sql, tuple(condition)
