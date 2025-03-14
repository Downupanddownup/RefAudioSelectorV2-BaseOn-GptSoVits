from server.bean.finished_product.finished_product_manager import ObjFinishedProductManagerFilter, \
    ObjFinishedProductManager
from server.dao.data_base_manager import DBSlaveSQLExecutor


class FinishedProductDao:
    @staticmethod
    def find_count(filter: ObjFinishedProductManagerFilter) -> int:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT COUNT(1) FROM tab_obj_finished_product_manager where 1=1
            '''

        condition_sql, condition = filter.make_sql()

        select_sql += condition_sql

        count = DBSlaveSQLExecutor.get_count(select_sql, condition)

        return count

    @staticmethod
    def find_list(audio_filter: ObjFinishedProductManagerFilter) -> list[ObjFinishedProductManager]:
        # 查询所有记录的SQL语句
        select_sql = '''
            SELECT * FROM tab_obj_finished_product_manager where 1=1
            '''

        condition_sql, condition = audio_filter.make_sql()

        select_sql += condition_sql

        select_sql += audio_filter.get_order_by_sql()

        select_sql += audio_filter.get_limit_sql()

        records = DBSlaveSQLExecutor.execute_query(select_sql, condition)

        list = []

        for data in records:
            list.append(ObjFinishedProductManager(
                id=data.get('Id'),
                name=data.get('Name'),
                category=data.get('Category'),
                gpt_sovits_version=data.get('GptSovitsVersion'),
                gpt_model_name=data.get('GptModelName'),
                gpt_model_path=data.get('GptModelPath'),
                vits_model_name=data.get('VitsModelName'),
                vits_model_path=data.get('VitsModelPath'),
                audio_id=data.get('AudioId'),
                audio_name=data.get('AudioName'),
                audio_path=data.get('AudioPath'),
                content=data.get('Content'),
                language=data.get('Language'),
                audio_length=data.get('AudioLength'),
                top_k=data.get('TopK'),
                top_p=data.get('TopP'),
                temperature=data.get('Temperature'),
                text_delimiter=data.get('TextDelimiter'),
                speed=data.get('Speed'),
                sample_steps=data.get('sample_steps'),
                if_sr=data.get('if_sr'),
                inp_refs=data.get('InpRefs'),
                score=data.get('Score'),
                remark=data.get('Remark'),
                create_time=data.get('CreateTime')
            ))
        return list

    @staticmethod
    def add_finished_product(product: ObjFinishedProductManager) -> int:
        sql = '''
            INSERT INTO tab_obj_finished_product_manager(Name,Category,GptSovitsVersion,GptModelName,GptModelPath,VitsModelName,VitsModelPath,AudioId,AudioName,AudioPath,Content,Language,AudioLength,TopK,TopP,Temperature,TextDelimiter,Speed,SampleSteps,IfSr,InpRefs,Score,Remark,CreateTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
            '''
        return DBSlaveSQLExecutor.insert(sql, (
            product.name,
            product.category,
            product.gpt_sovits_version,
            product.gpt_model_name,
            product.gpt_model_path,
            product.vits_model_name,
            product.vits_model_path,
            product.audio_id,
            product.audio_name,
            product.audio_path,
            product.content,
            product.language,
            product.audio_length,
            product.top_k,
            product.top_p,
            product.temperature,
            product.text_delimiter,
            product.speed,
            product.sample_steps,
            product.if_sr,
            product.inp_refs,
            product.score,
            product.remark
        ))

    @staticmethod
    def update_finished_product(product: ObjFinishedProductManager) -> int:
        sql = '''
            UPDATE tab_obj_finished_product_manager SET Name=?,Category=?,GptSovitsVersion=?,GptModelName=?,GptModelPath=?,VitsModelName=?,VitsModelPath=?,AudioId=?,AudioName=?,AudioPath=?,Content=?,Language=?,AudioLength=?,TopK=?,TopP=?,Temperature=?,TextDelimiter=?,Speed=?,SampleSteps=?,IfSr=?,InpRefs=?,Score=?,Remark=? WHERE Id = ? 
            '''
        return DBSlaveSQLExecutor.execute_update(sql, (
            product.name,
            product.category,
            product.gpt_sovits_version,
            product.gpt_model_name,
            product.gpt_model_path,
            product.vits_model_name,
            product.vits_model_path,
            product.audio_id,
            product.audio_name,
            product.audio_path,
            product.content,
            product.language,
            product.audio_length,
            product.top_k,
            product.top_p,
            product.temperature,
            product.text_delimiter,
            product.speed,
            product.sample_steps,
            product.if_sr,
            product.inp_refs,
            product.score,
            product.remark,
            product.id
        ))
