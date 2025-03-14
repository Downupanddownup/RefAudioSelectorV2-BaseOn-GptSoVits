from server.bean.inference_task.obj_inference_task import ObjInferenceTaskFilter, ObjInferenceTask
from server.bean.inference_task.obj_inference_task_audio import ObjInferenceTaskAudio, ObjInferenceTaskAudioFilter
from server.bean.inference_task.obj_inference_task_compare_params import ObjInferenceTaskCompareParams, \
    ObjInferenceTaskCompareParamsFilter
from server.bean.inference_task.obj_inference_task_text import ObjInferenceTaskText, ObjInferenceTaskTextFilter
from server.bean.sound_fusion.obj_inference_task_sound_fusion_audio import ObjInferenceTaskSoundFusionAudio
from server.dao.data_base_manager import DBSlaveSQLExecutor


class InferenceTaskDao:
    @staticmethod
    def find_count(task_filter: ObjInferenceTaskFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_inference_task where 1=1
            '''

        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        count = DBSlaveSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(task_filter: ObjInferenceTaskFilter) -> list[ObjInferenceTask]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_task where 1=1
            '''

        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        select_sql += task_filter.get_order_by_sql()

        select_sql += task_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)

        text_list = []

        for data in records:
            text_list.append(ObjInferenceTask(
                id=data.get('Id'),
                task_name=data.get('TaskName'),
                compare_type=data.get('CompareType'),
                gpt_sovits_version=data.get('GptSovitsVersion'),
                gpt_model_name=data.get('GptModelName'),
                vits_model_name=data.get('VitsModelName'),
                top_k=data.get('TopK'),
                top_p=data.get('TopP'),
                temperature=data.get('Temperature'),
                text_delimiter=data.get('TextDelimiter'),
                speed=data.get('Speed'),
                sample_steps=data.get('SampleSteps'),
                if_sr=data.get('IfSr'),
                other_parameters=data.get('OtherParameters'),
                inference_status=data.get('InferenceStatus'),
                execute_text_similarity=data.get('ExecuteTextSimilarity'),
                execute_audio_similarity=data.get('ExecuteAudioSimilarity'),
                conclusion=data.get('Conclusion'),
                create_time=data.get('CreateTime')
            ))
        return text_list

    @staticmethod
    def insert_inference_task(task: ObjInferenceTask) -> int:
        sql = '''
            INSERT INTO tab_obj_inference_task(TaskName,CompareType,GptSovitsVersion,GptModelName,VitsModelName,TopK,TopP,Temperature,TextDelimiter,Speed,SampleSteps,IfSr,OtherParameters,InferenceStatus,ExecuteTextSimilarity,ExecuteAudioSimilarity,Conclusion,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.insert(sql, (
            task.task_name,
            task.compare_type,
            task.gpt_sovits_version,
            task.gpt_model_name,
            task.vits_model_name,
            task.top_k,
            task.top_p,
            task.temperature,
            task.text_delimiter,
            task.speed,
            task.sample_steps,
            task.if_sr,
            task.other_parameters,
            task.inference_status,
            task.execute_text_similarity,
            task.execute_audio_similarity,
            task.conclusion,
        ))

    @staticmethod
    def batch_insert_task_param(param_list: list[ObjInferenceTaskCompareParams]) -> int:
        sql = '''
        INSERT INTO tab_obj_inference_task_compare_params(TaskId,AudioCategory,GptSovitsVersion,GptModelName,VitsModelName,TopK,TopP,Temperature,TextDelimiter,Speed,SampleSteps,IfSr,OtherParameters,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.audio_category,
            x.gpt_sovits_version,
            x.gpt_model_name,
            x.vits_model_name,
            x.top_k,
            x.top_p,
            x.temperature,
            x.text_delimiter,
            x.speed,
            x.sample_steps,
            x.if_sr,
            x.other_parameters
        ) for x in param_list])

    @staticmethod
    def insert_task_param(param: ObjInferenceTaskCompareParams) -> int:
        sql = '''
            INSERT INTO tab_obj_inference_task_compare_params(TaskId,AudioCategory,GptSovitsVersion,GptModelName,VitsModelName,TopK,TopP,Temperature,TextDelimiter,Speed,SampleSteps,IfSr,OtherParameters,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.insert(sql, (
            param.task_id,
            param.audio_category,
            param.gpt_sovits_version,
            param.gpt_model_name,
            param.vits_model_name,
            param.top_k,
            param.top_p,
            param.temperature,
            param.text_delimiter,
            param.speed,
            param.sample_steps,
            param.if_sr,
            param.other_parameters
        ))

    @staticmethod
    def batch_insert_task_sound_fusion_audio(inp_refs_list: list[ObjInferenceTaskSoundFusionAudio]):
        sql = '''
        INSERT INTO tab_obj_inference_task_sound_fusion_audio(TaskId,CompareParamId,AudioId,RoleName,AudioName,AudioPath,Content,Language,Category,AudioLength,Remark,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.compare_param_id,
            x.audio_id,
            x.role_name,
            x.audio_name,
            x.audio_path,
            x.content,
            x.language,
            x.category,
            x.audio_length,
            x.remark
        ) for x in inp_refs_list])

    @staticmethod
    def batch_insert_task_audio(audio_list: list[ObjInferenceTaskAudio]) -> int:
        sql = '''
        INSERT INTO tab_obj_inference_task_audio(TaskId,AudioId,AudioName,AudioPath,AudioContent,AudioLanguage,AudioCategory,AudioLength,CreateTime) VALUES (?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.audio_id,
            x.audio_name,
            x.audio_path,
            x.audio_content,
            x.audio_language,
            x.audio_category,
            x.audio_length,
        ) for x in audio_list])

    @staticmethod
    def batch_insert_task_text(text_list: list[ObjInferenceTaskText]) -> int:
        sql = '''
        INSERT INTO tab_obj_inference_task_text(TaskId,TextId,Category,TextContent,TextLanguage,CreateTime) VALUES (?,?,?,?,?,datetime('now'))
        '''
        return DBSlaveSQLExecutor.batch_execute(sql, [(
            x.task_id,
            x.text_id,
            x.category,
            x.text_content,
            x.text_language
        ) for x in text_list])

    @staticmethod
    def get_task_param_list(task_filter: ObjInferenceTaskCompareParamsFilter) -> list[ObjInferenceTaskCompareParams]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_task_compare_params where 1 = 1
            '''
        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        select_sql += task_filter.get_order_by_sql()

        select_sql += task_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)
        record_list = []
        for data in records:
            record_list.append(ObjInferenceTaskCompareParams(
                id=data.get('Id'),
                task_id=data.get('TaskId'),
                audio_category=data.get('AudioCategory'),
                gpt_sovits_version=data.get('GptSovitsVersion'),
                gpt_model_name=data.get('GptModelName'),
                vits_model_name=data.get('VitsModelName'),
                top_k=data.get('TopK'),
                top_p=data.get('TopP'),
                temperature=data.get('Temperature'),
                text_delimiter=data.get('TextDelimiter'),
                speed=data.get('Speed'),
                sample_steps=data.get('SampleSteps'),
                if_sr=data.get('IfSr'),
                other_parameters=data.get('OtherParameters'),
                create_time=data.get('CreateTime')
            ))
        return record_list

    @staticmethod
    def get_task_sound_fusion_list_by_task_id(task_id: int) -> list[ObjInferenceTaskSoundFusionAudio]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_task_sound_fusion_audio where TaskId = ?
            '''

        records = DBSlaveSQLExecutor.execute_query(select_sql, (task_id,))
        record_list = []
        for data in records:
            record_list.append(ObjInferenceTaskSoundFusionAudio(
                id=data.get('Id'),
                task_id=data.get('TaskId'),
                compare_param_id=data.get('CompareParamId'),
                audio_id=data.get('AudioId'),
                role_name=data.get('RoleName'),
                audio_name=data.get('AudioName'),
                audio_path=data.get('AudioPath'),
                content=data.get('Content'),
                language=data.get('Language'),
                category=data.get('Category'),
                audio_length=data.get('AudioLength'),
                remark=data.get('Remark'),
                create_time=data.get('CreateTime')
            ))
        return record_list

    @staticmethod
    def get_task_audio_list(task_filter: ObjInferenceTaskAudioFilter) -> list[ObjInferenceTaskAudio]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_task_audio ta where 1 = 1
            '''
        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        select_sql += task_filter.get_order_by_sql()

        select_sql += task_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)
        record_list = []
        for data in records:
            record_list.append(ObjInferenceTaskAudio(
                id=data.get('Id'),
                task_id=data.get('TaskId'),
                audio_id=data.get('AudioId'),
                audio_name=data.get('AudioName'),
                audio_path=data.get('AudioPath'),
                audio_content=data.get('AudioContent'),
                audio_language=data.get('AudioLanguage'),
                audio_category=data.get('AudioCategory'),
                audio_length=data.get('AudioLength'),
                create_time=data.get('CreateTime')
            ))
        return record_list

    @staticmethod
    def get_task_text_list(task_filter: ObjInferenceTaskTextFilter) -> list[ObjInferenceTaskText]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_inference_task_text where 1 = 1
            '''

        condition_sql, condition = task_filter.make_sql()

        select_sql += condition_sql

        select_sql += task_filter.get_order_by_sql()

        select_sql += task_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)
        record_list = []
        for data in records:
            record_list.append(ObjInferenceTaskText(
                id=data.get('Id'),
                task_id=data.get('TaskId'),
                text_id=data.get('TextId'),
                category=data.get('Category'),
                text_content=data.get('TextContent'),
                text_language=data.get('TextLanguage'),
                create_time=data.get('CreateTime')
            ))
        return record_list

    @staticmethod
    def update_inference_task(task: ObjInferenceTask) -> int:
        sql = '''
            UPDATE tab_obj_inference_task SET 
            TaskName=?,
            CompareType=?,
            GptSovitsVersion=?,
            GptModelName=?,
            VitsModelName=?,
            TopK=?,
            TopP=?,
            Temperature=?,
            TextDelimiter=?,
            Speed=?,
            SampleSteps=?,
            IfSr=?,
            OtherParameters=?
             WHERE Id = ? 
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task.task_name,
            task.compare_type,
            task.gpt_sovits_version,
            task.gpt_model_name,
            task.vits_model_name,
            task.top_k,
            task.top_p,
            task.temperature,
            task.text_delimiter,
            task.speed,
            task.sample_steps,
            task.if_sr,
            task.other_parameters,
            task.id
        ))

    @staticmethod
    def delete_task_param_by_task_id(task_id: int) -> int:
        sql = '''
            DELETE FROM tab_obj_inference_task_compare_params WHERE TaskId = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task_id,
        ))

    @staticmethod
    def delete_task_sound_fusion_by_task_id(task_id: int):
        sql = '''
            DELETE FROM tab_obj_inference_task_sound_fusion_audio WHERE TaskId = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task_id,
        ))

    @staticmethod
    def delete_task_audio_by_task_id(task_id: int) -> int:
        sql = '''
            DELETE FROM tab_obj_inference_task_audio WHERE TaskId = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task_id,
        ))

    @staticmethod
    def delete_task_text_by_task_id(task_id: int) -> int:
        sql = '''
            DELETE FROM tab_obj_inference_task_text WHERE TaskId = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task_id,
        ))

    @staticmethod
    def change_inference_task_inference_status(task_id, inference_status: int) -> int:
        sql = '''
            UPDATE tab_obj_inference_task SET InferenceStatus = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            inference_status,
            task_id
        ))

    @staticmethod
    def update_task_execute_audio_similarity(task_id: int, execute_audio_similarity: int):
        sql = '''
            UPDATE tab_obj_inference_task SET ExecuteAudioSimilarity = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            execute_audio_similarity,
            task_id
        ))

    @staticmethod
    def update_task_execute_text_similarity(task_id: int, execute_text_similarity: int):
        sql = '''
            UPDATE tab_obj_inference_task SET ExecuteTextSimilarity = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            execute_text_similarity,
            task_id
        ))

    @staticmethod
    def update_task_name(task_id: int, task_name: str):
        sql = '''
            UPDATE tab_obj_inference_task SET TaskName = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            task_name,
            task_id
        ))

    @staticmethod
    def update_task_conclusion(task_id: int, conclusion: str):
        sql = '''
            UPDATE tab_obj_inference_task SET Conclusion = ? WHERE Id = ?
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            conclusion,
            task_id
        ))