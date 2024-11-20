from server.bean.tts_correction.obj_tts_correction_task import ObjTtsCorrectionTask, ObjTtsCorrectionTaskFilter
from server.bean.tts_correction.obj_tts_correction_task_detail import ObjTtsCorrectionTaskDetailFilter, \
    ObjTtsCorrectionTaskDetail
from server.dao.tts_correction.tts_correction_dao import TtsCorrectionDao


class TtsCorrectionService:
    @staticmethod
    def find_count(task_filter: ObjTtsCorrectionTaskFilter) -> int:
        return TtsCorrectionDao.find_count(task_filter)

    @staticmethod
    def find_list(task_filter: ObjTtsCorrectionTaskFilter) -> list[ObjTtsCorrectionTask]:
        return TtsCorrectionDao.find_list(task_filter)

    @staticmethod
    def find_detail_count(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> int:
        return TtsCorrectionDao.find_detail_count(detail_filter)

    @staticmethod
    def find_detail_list(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> list[ObjTtsCorrectionTaskDetail]:
        return TtsCorrectionDao.find_detail_list(detail_filter)

    @staticmethod
    def find_task_by_id(task_id: int) -> ObjTtsCorrectionTask:
        task_filter = ObjTtsCorrectionTaskFilter({
            'id': task_id
        })
        task_list = TtsCorrectionService.find_list(task_filter)

        if task_list is None or len(task_list) == 0:
            return None

        task = task_list[0]

        detail_list = TtsCorrectionService.find_detail_list(ObjTtsCorrectionTaskDetailFilter({
            'task_id': task_id
        }))

        task.detail_list = detail_list

        return task

    @staticmethod
    def add_tts_correction_task(task: ObjTtsCorrectionTask) -> int:
        return TtsCorrectionDao.add_tts_correction_task(task)

    @staticmethod
    def batch_add_tts_correction_task_detail(task_detail_list: list[ObjTtsCorrectionTaskDetail]) -> int:
        return TtsCorrectionDao.batch_add_tts_correction_task_detail(task_detail_list)
