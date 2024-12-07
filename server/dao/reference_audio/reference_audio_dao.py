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
                                          md5_value=data.get('Md5Value'),
                                          is_manual_calib=data.get('IsManualCalib'),
                                          file_size=data.get('FileSize'),
                                          score=data.get('Score'),
                                          long_text_score=data.get('LongTextScore'),
                                          remark=data.get('Remark'),
                                          create_time=data.get('CreateTime')))
        return list

    @staticmethod
    def batch_insert_reference_audio(audio_list: list[ObjReferenceAudio]) -> int:
        sql = '''
        INSERT INTO tab_obj_reference_audio(AudioName,AudioPath,Content,Language,Category,AudioLength,ValidOrNot,Md5Value,IsManualCalib,FileSize,Score,LongTextScore,Remark,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.audio_name,
            x.audio_path,
            x.content,
            x.language,
            x.category,
            x.audio_length,
            x.valid_or_not,
            x.md5_value,
            x.is_manual_calib,
            x.file_size,
            x.score,
            x.long_text_score,
            x.remark
        ) for x in audio_list])


    @staticmethod
    def update_reference_audio_list(audio_list: list[ObjReferenceAudio]) -> int:
        sql = '''
        UPDATE tab_obj_reference_audio SET AudioName=?,AudioPath=?,Content=?,Language=?,Category=?,AudioLength=?,ValidOrNot=?,Md5Value=?,IsManualCalib=?,FileSize=?,Score=?,LongTextScore=?,Remark=? WHERE Id = ? 
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.audio_name,
            x.audio_path,
            x.content,
            x.language,
            x.category,
            x.audio_length,
            x.valid_or_not,
            x.md5_value,
            x.is_manual_calib,
            x.file_size,
            x.score,
            x.long_text_score,
            x.remark,
            x.id
        ) for x in audio_list])

    @staticmethod
    def update_audio_category(change_audio_id_str: str, target_category: str) -> int:
        sql = f'''
        UPDATE tab_obj_reference_audio SET Category = ? WHERE Id IN ({change_audio_id_str})
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (target_category,))

    @staticmethod
    def update_audio_content(audio_id: int, content: str):
        sql = f'''
        UPDATE tab_obj_reference_audio SET Content = ? WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (content, audio_id))

    @staticmethod
    def update_audio_remark(audio_id: int, remark: str):
        sql = f'''
        UPDATE tab_obj_reference_audio SET Remark = ? WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (remark, audio_id))

    @staticmethod
    def update_audio_is_manual_calib(audio_id: int, is_manual_calib: int):
        sql = f'''
        UPDATE tab_obj_reference_audio SET IsManualCalib = ? WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (is_manual_calib, audio_id))


    @staticmethod
    def delete_reference_audio(audio_id: int):
        sql = f'''
        DELETE FROM tab_obj_reference_audio WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (audio_id,))
    @staticmethod
    def update_reference_audio(audio: ObjReferenceAudio) -> int:
        sql = f'''
        UPDATE tab_obj_reference_audio SET AudioName=?,Content=?,Language=?,Category=?,Remark=?,IsManualCalib=? WHERE Id = ? 
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            audio.audio_name,
            audio.content,
            audio.language,
            audio.category,
            audio.remark,
            audio.is_manual_calib,
            audio.id
        ))


    @staticmethod
    def update_audio_score_by_id(reference_audio_id: int):
        sql = f'''
            UPDATE tab_obj_reference_audio
            SET Score = (
                SELECT COALESCE(MAX(d.Score), 0)
                FROM tab_obj_inference_task_audio c
                INNER JOIN tab_obj_inference_task_result_audio d ON c.Id = d.AudioId
                WHERE c.AudioId = ?
            )
            WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (reference_audio_id,reference_audio_id))

    @staticmethod
    def update_audio_long_text_score_by_id(reference_audio_id: int):
        sql = f'''
            UPDATE tab_obj_reference_audio
            SET LongTextScore = (
                SELECT COALESCE(MAX(d.LongTextScore), 0)
                FROM tab_obj_inference_task_audio c
                INNER JOIN tab_obj_inference_task_result_audio d ON c.Id = d.AudioId
                WHERE c.AudioId = ?
            )
            WHERE Id = ?
        '''
        return DBSlaveSQLExecutor.execute_update(sql, (reference_audio_id,reference_audio_id))