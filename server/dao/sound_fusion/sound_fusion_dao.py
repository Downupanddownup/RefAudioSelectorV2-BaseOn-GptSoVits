from server.bean.sound_fusion.obj_sound_fusion_audio import ObjSoundFusionAudioFilter, ObjSoundFusionAudio
from server.dao.data_base_manager import DBMasterSQLExecutor


class SoundFusionDao:
    @staticmethod
    def find_count(audio_filter: ObjSoundFusionAudioFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_sound_fusion_audio where 1=1
            '''

        condition_sql, condition = audio_filter.make_sql()

        select_sql += condition_sql

        count = DBMasterSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(audio_filter: ObjSoundFusionAudioFilter) -> list[ObjSoundFusionAudio]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_sound_fusion_audio where 1=1
            '''

        condition_sql, condition = audio_filter.make_sql()

        select_sql += condition_sql

        select_sql += audio_filter.get_order_by_sql()

        select_sql += audio_filter.get_limit_sql()

        records = DBMasterSQLExecutor.execute_query(select_sql, condition)

        list = []

        for data in records:
            list.append(ObjSoundFusionAudio(
                id=data['id'],
                role_name=data['roleName'],
                audio_name=data['audioName'],
                audio_path=data['audioPath'],
                content=data['content'],
                language=data['language'],
                category=data['category'],
                audio_length=data['audioLength'],
                remark=data['remark'],
                create_time=data['createTime']
            ))
        return list

    @staticmethod
    def batch_add_sound_fusion_audio(sound_fusion_audio_list: list[ObjSoundFusionAudio]):
        sql = '''
        INSERT INTO tab_obj_sound_fusion_audio(RoleName,AudioName,AudioPath,Content,Language,Category,AudioLength,Remark,CreateTime) VALUES (?,?,?,?,?,?,?,?,datetime('now'))
        '''
        return DBMasterSQLExecutor.batch_execute(sql, [(
            x.role_name,
            x.audio_name,
            x.audio_path,
            x.content,
            x.language,
            x.category,
            x.audio_length,
            x.remark
        ) for x in sound_fusion_audio_list])

    @staticmethod
    def update_sound_fusion_audio(audio: ObjSoundFusionAudio):
        sql = f'''
        UPDATE tab_obj_sound_fusion_audio SET RoleName=?,AudioName=?,Content=?,Language=?,Category=?,Remark=? WHERE Id = ? 
        '''
        return DBMasterSQLExecutor.execute_update(sql, (
            audio.role_name,
            audio.audio_name,
            audio.content,
            audio.language,
            audio.category,
            audio.remark,
            audio.id
        ))

    @staticmethod
    def delete_sound_fusion_audio_by_id(audio_id: int):
        sql = f'''
        DELETE FROM tab_obj_sound_fusion_audio WHERE Id = ?
        '''
        return DBMasterSQLExecutor.execute_update(sql, (audio_id,))
