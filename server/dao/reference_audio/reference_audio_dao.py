from typing import Dict

from server.bean.reference_audio.obj_reference_audio import ObjReferenceAudio, ObjReferenceAudioFilter
from server.dao.data_base_manager import DatabaseConnection, DBSlaveSQLExecutor


class ReferenceAudioDao:
    @staticmethod
    def find_count(filter: ObjReferenceAudioFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_reference_audio where 1=1
            '''

        condition_sql, condition = filter.make_sql()

        select_sql += condition_sql

        count = DBSlaveSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(audio_filter: ObjReferenceAudioFilter) -> list[ObjReferenceAudio]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_reference_audio where 1=1
            '''

        condition_sql, condition = audio_filter.make_sql()

        select_sql += condition_sql

        select_sql += audio_filter.get_order_by_sql()

        select_sql += audio_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)

        list = []

        for data in records:
            list.append(ObjReferenceAudio(id=data.get('Id'),
                                          audio_name=data.get('AudioName'),
                                          audio_path=data.get('AudioPath'),
                                          content=data.get('Content'),
                                          language=data.get('Language'),
                                          category=data.get('Category'),
                                          audio_length=data.get('AudioLength'),
                                          valid_or_not=data.get('ValidOrNot'),
                                          create_time=data.get('CreateTime')))
        return list

    @staticmethod
    def batch_insert_reference_audio(audio_list: list[ObjReferenceAudio]) -> int:
        sql = '''
        INSERT INTO tab_obj_reference_audio(AudioName,AudioPath,Content,Language,Category,AudioLength,ValidOrNot,CreateTime) VALUES (?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.audio_name,
            x.audio_path,
            x.content,
            x.language,
            x.category,
            x.audio_length,
            x.valid_or_not
        ) for x in audio_list])

    @staticmethod
    def update_audio_category(change_audio_id_str: str, target_category: str) -> int:
        sql = f'''
        UPDATE tab_obj_reference_audio SET Category = ? WHERE Id IN ({change_audio_id_str})
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (target_category,))
