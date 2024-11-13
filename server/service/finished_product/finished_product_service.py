from server.bean.finished_product.finished_product_manager import ObjFinishedProductManager, \
    ObjFinishedProductManagerFilter
from server.dao.finished_product.finished_product_dao import FinishedProductDao


class FinishedProductService:
    @staticmethod
    def find_count(audio_filter: ObjFinishedProductManagerFilter) -> int:
        return FinishedProductDao.find_count(audio_filter)

    @staticmethod
    def find_list(audio_filter: ObjFinishedProductManagerFilter) -> list[ObjFinishedProductManager]:
        return FinishedProductDao.find_list(audio_filter)

    @staticmethod
    def find_by_id(product_id: int) -> ObjFinishedProductManager:
        product_list = FinishedProductService.find_list(ObjFinishedProductManagerFilter({'id': product_id}))
        return product_list[0] if len(product_list) > 0 else None

    @staticmethod
    def add_finished_product(product: ObjFinishedProductManager) -> int:
        return FinishedProductDao.add_finished_product(product)

    @staticmethod
    def update_finished_product(product: ObjFinishedProductManager) -> int:
        return FinishedProductDao.update_finished_product(product)
