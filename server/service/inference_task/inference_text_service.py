from server.bean.text.obj_inference_text import ObjInferenceTextFilter, ObjInferenceText
from server.dao.inference_task.inference_text_dao import InferenceTextDao


class InferenceTextService:
    @staticmethod
    def find_count(audio_filter: ObjInferenceTextFilter) -> int:
        return InferenceTextDao.find_count(audio_filter)

    @staticmethod
    def find_list(audio_filter: ObjInferenceTextFilter) -> list[ObjInferenceText]:
        return InferenceTextDao.find_list(audio_filter)

    @staticmethod
    def find_one_by_id(text_id: int) -> ObjInferenceText:
        text_list = InferenceTextDao.find_list(ObjInferenceTextFilter({
            "id": text_id
        }))
        
        if len(text_list) > 0:
            return text_list[0]
        
        return None

    @staticmethod
    def insert_inference_text(text: ObjInferenceText) -> int:
        return InferenceTextDao.insert_inference_text(text)

    @staticmethod
    def delete_inference_text_by_id(text_id) -> int:
        return InferenceTextDao.delete_inference_text_by_id(text_id)

    @staticmethod
    def update_inference_text_by_id(text: ObjInferenceText):
        return InferenceTextDao.update_inference_text_by_id(text)

