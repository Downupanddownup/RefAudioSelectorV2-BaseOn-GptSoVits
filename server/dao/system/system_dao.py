from server.bean.system.sys_cache import SysCache
from server.dao.data_base_manager import DBMasterSQLExecutor


class SystemDao:
    @staticmethod
    def get_sys_cache(cache_type, cache_key) -> SysCache:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_sys_cache where Type = ? AND KeyName = ? LIMIT 1
            '''

        records = DBMasterSQLExecutor.execute_query(select_sql, (cache_type, cache_key))

        task_list = []

        for data in records:
            task_list.append(SysCache(
                id=data['Id'],
                type=data['Type'],
                key_name=data['KeyName'],
                value=data['Value']
            ))
        if len(task_list) == 0:
            return None
        return task_list[0]

    @staticmethod
    def insert_sys_cache(cache):
        sql = '''
            INSERT INTO tab_sys_cache(Type,KeyName,Value,CreateTime) VALUES (?,?,?,datetime('now'))
            '''
        return DBMasterSQLExecutor.insert(sql, (
            cache.type,
            cache.key_name,
            cache.value
        ))

    @staticmethod
    def update_sys_cache(cache):
        sql = '''
            UPDATE tab_sys_cache SET Value = ? WHERE Type = ? AND KeyName = ?
            '''
        return DBMasterSQLExecutor.execute_update(sql, (
            cache.value,
            cache.type,
            cache.key_name
        ))
