from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudioFilter
from server.bean.reference_audio.obj_reference_audio_compare_detail import ObjReferenceAudioCompareDetail
from server.bean.reference_audio.obj_reference_audio_compare_task import ObjReferenceAudioCompareTask
from server.dao.reference_audio.reference_audio_compare_dao import ReferenceAudioCompareDao
from server.service.reference_audio.reference_audio_service import ReferenceAudioService
from server.service.reference_audio.reference_category_service import ReferenceCategoryService


class ReferenceAudioCompareService:
    @staticmethod
    def insert_task(task: ObjReferenceAudioCompareTask) -> int:
        return ReferenceAudioCompareDao.insert_task(task)

    @staticmethod
    def get_task_by_id(task_id: int) -> ObjReferenceAudioCompareTask:
        return ReferenceAudioCompareDao.get_task_by_id(task_id)

    @staticmethod
    def update_task_to_fail(task_id: int) -> int:
        return ReferenceAudioCompareDao.update_task_status(task_id, 3)

    @staticmethod
    def update_task_to_start(task_id: int) -> int:
        return ReferenceAudioCompareDao.update_task_status(task_id, 1)

    @staticmethod
    def update_task_to_finish(task_id: int) -> int:
        return ReferenceAudioCompareDao.update_task_status(task_id, 2)

    @staticmethod
    def batch_insert_task_detail(detail_list: list[ObjReferenceAudioCompareDetail]) -> int:
        return ReferenceAudioCompareDao.batch_insert_task_detail(detail_list)

    @staticmethod
    def get_last_finish_task_by_audio_id(audio_id: int) -> ObjReferenceAudioCompareTask:
        return ReferenceAudioCompareDao.get_last_finish_task_by_audio_id(audio_id)

    @staticmethod
    def get_compare_detail_list_by_task_id(task_id: int) -> list[ObjReferenceAudioCompareDetail]:
        detail_list = ReferenceAudioCompareDao.get_compare_detail_list_by_task_id(task_id)
        if len(detail_list) == 0:
            return detail_list
        audio_ids_str = ','.join(str(x.compare_audio_id) for x in detail_list)
        audio_list = ReferenceAudioService.find_list(ObjReferenceAudioFilter({'audio_ids_str': audio_ids_str}))
        for detail in detail_list:
            detail.compare_audio = next(filter(lambda x: x.id == detail.compare_audio_id, audio_list), None)
        return detail_list

    @staticmethod
    def change_audio_category(task_id: int, target_category: str, limit_score: float) -> int:
        ReferenceCategoryService.add_category(target_category)
        compare_audio_list = ReferenceAudioCompareService.get_compare_detail_list_by_task_id(task_id)
        change_audio_list = []
        for compare_audio in compare_audio_list:
            if compare_audio.score >= limit_score and compare_audio.compare_audio.category != target_category:
                change_audio_list.append(compare_audio.compare_audio)
        change_audio_id_str = ','.join(str(x.id) for x in change_audio_list)
        return ReferenceAudioService.update_audio_category(change_audio_id_str, target_category)
