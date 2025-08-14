import os

from server.bean.system.role import Role
from server.bean.system.role_category import RoleCategory
from server.bean.system.sys_cache import SysCache
from server.bean.system.sys_cache_constants import SystemConstants
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
    def get_role_list() -> list[RoleCategory]:
        directory_path = db_config.get_slave_dir()  # 假设db_config.get_slave_dir()返回的是正确的目录路径
        subdirectories = []
        try:
            # 使用os.listdir获取目录下的所有条目
            entries = os.listdir(directory_path)

            # 遍历所有条目，检查是否为子目录
            for entry in entries:
                full_path = os.path.join(directory_path, entry)
                if os.path.isdir(full_path):

                    role_list = []

                    # 获取该子目录下的所有条目
                    second_level_entries = os.listdir(full_path)
                    for second_entry in second_level_entries:
                        second_full_path = os.path.join(full_path, second_entry)
                        if os.path.isdir(second_full_path):
                            role_list.append(Role(category=entry, name=second_entry))  # 添加二级子目录

                    if len(role_list) > 0:
                        subdirectories.append(RoleCategory(category=entry, role_list=role_list))  # 添加一级子目录

        except FileNotFoundError:
            logger.error(f"错误：指定的目录 '{directory_path}' 不存在。")
        except PermissionError:
            logger.error(f"错误：没有权限访问目录 '{directory_path}'。")
        except Exception as e:
            logger.error(f"发生未知错误：{e}")
        return subdirectories

    @staticmethod
    def get_valid_role() -> Role:
        role = SystemService.get_sys_cache(SystemConstants.CACHE_TYPE, SystemConstants.CACHE_KEY_ROLE)
        if role is not None:
            return Role.from_json_string(role)
        role_list = SystemService.get_role_list()
        if len(role_list) > 0:
            return role_list[0].role_list[0]
        return None

    @staticmethod
    def get_role_by_name(role_name: str) -> Role:
        """
        根据角色名称查找角色对象
        
        Args:
            role_name (str): 角色名称
            
        Returns:
            Role: 找到的角色对象，如果未找到则返回None
        """
        role_list = SystemService.get_role_list()
        for role_category in role_list:
            for role in role_category.role_list:
                if role.name == role_name:
                    return role
        return None
