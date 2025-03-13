import sqlite3


def init_slave_table(db_path):
    # 连接到SQLite数据库，如果不存在则创建
    conn = sqlite3.connect(db_path)

    # 创建一个游标对象用于执行SQL命令
    cursor = conn.cursor()

    # 文本转音频任务
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_tts_correction_task (
           Id                   INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增编号
           TaskName             TEXT, -- 任务名称
           TextId               INTEGER, -- 推理文本id
           ProductId            INTEGER, -- 成品Id
           InferenceStatus      INTEGER, -- 推理状态 0 待推理 1 推理中 2 推理完成
           Remark               TEXT, -- 备注
           CreateTime           DATETIME DEFAULT CURRENT_TIMESTAMP -- 创建时间
        );
    ''')

    # 文本转音频任务明细
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_tts_correction_task_detail (
           Id                   INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增编号
           TaskId               INTEGER, -- 任务id
           TextContent          TEXT, -- 待推理的文本内容
           TextIndex            INTEGER, -- 文本序号
           Status               INTEGER, -- 推理状态 0 待推理；1 推理中；2 已完成；3 失败
           AudioPath            TEXT, -- 音频路径
           AudioLength          REAL,  -- 音频时长
           AsrText              TEXT, -- asr文本
           AsrTextSimilarity    REAL, -- 文本相似度
           AudioStatus          INTEGER, -- 音频状态 0 未校验；1 推理正确；2 推理不正确
           CreateTime           DATETIME DEFAULT CURRENT_TIMESTAMP -- 创建时间
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_finished_product_manager (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增编号
            Name TEXT,  -- 成品名称
            Category TEXT,  -- 分类
            GptSovitsVersion TEXT,  -- 模型版本
            GptModelName TEXT,  -- GPT模型名称
            GptModelPath TEXT,  -- GPT模型路径
            VitsModelName TEXT,  -- Vits模型名称
            VitsModelPath TEXT,  -- Vits模型路径
            AudioId INTEGER,  -- 音频id
            AudioName TEXT,  -- 音频名称
            AudioPath TEXT,  -- 音频路径
            Content TEXT,  -- 音频内容
            Language TEXT,  -- 音频语种
            AudioLength REAL,  -- 音频时长
            TopK REAL,  -- top_k值
            TopP REAL,  -- top_p值
            Temperature REAL,  -- 温度
            TextDelimiter TEXT,  -- 文本分隔符
            Speed REAL,  -- 语速
            SampleSteps INTEGER,  -- 采样步数
            IfSr INTEGER,  -- 是否超分
            InpRefs TEXT,  -- 融合音频，json字符串
            Score INTEGER,  -- 评分
            Remark TEXT,  -- 备注
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_sound_fusion_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增编号
            TaskId INTEGER DEFAULT 0 ,-- 任务id
            CompareParamId INTEGER DEFAULT 0 ,-- 对比参数id
            AudioId INTEGER DEFAULT 0 ,-- 融合音频id
            RoleName TEXT DEFAULT '' ,-- 角色名称
            AudioName TEXT DEFAULT '' ,-- 音频名称
            AudioPath TEXT DEFAULT '' ,-- 音频路径
            Content TEXT DEFAULT '' ,-- 音频内容
            Language TEXT DEFAULT '',-- 音频语种
            Category TEXT DEFAULT '',-- 音频分类
            AudioLength REAL DEFAULT 0 ,-- 音频时长
            Remark TEXT DEFAULT '' ,-- 备注
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- 创建时间
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_reference_audio_compare_detail (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- SQLite使用INTEGER PRIMARY KEY AUTOINCREMENT
            TaskId INTEGER, -- MySQL的int(11)在SQLite中可以简单地用INTEGER表示
            CompareAudioId INTEGER, -- 同样适用于CompareAudioId
            Score REAL, -- MySQL的float在SQLite中可以用REAL表示
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- SQLite支持CURRENT_TIMESTAMP
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_reference_audio_compare_task (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- SQLite使用INTEGER PRIMARY KEY AUTOINCREMENT
            AudioId INTEGER, -- MySQL的int(11)在SQLite中可以简单地用INTEGER表示
            CategoryNames TEXT, -- MySQL的varchar在SQLite中可以用TEXT表示
            Status INTEGER, -- 任务状态：0 待执行 1 执行中 2 已完成 3 失败
            Remark TEXT, -- 备注
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- SQLite支持CURRENT_TIMESTAMP
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_category (
            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, -- 自增编号
            Name TEXT, -- 分类名称
            CreateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP -- 创建时间
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_reference_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            AudioName TEXT,--'音频名称' -- SQLite不支持直接在列定义中添加注释
            AudioPath TEXT,--'音频路径'
            Content TEXT,-- '音频内容'
            Language TEXT,--'音频语种'
            Category TEXT,-- '音频分类'
            AudioLength REAL,-- '音频时长'
            ValidOrNot INTEGER,-- '是否有效 1 有效 0 无效'
            Md5Value TEXT,-- 'md5值'
            IsManualCalib INTEGER,-- '是否人工校准 1 是； 0 否'
            FileSize INTEGER,-- '文件大小'
            Score INTEGER,-- '评分'
            LongTextScore INTEGER,-- '长文评分'
            Remark TEXT,-- '备注'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskName TEXT,-- '任务名称' -- 任务名称
            CompareType TEXT,-- '比较类型' -- SQLite不支持直接在列定义中添加注释
            GptSovitsVersion TEXT,-- '模型版本'
            GptModelName TEXT,--'GPT模型名称'
            VitsModelName TEXT,-- 'Vits模型名称'
            TopK REAL,-- 'top_k值' -- MySQL中的float类型在SQLite中对应REAL类型
            TopP REAL,--'top_p值'
            Temperature REAL,-- '温度'
            TextDelimiter TEXT,-- '文本分隔符'
            Speed REAL,-- '语速'
            SampleSteps INTEGER,  -- 采样步数
            IfSr INTEGER,  -- 是否超分
            OtherParameters TEXT,-- '其余参数'
            InferenceStatus INTEGER,-- '推理状态 0 待推理 1 推理中 2 推理完成' DEFAULT 0
            ExecuteTextSimilarity INTEGER,-- '是否已执行文本相似度 0 否 1 是' DEFAULT 0
            ExecuteAudioSimilarity INTEGER,-- '是否已执行音频相似度 0 否 1 是' DEFAULT 0
            Conclusion TEXT,-- '结论'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_text (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER,-- '推理任务id' -- SQLite不支持直接在列定义中添加注释
            TextId INTEGER,-- '推理文本id'
            Category TEXT, -- 文本分类 -- '文本分类'
            TextContent TEXT, -- '推理文本' MySQL中的text类型在SQLite中对应TEXT类型
            TextLanguage TEXT,-- '文本语种'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER,-- '推理任务id' -- SQLite不支持直接在列定义中添加注释
            AudioId INTEGER,-- '音频id'
            AudioName TEXT,-- '音频名称' -- 使用TEXT类型，虽然也可以使用VARCHAR
            AudioPath TEXT,-- '音频路径'
            AudioContent TEXT,-- '音频内容'
            AudioLanguage TEXT,-- '音频语种'
            AudioCategory TEXT,-- '音频分类'
            AudioLength REAL,-- '音频时长'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_compare_params (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER,-- '任务id' -- SQLite不支持直接在列定义中添加注释
            AudioCategory TEXT,-- '音频分类'
            GptSovitsVersion TEXT,-- '模型版本'
            GptModelName TEXT,-- 'GPT模型名称'
            VitsModelName TEXT,-- 'Vits模型名称'
            TopK REAL, -- 'top_k值' MySQL中的float类型在SQLite中对应REAL类型
            TopP REAL,-- 'top_p值'
            Temperature REAL,-- '温度'
            TextDelimiter TEXT,-- '文本分隔符'
            Speed REAL,-- '语速'
            SampleSteps INTEGER,  -- 采样步数
            IfSr INTEGER,  -- 是否超分
            OtherParameters TEXT,-- '其余参数'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_result_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER,-- '推理任务id' -- SQLite不支持直接在列定义中添加注释
            TextId INTEGER,-- '推理文本id'
            AudioId INTEGER,-- '参考音频id'
            CompareParamId INTEGER,-- '比对参数id'
            Path TEXT,-- '音频地址'
            AudioLength REAL,-- '时长'
            Status INTEGER,-- '生成状态 1 成功；2 失败'
            AsrText TEXT,-- 'asr文本'
            AsrSimilarScore REAL,-- '文本相似度'
            AudioSimilarScore REAL,-- '音频相似度'
            Score SMALLINT,-- '评分'
            LongTextScore SMALLINT,-- '长文评分'
            Remark TEXT,-- '备注'
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 提交事务（如果没有这一步，则不会保存更改）
    conn.commit()

    # 关闭连接
    conn.close()
