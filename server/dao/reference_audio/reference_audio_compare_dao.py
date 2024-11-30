from server.bean.reference_audio.obj_reference_audio_compare_detail import ObjReferenceAudioCompareDetail
from server.bean.reference_audio.obj_reference_audio_compare_task import ObjReferenceAudioCompareTask
from server.dao.data_base_manager import DBSlaveSQLExecutor


class ReferenceAudioCompareDao:
    @staticmethod
    def insert_task(task: ObjReferenceAudioCompareTask) -> int:
        sql = '''
            INSERT INTO tab_obj_reference_audio_compare_task(AudioId,CategoryNames,Status,Remark,CreateTime) VALUES (?,?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.insert(sql, (
            task.audio_id,
            task.category_names,
            task.status,
            task.remark
        ))

    @staticmethod
    def get_task_by_id(task_id: int) -> ObjReferenceAudioCompareTask:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_reference_audio_compare_task where id = ? LIMIT 1
            '''

        records = DBSlaveSQLExecutor.execute_query(select_sql, (task_id,))

        task_list = []

        for data in records:
            task_list.append(ObjReferenceAudioCompareTask(
                id=data.get('Id'),
                audio_id=data.get('AudioId'),
                category_names=data.get('CategoryNames'),
                status=data.get('Status'),
                remark=data.get('Remark'),
                create_time=data.get('CreateTime')
            ))
        if len(task_list) == 0:
            return None
        return task_list[0]

    @staticmethod
    def update_task_status(task_id: int, status: int) -> int:
        sql = '''
            UPDATE tab_obj_reference_audio_compare_task SET Status = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            status,
            task_id
        ))

    @staticmethod
    def batch_insert_task_detail(detail_list: list[ObjReferenceAudioCompareDetail]) -> int:
        sql = '''
            INSERT INTO tab_obj_reference_audio_compare_detail(TaskId,CompareAudioId,Score,CreateTime) VALUES (?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.compare_audio_id,
            x.score
        ) for x in detail_list])

    @staticmethod
    def get_last_finish_task_by_audio_id(audio_id: int) -> ObjReferenceAudioCompareTask:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_reference_audio_compare_task where AudioId = ? AND Status = 2 ORDER BY Id DESC LIMIT 1
            '''

        records = DBSlaveSQLExecutor.execute_query(select_sql, (audio_id,))

        task_list = []

        for data in records:
            task_list.append(ObjReferenceAudioCompareTask(
                id=data.get('Id'),
                audio_id=data.get('AudioId'),
                category_names=data.get('CategoryNames'),
                status=data.get('Status'),
                remark=data.get('Remark'),
                create_time=data.get('CreateTime')
            ))
        if len(task_list) == 0:
            return None
        return task_list[0]

    @staticmethod
    def get_compare_detail_list_by_task_id(task_id: int) -> list[ObjReferenceAudioCompareDetail]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_reference_audio_compare_detail where TaskId = ? ORDER BY Score DESC
            '''

        records = DBSlaveSQLExecutor.execute_query(select_sql, (task_id,))

        task_list = []

        for data in records:
            task_list.append(ObjReferenceAudioCompareDetail(
                id=data.get('Id'),
                task_id=data.get('TaskId'),
                compare_audio_id=data.get('CompareAudioId'),
                score=data.get('Score'),
                create_time=data.get('CreateTime')
            ))
        return task_list

