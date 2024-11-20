from fastapi import APIRouter, Request

from server.bean.tts_correction.obj_tts_correction_task import ObjTtsCorrectionTaskFilter, ObjTtsCorrectionTask
from server.bean.tts_correction.obj_tts_correction_task_detail import ObjTtsCorrectionTaskDetailFilter, \
    ObjTtsCorrectionTaskDetail
from server.common.response_result import ResponseResult
from server.service.tts_correction.tts_correction_service import TtsCorrectionService
from server.util.util import str_to_int

router = APIRouter(prefix="/correction")


@router.post("/get_tts_correction_task_list")
async def get_tts_correction_task_list(request: Request):
    form_data = await request.form()
    task_filter = ObjTtsCorrectionTaskFilter(form_data)

    count = TtsCorrectionService.find_count(task_filter)
    task_list = TtsCorrectionService.find_list(task_filter)

    if task_list is not None and len(task_list) > 0:
        for task in task_list:
            task.detail_count = TtsCorrectionService.find_detail_count(ObjTtsCorrectionTaskDetailFilter({
                'task_id': task.id
            }))

    return ResponseResult(data=task_list, count=count)


@router.post("/get_tts_correction_task_by_id")
async def get_tts_correction_task_by_id(request: Request):
    form_data = await request.form()

    id = str_to_int(form_data.get('id'))

    if id < 1:
        return ResponseResult(code=1, msg="id is invalid")

    task = TtsCorrectionService.find_task_by_id(id)

    return ResponseResult(data=task)


def get_tts_correction_from_json(form_data: dict) -> ObjTtsCorrectionTask:
    task = ObjTtsCorrectionTask(
        task_name=form_data.get('taskName'),
        text_id=form_data.get('textId'),
        product_id=form_data.get('productId'),
        remark=form_data.get('remark')
    )

    detail_list = form_data.get('taskDetailList')

    task_detail_list = []
    for detail in detail_list:
        task_detail_list.append(ObjTtsCorrectionTaskDetail(
            text_content=detail.get('textContent'),
            text_index=detail.get('textIndex')
        ))
    task.detail_list = task_detail_list

    return task


@router.post("/add_tts_correction_task")
async def add_tts_correction_task(request: Request):
    form_data = await request.form()

    task = get_tts_correction_from_json(form_data)
    task_detail_list = task.detail_list

    task_id = TtsCorrectionService.add_tts_correction_task(task)

    if task_id < 1:
        return ResponseResult(code=1, msg="add tts correction task failed")

    for detail in task_detail_list:
        detail.task_id = task_id
        detail.status = 0
        detail.audio_path = ''
        detail.asr_text = ''
        detail.asr_text_similarity = 0
        detail.audio_status = 0

    TtsCorrectionService.batch_add_tts_correction_task_detail(task_detail_list)

    return ResponseResult(data=task)
