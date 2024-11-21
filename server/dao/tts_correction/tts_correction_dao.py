from server.bean.tts_correction.obj_tts_correction_task import ObjTtsCorrectionTaskFilter, ObjTtsCorrectionTask
from server.bean.tts_correction.obj_tts_correction_task_detail import ObjTtsCorrectionTaskDetailFilter, \
    ObjTtsCorrectionTaskDetail
from server.dao.data_base_manager import DBSlaveSQLExecutor


class TtsCorrectionDao:
    @staticmethod
    def find_count(task_filter: ObjTtsCorrectionTaskFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_tts_correction_task where 1=1
            '''

        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        count = DBSlaveSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(task_filter: ObjTtsCorrectionTaskFilter) -> list[ObjTtsCorrectionTask]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_tts_correction_task where 1=1
            '''

        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        select_sql += task_filter.get_order_by_sql()

        select_sql += task_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)

        text_list = []

        for data in records:
            text_list.append(ObjTtsCorrectionTask(
                id=data.get('id'),
                task_name=data.get('task_name'),
                text_id=data.get('text_id'),
                product_id=data.get('product_id'),
                inference_status=data.get('inference_status'),
                remark=data.get('remark'),
                create_time=data.get('create_time')
            ))
        return text_list

    @staticmethod
    def find_detail_count(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_tts_correction_task_detail where 1=1
            '''

        condition_sql, condition = detail_filter.make_sql()

        select_sql += condition_sql

        count = DBSlaveSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_detail_list(detail_filter: ObjTtsCorrectionTaskDetailFilter) -> list[ObjTtsCorrectionTaskDetail]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_tts_correction_task_detail where 1=1
            '''

        condition_sql, condition = detail_filter.make_sql()

        select_sql += condition_sql

        select_sql += detail_filter.get_order_by_sql()

        select_sql += detail_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)

        text_list = []

        for data in records:
            text_list.append(ObjTtsCorrectionTaskDetail(
                id=data.get('id'),
                task_id=data.get('task_id'),
                text_content=data.get('text_content'),
                text_index=data.get('text_index'),
                status=data.get('status'),
                audio_path=data.get('audio_path'),
                asr_text=data.get('asr_text'),
                asr_text_similarity=data.get('asr_text_similarity'),
                audio_status=data.get('audio_status'),
                create_time=data.get('create_time')
            ))
        return text_list

    @staticmethod
    def add_tts_correction_task(task: ObjTtsCorrectionTask) -> int:
        sql = '''
            INSERT INTO tab_obj_tts_correction_task(TaskName,TextId,ProductId,InferenceStatus,Remark,CreateTime) VALUES (?,?,?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.insert(sql, (
            task.task_name,
            task.text_id,
            task.product_id,
            task.inference_status,
            task.remark
        ))


    @staticmethod
    def batch_add_tts_correction_task_detail(task_detail_list: list[ObjTtsCorrectionTaskDetail]) -> int:
        sql = '''
        INSERT INTO tab_obj_tts_correction_task_detail(TaskId,TextContent,TextIndex,Status,AudioPath,AudioLength,AsrText,AsrTextSimilarity,AudioStatus,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.text_content,
            x.text_index,
            x.status,
            x.audio_path,
            x.audio_length,
            x.asr_text,
            x.asr_text_similarity,
            x.audio_status
        ) for x in task_detail_list])

    @staticmethod
    def batch_update_tts_correction_detail_status_file_length(detail_list):
        sql = '''
            UPDATE tab_obj_tts_correction_task_detail SET 
            Status=?,
            AudioPath=?,
            AudioLength=?
             WHERE Id = ? 
            '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.status,
            x.audio_path,
            x.audio_length,
            x.id
        ) for x in detail_list])

    @staticmethod
    def change_task_status(id: int, status: int):
        sql = '''
            UPDATE tab_obj_tts_correction_task SET InferenceStatus = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            status,
            id
        ))