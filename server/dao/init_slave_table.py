import sqlite3


def init_slave_table(db_path):
    # 连接到SQLite数据库，如果不存在则创建
    conn = sqlite3.connect(db_path)

    # 创建一个游标对象用于执行SQL命令
    cursor = conn.cursor()

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
            AudioLength INTEGER DEFAULT 0 ,-- 音频时长
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
            CategoryName TEXT, -- MySQL的varchar在SQLite中可以用TEXT表示
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
            AudioName TEXT COMMENT '音频名称', -- SQLite不支持直接在列定义中添加注释
            AudioPath TEXT COMMENT '音频路径',
            Content TEXT COMMENT '音频内容',
            Language TEXT COMMENT '音频语种',
            Category TEXT COMMENT '音频分类',
            AudioLength INTEGER COMMENT '音频时长',
            ValidOrNot INTEGER COMMENT '是否有效 1 有效 0 无效' DEFAULT 1,
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskName TEXT COMMENT '任务名称', -- 任务名称
            CompareType TEXT COMMENT '比较类型', -- SQLite不支持直接在列定义中添加注释
            GptSovitsVersion TEXT COMMENT '模型版本',
            GptModelName TEXT COMMENT 'GPT模型名称',
            VitsModelName TEXT COMMENT 'Vits模型名称',
            TopK REAL COMMENT 'top_k值', -- MySQL中的float类型在SQLite中对应REAL类型
            TopP REAL COMMENT 'top_p值',
            Temperature REAL COMMENT '温度',
            TextDelimiter TEXT COMMENT '文本分隔符',
            Speed REAL COMMENT '语速',
            OtherParameters TEXT COMMENT '其余参数',
            InferenceStatus INTEGER COMMENT '推理状态 0 待推理 1 推理中 2 推理完成' DEFAULT 0,
            ExecuteTextSimilarity INTEGER COMMENT '是否已执行文本相似度 0 否 1 是' DEFAULT 0,
            ExecuteAudioSimilarity INTEGER COMMENT '是否已执行音频相似度 0 否 1 是' DEFAULT 0,
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_text (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER COMMENT '推理任务id', -- SQLite不支持直接在列定义中添加注释
            TextId INTEGER COMMENT '推理文本id',
            Category TEXT COMMENT '文本分类', -- 文本分类
            TextContent TEXT COMMENT '推理文本', -- MySQL中的text类型在SQLite中对应TEXT类型
            TextLanguage TEXT COMMENT '文本语种',
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER COMMENT '推理任务id', -- SQLite不支持直接在列定义中添加注释
            AudioId INTEGER COMMENT '音频id',
            AudioName TEXT COMMENT '音频名称', -- 使用TEXT类型，虽然也可以使用VARCHAR
            AudioPath TEXT COMMENT '音频路径',
            AudioContent TEXT COMMENT '音频内容',
            AudioLanguage TEXT COMMENT '音频语种',
            AudioCategory TEXT COMMENT '音频分类',
            AudioLength REAL COMMENT '音频时长',
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_compare_params (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER COMMENT '任务id', -- SQLite不支持直接在列定义中添加注释
            AudioCategory TEXT COMMENT '音频分类',
            GptSovitsVersion TEXT COMMENT '模型版本',
            GptModelName TEXT COMMENT 'GPT模型名称',
            VitsModelName TEXT COMMENT 'Vits模型名称',
            TopK REAL COMMENT 'top_k值', -- MySQL中的float类型在SQLite中对应REAL类型
            TopP REAL COMMENT 'top_p值',
            Temperature REAL COMMENT '温度',
            TextDelimiter TEXT COMMENT '文本分隔符',
            Speed REAL COMMENT '语速',
            OtherParameters TEXT COMMENT '其余参数',
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_task_result_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用AUTOINCREMENT关键字实现自动增长
            TaskId INTEGER COMMENT '推理任务id', -- SQLite不支持直接在列定义中添加注释
            TextId INTEGER COMMENT '推理文本id',
            AudioId INTEGER COMMENT '参考音频id',
            CompareParamId INTEGER COMMENT '比对参数id',
            Path TEXT COMMENT '音频地址',
            AudioLength REAL COMMENT '时长',
            Status INTEGER COMMENT '生成状态 1 成功；2 失败',
            AsrText TEXT COMMENT 'asr文本',
            AsrSimilarScore REAL COMMENT '文本相似度',
            AudioSimilarScore REAL COMMENT '音频相似度',
            Score SMALLINT COMMENT '评分',
            LongTextScore SMALLINT COMMENT '长文评分',
            Remark TEXT COMMENT '备注',
            CreateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- SQLite中默认值可以直接设置
        );
    ''')

    # 提交事务（如果没有这一步，则不会保存更改）
    conn.commit()

    # 关闭连接
    conn.close()
