from typing import Callable, Any

from server.bean.system.role import Role
from server.bean.system.sys_cache_constants import SystemConstants
from server.service.system.system_service import SystemService
from server.common.log_config import logger
from server.dao.data_base_manager import db_config


class DatabaseSwitchUtil:
    """
    数据库临时切换工具类
    根据角色名称切换数据库，执行业务逻辑后恢复原角色
    """

    @staticmethod
    def execute_with_role_name_switch(target_role_name: str, business_func: Callable[[], Any]) -> Any:
        """
        根据角色名称切换到指定角色执行业务逻辑，执行完成后恢复原角色
        
        Args:
            target_role_name (str): 目标角色名称
            business_func (Callable[[], Any]): 业务逻辑函数
            
        Returns:
            Any: 业务逻辑函数的返回值
            
        Raises:
            ValueError: 当找不到指定角色名称时
            Exception: 业务逻辑执行过程中的异常
        """
        # 获取原始角色
        original_role = SystemService.get_valid_role()

        # 根据角色名称查找角色对象
        target_role = SystemService.get_role_by_name(target_role_name)
        if target_role is None:
            raise ValueError(f"找不到角色名称为 '{target_role_name}' 的角色")

        try:
            # 切换到目标角色
            DatabaseSwitchUtil._switch_to_role(target_role)
            logger.info(f"数据库角色已切换到: {target_role}")

            # 执行业务逻辑
            result = business_func()

            return result

        except Exception as e:
            logger.error(f"执行业务逻辑时发生错误: {e}")
            raise e

        finally:
            # 恢复原角色
            if original_role is not None:
                DatabaseSwitchUtil._switch_to_role(original_role)
                logger.info(f"数据库角色已恢复到: {original_role}")
            else:
                logger.warning("原始角色为空，无法恢复")

    @staticmethod
    def _switch_to_role(role: Role):
        """
        内部方法：切换到指定角色
        
        Args:
            role (Role): 要切换到的角色
        """
        if role is not None:
            db_config.update_db_path(role)
        else:
            logger.warning("尝试切换到空角色")
