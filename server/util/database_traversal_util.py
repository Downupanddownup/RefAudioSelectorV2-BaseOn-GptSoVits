import os
from typing import Callable, List, Dict, Any, Optional

from server.bean.finished_product.finished_product_manager import ObjFinishedProductManagerFilter
from server.bean.system.role import Role
from server.dao.data_base_manager import db_config
from server.service.finished_product.finished_product_service import FinishedProductService
from server.service.system.system_service import SystemService
from server.common.log_config import logger


class DatabaseTraversalResult:
    """数据库遍历结果封装类"""

    def __init__(self, category: str, role_name: str, db_path: str,
                 status: str = 'success', result: Any = None, error: str = None):
        self.category = category
        self.role_name = role_name
        self.db_path = db_path
        self.status = status  # 'success', 'error', 'not_found', 'skipped'
        self.result = result
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'category': self.category,
            'role_name': self.role_name,
            'db_path': self.db_path,
            'status': self.status,
            'result': self.result,
            'error': self.error
        }

    def is_success(self) -> bool:
        """判断是否执行成功"""
        return self.status == 'success'

    def __str__(self):
        return f"DatabaseTraversalResult(category={self.category}, role_name={self.role_name}, status={self.status})"


class DatabaseTraversalUtil:
    """数据库遍历工具类
    
    提供遍历所有分库并执行业务逻辑的抽象接口
    """

    @staticmethod
    def traverse_all_databases(business_function: Callable[[Role], Any],
                               filter_function: Optional[Callable[[Role], bool]] = None,
                               continue_on_error: bool = True,
                               log_progress: bool = True) -> List[DatabaseTraversalResult]:
        """
        遍历所有分库并执行业务逻辑
        
        Args:
            business_function: 业务逻辑函数，接收数据库连接和角色对象作为参数
            filter_function: 可选的过滤函数，用于筛选需要处理的角色
            continue_on_error: 遇到错误时是否继续处理其他数据库
            log_progress: 是否记录处理进度日志
            
        Returns:
            List[DatabaseTraversalResult]: 处理结果列表
        """
        # 保存原始角色状态
        original_role = SystemService.get_valid_role()
        
        results = []
        
        try:
            role_categories = SystemService.get_role_list()

            total_roles = sum(len(category.role_list) for category in role_categories)
            processed_count = 0

            if log_progress:
                logger.info(f"开始遍历数据库，共 {total_roles} 个角色")

            for category in role_categories:
                for role in category.role_list:
                    processed_count += 1

                    if log_progress:
                        logger.info(f"处理进度 [{processed_count}/{total_roles}] - {category.category}/{role.name}")

                    # 应用过滤器
                    if filter_function and not filter_function(role):
                        if log_progress:
                            logger.info(f"跳过角色: {category.category}/{role.name} (被过滤器排除)")
                        results.append(DatabaseTraversalResult(
                            category=category.category,
                            role_name=role.name,
                            db_path='',
                            status='skipped',
                            result='filtered out'
                        ))
                        continue

                    try:
                        result = DatabaseTraversalUtil._process_single_database(role, business_function, log_progress)
                        results.append(result)

                        if not result.is_success() and not continue_on_error:
                            logger.error(f"处理失败，停止遍历: {result.error}")
                            break

                    except Exception as e:
                        error_msg = f"处理角色 {category.category}/{role.name} 时发生未预期错误: {str(e)}"
                        logger.error(error_msg)

                        results.append(DatabaseTraversalResult(
                            category=category.category,
                            role_name=role.name,
                            db_path='',
                            status='error',
                            error=error_msg
                        ))

                        if not continue_on_error:
                            break

            if log_progress:
                DatabaseTraversalUtil._log_summary(results)

        finally:
            # 恢复原始数据库状态
            db_config.update_db_path(original_role)
            if log_progress:
                logger.info(f"已恢复原始数据库状态: {original_role.category}/{original_role.name}")

        return results

    @staticmethod
    def _process_single_database(role: Role,
                                 business_function: Callable[[Role], Any],
                                 log_progress: bool) -> DatabaseTraversalResult:
        """
        处理单个数据库
        
        Args:
            role: 角色对象
            business_function: 业务逻辑函数
            log_progress: 是否记录日志
            
        Returns:
            DatabaseTraversalResult: 处理结果
        """
        # 切换到当前角色的数据库
        db_config.update_db_path(role)
        db_path = db_config.db_path

        # 检查数据库文件是否存在
        if not os.path.exists(db_path):
            if log_progress:
                logger.warning(f"数据库文件不存在: {db_path}")
            return DatabaseTraversalResult(
                category=role.category,
                role_name=role.name,
                db_path=db_path,
                status='not_found',
                error='数据库文件不存在'
            )

        try:
            # 执行业务逻辑
            result = business_function(role)

            if log_progress:
                logger.info(f"成功处理角色: {role.category}/{role.name}")

            return DatabaseTraversalResult(
                category=role.category,
                role_name=role.name,
                db_path=db_path,
                status='success',
                result=result
            )

        except Exception as e:
            error_msg = f"执行业务逻辑时出错: {str(e)}"
            if log_progress:
                logger.error(f"处理角色 {role.category}/{role.name} 失败: {error_msg}")

            return DatabaseTraversalResult(
                category=role.category,
                role_name=role.name,
                db_path=db_path,
                status='error',
                error=error_msg
            )

    @staticmethod
    def _log_summary(results: List[DatabaseTraversalResult]):
        """记录处理结果摘要"""
        success_count = len([r for r in results if r.status == 'success'])
        error_count = len([r for r in results if r.status == 'error'])
        not_found_count = len([r for r in results if r.status == 'not_found'])
        skipped_count = len([r for r in results if r.status == 'skipped'])

        logger.info("=== 数据库遍历结果摘要 ===")
        logger.info(f"总计: {len(results)} 个角色")
        logger.info(f"成功处理: {success_count}")
        logger.info(f"处理错误: {error_count}")
        logger.info(f"文件不存在: {not_found_count}")
        logger.info(f"被跳过: {skipped_count}")

    @staticmethod
    def traverse_by_category(category_name: str,
                             business_function: Callable[[Role], Any],
                             continue_on_error: bool = True,
                             log_progress: bool = True) -> List[DatabaseTraversalResult]:
        """
        遍历指定分类下的所有数据库
        
        Args:
            category_name: 分类名称
            business_function: 业务逻辑函数
            continue_on_error: 遇到错误时是否继续处理
            log_progress: 是否记录处理进度日志
            
        Returns:
            List[DatabaseTraversalResult]: 处理结果列表
        """

        def category_filter(role: Role) -> bool:
            return role.category == category_name

        return DatabaseTraversalUtil.traverse_all_databases(
            business_function=business_function,
            filter_function=category_filter,
            continue_on_error=continue_on_error,
            log_progress=log_progress
        )

    @staticmethod
    def traverse_by_role_names(role_names: List[str],
                               business_function: Callable[[Role], Any],
                               continue_on_error: bool = True,
                               log_progress: bool = True) -> List[DatabaseTraversalResult]:
        """
        遍历指定角色名称列表的数据库
        
        Args:
            role_names: 角色名称列表
            business_function: 业务逻辑函数
            continue_on_error: 遇到错误时是否继续处理
            log_progress: 是否记录处理进度日志
            
        Returns:
            List[DatabaseTraversalResult]: 处理结果列表
        """

        def role_name_filter(role: Role) -> bool:
            return role.name in role_names

        return DatabaseTraversalUtil.traverse_all_databases(
            business_function=business_function,
            filter_function=role_name_filter,
            continue_on_error=continue_on_error,
            log_progress=log_progress
        )

    @staticmethod
    def get_successful_results(results: List[DatabaseTraversalResult]) -> List[DatabaseTraversalResult]:
        """获取成功处理的结果"""
        return [r for r in results if r.is_success()]

    @staticmethod
    def get_failed_results(results: List[DatabaseTraversalResult]) -> List[DatabaseTraversalResult]:
        """获取处理失败的结果"""
        return [r for r in results if r.status == 'error']

    @staticmethod
    def export_results_to_dict(results: List[DatabaseTraversalResult]) -> List[Dict[str, Any]]:
        """将结果导出为字典列表"""
        return [result.to_dict() for result in results]


# 使用示例和常用业务函数
class CommonBusinessFunctions:
    """常用业务函数集合"""

    @staticmethod
    def count_tables(role: Role) -> int:
        """统计各表的记录数量"""

        audio_filter = ObjFinishedProductManagerFilter({})

        count = FinishedProductService.find_count(audio_filter)

        return count


if __name__ == '__main__':
    # 使用示例
    
    # 确保主数据库已初始化
    db_config.init_master_db_path()

    # 示例1: 使用lambda表达式统计所有数据库的表记录数量
    print("=== 示例1: 使用lambda表达式统计表记录数量 ===")
    results = DatabaseTraversalUtil.traverse_all_databases(
        business_function=lambda role: FinishedProductService.find_count(ObjFinishedProductManagerFilter({}))
    )

    for result in DatabaseTraversalUtil.get_successful_results(results):
        print(f"{result.category}/{result.role_name}: {result.result}")
    
    # 示例2: 使用lambda表达式进行条件过滤
    print("\n=== 示例2: 使用lambda表达式过滤特定分类 ===")
    results = DatabaseTraversalUtil.traverse_all_databases(
        business_function=lambda role: FinishedProductService.find_count(ObjFinishedProductManagerFilter({})),
        filter_function=lambda role: role.category == "崩坏三"  # 只处理崩坏三分类
    )
    
    for result in DatabaseTraversalUtil.get_successful_results(results):
        print(f"{result.category}/{result.role_name}: {result.result}")
    
    # 示例3: 使用传统函数方式（保留兼容性）
    print("\n=== 示例3: 传统函数方式 ===")
    results = DatabaseTraversalUtil.traverse_all_databases(
        business_function=CommonBusinessFunctions.count_tables
    )

    for result in DatabaseTraversalUtil.get_successful_results(results):
        print(f"{result.category}/{result.role_name}: {result.result}")
