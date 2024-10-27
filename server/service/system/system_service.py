import os
from server.bean.system.sys_cache import SysCache
from server.common.log_config import logger
from server.dao.data_base_manager import db_config
from server.dao.system.system_dao import SystemDao


class SystemService:
    @staticmethod
    def get_sys_cache(cache_type: str, cache_key: str) -> str:
        cache = SystemDao.get_sys_cache(cache_type, cache_key)
        if cache is None:
            return None
        return cache.value

    @staticmethod
    def update_sys_cache(cache_type: str, cache_key: str, cache_value: str):
        cache = SystemDao.get_sys_cache(cache_type, cache_key)
        if cache is None:
            cache = SysCache(type=cache_type, key_name=cache_key, value=cache_value)
            SystemDao.insert_sys_cache(cache)
        else:
            cache.value = cache_value
            SystemDao.update_sys_cache(cache)

    @staticmethod
    def get_role_list():
        directory_path = db_config.get_slave_db_dir()
        subdirectories = []
        try:
            # 使用os.listdir获取目录下的所有条目
            entries = os.listdir(directory_path)

            # 遍历所有条目，检查是否为子目录
            for entry in entries:
                full_path = os.path.join(directory_path, entry)
                if os.path.isdir(full_path):
                    subdirectories.append(entry)
        except FileNotFoundError:
            logger.error(f"错误：指定的目录 '{directory_path}' 不存在。")
        except PermissionError:
            logger.error(f"错误：没有权限访问目录 '{directory_path}'。")
        except Exception as e:
            logger.error(f"发生未知错误：{e}")
        return subdirectories

    @staticmethod
    def get_valid_role_name():
        role_name = SystemService.get_sys_cache('system', 'roleName')
        if role_name is not None:
            return role_name
        role_list = SystemService.get_role_list()
        if len(role_list) > 0:
            return role_list[0]
        return None
