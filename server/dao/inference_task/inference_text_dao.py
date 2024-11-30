from server.bean.text.obj_inference_text import ObjInferenceTextFilter, ObjInferenceText
from server.dao.data_base_manager import DBMasterSQLExecutor


class InferenceTextDao:
    @staticmethod
    def find_count(text_filter: ObjInferenceTextFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_inference_text where 1=1
            '''

        condition_sql, condition = text_filter.make_sql()

        select_sql += condition_sql

        count = DBMasterSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(text_filter: ObjInferenceTextFilter) -> list[ObjInferenceText]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_text where 1=1
            '''

        condition_sql, condition = text_filter.make_sql()

        select_sql += condition_sql

        select_sql += text_filter.get_order_by_sql()

        select_sql += text_filter.get_limit_sql()

        records = DBMasterSQLExecutor.execute_query(select_sql, condition)

        text_list = []

        for data in records:
            text_list.append(ObjInferenceText(
                id=data.get('Id'),
                category=data.get('Category'),
                text_content=data.get('TextContent'),
                text_language=data.get('TextLanguage'),
                create_time=data.get('CreateTime')
            ))
        return text_list

    @staticmethod
    def insert_inference_text(text):
        sql = '''
            INSERT INTO tab_obj_inference_text(Category,TextContent,TextLanguage,CreateTime) VALUES (?,?,?,datetime('now'))
            '''
        return DBMasterSQLExecutor.insert(sql, (
            text.category,
            text.text_content,
            text.text_language
        ))

    @staticmethod
    def delete_inference_text_by_id(text_id):
        sql = '''
            DELETE FROM tab_obj_inference_text WHERE Id = ?
            '''
        return DBMasterSQLExecutor.execute_update(sql, (text_id,))

    @staticmethod
    def update_inference_text_by_id(text):
        sql = '''
            UPDATE tab_obj_inference_text SET
            Category = ?,
            TextContent = ?,
            TextLanguage = ?
            WHERE Id = ?
            '''
        return DBMasterSQLExecutor.execute_update(sql, (
            text.category,
            text.text_content,
            text.text_language,
            text.id
        ))
