class C_Role {
    constructor(data) {
        data = data || {};
        this.category = data.category ? data.category : ''; // 分类
        this.name = data.name || ''; // 角色名称
    }
}
class C_RoleCategory {
    constructor(data) {
        data = data || {};
        this.category = data.category ? data.category : ''; // 分类
        this.roleList = data.roleList ? data.roleList.map(item => new C_Role(item)) : []; // 角色列表
    }
}

class C_ObjTtsCorrectionTask {
    constructor(data) {
        data = data || {};
        this.id = data.id || 0; // 自增编号
        this.taskName = data.taskName || ''; // 任务名称
        this.textId = data.textId || 0; // 推理文本id
        this.productId = data.productId || 0; // 成品Id
        this.inferenceStatus = data.inferenceStatus || 0; // 推理状态 0 待推理 1 推理中 2 推理完成
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime; // 创建时间
    }
}

class C_ObjTtsCorrectionTaskDetail {
    constructor(data) {
        data = data || {};
        this.id = data.id || 0; // 自增编号
        this.taskId = data.taskId || 0; // 任务id
        this.textContent = data.textContent || ''; // 待推理的文本内容
        this.textIndex = data.textIndex || 0; // 文本序号
        this.status = data.status || 0; // 推理状态 0 待推理；1 推理中；2 已完成；3 失败
        this.audioPath = data.audioPath || ''; // 音频路径
        this.asrText = data.asrText || ''; // asr文本
        this.asrTextSimilarity = data.asrTextSimilarity || 0; // 文本相似度
        this.audioStatus = data.audioStatus || 0; // 音频状态 0 未校验；1 推理正确；2 推理不正确
        this.createTime = data.createTime; // 创建时间
    }
}

class C_ObjFinishedProductManager {
    constructor(data) {
        data = data || {};
        this.id = data.id || 0; // 自增编号
        this.name = data.name || ''; // 成品名称
        this.category = data.category || ''; // 分类
        this.gptSovitsVersion = data.gptSovitsVersion || ''; // 模型版本
        this.gptModelName = data.gptModelName || ''; // GPT模型名称
        this.gptModelPath = data.gptModelPath || ''; // GPT模型路径
        this.vitsModelName = data.vitsModelName || ''; // Vits模型名称
        this.vitsModelPath = data.vitsModelPath || ''; // Vits模型路径
        this.audioId = data.audioId || 0; // 音频id
        this.audioName = data.audioName || ''; // 音频名称
        this.audioPath = data.audioPath || ''; // 音频路径
        this.content = data.content || ''; // 音频内容
        this.language = data.language || ''; // 音频语种
        this.audioLength = data.audioLength || 0; // 音频时长
        this.topK = data.topK || 0.0; // top_k值
        this.topP = data.topP || 0.0; // top_p值
        this.temperature = data.temperature || 0.0; // 温度
        this.textDelimiter = data.textDelimiter || ''; // 文本分隔符
        this.speed = data.speed || 0.0; // 语速
        this.inpRefs = data.inpRefs || ''; // 融合音频，json字符串
        this.sound_fusion_list = data.sound_fusion_list ? data.sound_fusion_list.map(item => new C_ObjSoundFusionAudio(item)) : [];//融合音频
        this.score = data.score || 0; // 评分
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime; // 创建时间
    }
}
class C_ObjReferenceAudio {//参考音频
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // id
        this.audioName = data.audioName || ''; // 音频名称
        this.audioPath = data.audioPath || ''; // 音频路径
        this.content = data.content || ''; // 音频内容
        this.language = data.language || ''; // 音频语种
        this.category = data.category || ''; // 音频分类
        this.audioLength = data.audioLength || 0; // 音频时长
        this.score = data.score || 0; // 评分
        this.longTextScore = data.longTextScore || 0; // 长文评分
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime; // 创建时间, 默认为当前时间
    }
    
    getAudioExtension(){
        return getExtension(this.audioPath)
    }
}

class C_ObjInferenceTask {//推理任务
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.taskName = data.taskName || ''; // 任务名称
        this.compareType = data.compareType || ''; // 比较类型
        this.gptSovitsVersion = data.gptSovitsVersion || SysConfig.defaultGptSovitsVersion; // 模型版本
        this.gptModelName = data.gptModelName || ''; // GPT模型名称
        this.vitsModelName = data.vitsModelName || ''; // Vits模型名称
        this.topK = data.topK || SysConfig.defaultTopK; // top_k值
        this.topP = data.topP || SysConfig.defaultTopP; // top_p值
        this.temperature = data.temperature || SysConfig.defaultTemperature; // 温度
        this.textDelimiter = data.textDelimiter || SysConfig.defaultTextDelimiter; // 文本分隔符
        this.speed = data.speed || SysConfig.defaultSpeed; // 语速
        this.otherParameters = data.otherParameters || ''; // 其余参数
        this.inferenceStatus = data.inferenceStatus || 0; // 推理状态 0 待推理 1 推理中 2 推理完成
        this.executeTextSimilarity = data.executeTextSimilarity || 0;//是否已执行文本相似度 0 否 1 是
        this.executeAudioSimilarity = data.executeAudioSimilarity || 0;//是否已执行音频相似度 0 否 1 是
        this.conclusion = data.conclusion || ''; // 任务结论
        this.createTime = data.createTime; // 创建时间, 默认为当前时间
        this.taskTextList = data.textList ? data.textList.map(item => new C_ObjInferenceTaskText(item)) : [];
        this.taskAudioList = data.audioList ? data.audioList.map(item => new C_ObjInferenceTaskAudio(item)) : [];
        this.compareParams = data.paramList ? data.paramList.map(item => new C_ObjInferenceTaskCompareParams(item)) : [];
        this.taskInpRefsAudioList = data.inpRefsList ? data.inpRefsList.map(item => new C_ObjInferenceTaskSoundFusionAudio(item)) : [];
    }

    setParams(C_ObjInferenceTaskCompareParams$1){
        const param = C_ObjInferenceTaskCompareParams$1
        const compareType = this.compareType
        if (compareType === 'refer_audio') {
            return
        }
        if (['gpt_model','gv','all'].includes(compareType)) {
            this.gptSovitsVersion = param.gptSovitsVersion
            this.gptModelName = param.gptModelName
        }
        if (['vits_model','gv','all'].includes(compareType)) {
            this.gptSovitsVersion = param.gptSovitsVersion
            this.vitsModelName = param.vitsModelName
        }
        if (['top_k','kpt','all'].includes(compareType)) {
            this.topK = param.topK
        }
        if (['top_p','kpt','all'].includes(compareType)) {
            this.topP = param.topP
        }
        if (['temperature','kpt','all'].includes(compareType)) {
            this.temperature = param.temperature
        }
        if (['text_delimiter','all'].includes(compareType)) {
            this.textDelimiter = param.textDelimiter
        }
        if (['speed','all'].includes(compareType)) {
            this.speed = param.speed
        }
        if (['inp_refs','all'].includes(compareType)) {
            this.taskInpRefsAudioList = param.inpRefsAudioList
        }
    }
}
class C_ObjInferenceTaskText {//推理任务中，相关推理文本
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.taskId = data.taskId || 0; // 推理任务id
        this.textId = data.textId || 0; // 推理文本id
        this.category = data.category || ''; // 文本分类
        this.textContent = data.textContent || ''; // 推理文本
        this.textLanguage = data.textLanguage || ''; // 文本语种
        this.createTime = data.createTime; // 创建时间, 默认为当前时间
    }
}
class C_ObjInferenceTaskAudio {//推理任务中，相关参考音频
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.taskId = data.taskId || 0; // 推理任务id
        this.audioId = data.audioId || 0; // 音频id
        this.audioName = data.audioName || ''; // 音频名称
        this.audioPath = data.audioPath || ''; // 音频路径
        this.audioContent = data.audioContent || ''; // 音频内容
        this.audioLanguage = data.audioLanguage || ''; // 音频语种
        this.audioCategory = data.audioCategory || ''; // 音频分类
        this.audioLength = data.audioLength || 0; // 音频时长
        this.createTime = data.createTime ? new Date(data.createTime) : null; // 创建时间, 默认为当前时间
    }
    
    getObjReferenceAudio() {
        return new C_ObjReferenceAudio({
            id: this.audioId,
            audioName: this.audioName,
            audioPath: this.audioPath,
            content: this.audioContent,
            language: this.audioLanguage,
            category: this.audioCategory,
            audioLength: this.audioLength,
        })
    }
}
class C_ObjInferenceTaskCompareParams {//推理任务中，对比的变量
    constructor(data) {
        data = data || {};
        this.index = data.index ? data.index : 0; // 自增编号
        this.id = data.id ? data.id : 0; // 自增编号
        this.taskId = data.taskId || 0; // 任务id
        this.audioCategory = data.audioCategory || ''; // 音频分类
        this.gptSovitsVersion = data.gptSovitsVersion || 'v2'; // 模型版本
        this.gptModelName = data.gptModelName || ''; // GPT模型名称
        this.vitsModelName = data.vitsModelName || ''; // Vits模型名称
        this.topK = data.topK || 15; // top_k值
        this.topP = data.topP || 1.0; // top_p值
        this.temperature = data.temperature || 1.0; // 温度
        this.textDelimiter = data.textDelimiter || ''; // 文本分隔符
        this.speed = data.speed || 1.0; // 语速
        this.otherParameters = data.otherParameters || ''; // 其余参数
        this.createTime = data.createTime ? new Date(data.createTime) : null; // 创建时间, 默认为当前时间
        this.inpRefsAudioList = data.inpRefsList ? data.inpRefsList.map(item => new C_ObjInferenceTaskSoundFusionAudio(item)) : [];
    }
    
    getShowTxt(compareType){
        if (compareType == 'refer_audio') {
            return `音频分类：${this.audioCategory}`
        }
        if (compareType == 'gpt_model') {
            return `gpt模型：${this.gptSovitsVersion} ${this.gptModelName}`
        }
        if (compareType == 'vits_model') {
            return `vits模型：${this.gptSovitsVersion} ${this.vitsModelName}`
        }
        if (compareType == 'top_k') {
            return `top_k：${this.topK}`
        }
        if (compareType == 'top_p') {
            return `top_p：${this.topP}`
        }
        if (compareType == 'temperature') {
            return `temperature：${this.temperature}`
        }
        if (compareType == 'text_delimiter') {
            return `文本分隔符：${this.textDelimiter}`
        }
        if (compareType == 'speed') {
            return `语速：${this.speed}`
        }
        if (compareType == 'inp_refs') {
            return `融合音频：第${this.index}组`
        }
        if (compareType == 'kpt') {
            return `top_k:${this.topK};top_p:${this.topP};temperature:${this.temperature}`
        }
        if (compareType == 'gv') {
            return `版本:${this.gptSovitsVersion};gpt模型:${this.gptModelName};vits模型:${this.vitsModelName}`
        }
        if (compareType == 'all') {
            return `版本:${this.gptSovitsVersion};gpt模型:${this.gptModelName};vits模型:${this.vitsModelName};
            top_k:${this.topK};top_p:${this.topP};temperature:${this.temperature};
            文本分隔符:${this.textDelimiter};语速:${this.speed}
            `
        }
        return '--'
    }
}
class C_ObjInferenceText {//推理文本
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.category = data.category || ''; // 文本分类
        this.textContent = data.textContent || ''; // 推理文本
        this.textLanguage = data.textLanguage || ''; // 文本语种
        this.createTime = data.createTime; // 创建时间, 默认为当前时间
    }
}
class C_ObjInferenceTaskResultAudio {//推理任务的推理结果音频
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.taskId = data.taskId || 0; // 推理任务id
        this.textId = data.textId || 0; // 推理文本id
        this.audioId = data.audioId || 0; // 参考音频id
        this.compareParamId = data.compareParamId || 0; // 比对参数id
        this.path = data.path || ''; // 音频地址
        this.audioLength = data.audioLength || 0; // 时长
        this.status = data.status || 0; // 生成状态 1 成功；2 失败
        this.asrText = data.asrText || ''; // asr文本
        this.asrSimilarScore = data.asrSimilarScore || 0; // 文本相似度
        this.audioSimilarScore = data.audioSimilarScore || 0; // 音频相似度
        this.score = data.score || 0; // 评分
        this.longTextScore = data.longTextScore || 0; // 长文评分
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime ? new Date(data.createTime) : null; // 创建时间, 默认为当前时间
        
        this.objTask = data.objTask ? new C_ObjInferenceTask(data.objTask) : null;
        this.objText = data.objText ? new C_ObjInferenceText(data.objText) : null;
        this.objAudio = data.objAudio ? new C_ObjInferenceTaskAudio(data.objAudio) : null;
        this.objParam = data.objParam ? new C_ObjInferenceTaskCompareParams(data.objParam) : null;
    }
}

class C_ObjInferenceTaskResultAudioFilter {
    constructor(data) {
        data = data || {};
        this.taskId = data.taskId || 0;// 推理任务id
        this.compareParamIds = data.compareParamIds || [];// 对比参数id
        this.audioIds = data.audioIds || [];// 任务中，参考音频id
        this.textIds = data.textIds || [];// 任务中，推理文本id
        this.audioLengthStart = data.audioLengthStart || '';// 音频时长开始
        this.audioLengthEnd = data.audioLengthEnd || '';// 音频时长结束
        this.asrSimilarScoreStart = data.asrSimilarScoreStart || '';// 文本相似度开始
        this.asrSimilarScoreEnd = data.asrSimilarScoreEnd || '';// 文本相似度结束
        this.audioSimilarScoreStart = data.audioSimilarScoreStart || '';// 音频相似度开始
        this.audioSimilarScoreEnd = data.audioSimilarScoreEnd || '';// 音频相似度结束
        this.scoreStart = data.scoreStart || '';// 评分开始
        this.scoreEnd = data.scoreEnd || '';// 评分结束
        this.longTextScoreStart = data.longTextScoreStart || '';// 长文评分开始
        this.longTextScoreEnd = data.longTextScoreEnd || '';// 长文评分结束
        this.remark = data.remark || '';// 备注
        this.includeSort = data.includeSort || 0;// 包含排序
        this.audioSort = data.audioSort || 'audioLength';// 音频排序
        this.audioUpDown = data.audioUpDown || 'desc';// 音频排序方式
        this.visualization = data.visualization || 'close';// 音频可视化 close、 waveform, spectrogram, all
    }
}

class C_ObjInferenceCategory {//参考分类
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0; // 自增编号
        this.name = data.name || ''; // 分类名称
        this.createTime = data.createTime ? new Date(data.createTime) : null; // 创建时间, 默认为当前时间
    }
}

class C_ObjReferenceAudioCompareTask {
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0;// 自增编号
        this.audioId = data.audioId || 0;// 音频id
        this.categoryName = data.categoryName || '';// 比对目录名称
        this.status = data.status || 0;// 任务状态：0 待执行 1 执行中 2 已完成 3 失败
        this.remark = data.remark || '';// 备注
        this.createTime = data.createTime ? new Date(data.createTime) : null;// 创建时间,
    }
}

class C_ObjReferenceAudioCompareDetail {
    constructor(data) {
        data = data || {};
        this.id = data.id ? data.id : 0;// 自增编号
        this.taskId = data.taskId || 0;// 比对任务id
        this.compareAudioId = data.compareAudioId || 0;// 被比较的音频id
        this.score = data.score || 0;// 相似度分值
        this.createTime = data.createTime ? new Date(data.createTime) : null;// 创建时间,
        this.compareAudio = data.compareAudio ? new C_ObjReferenceAudio(data.compareAudio) : null;
    }
}

class C_GptModel {
    constructor(data) {
        data = data || {};
        this.version = data.version || '';//模型版本
        this.name = data.name || '';//模型名称
        this.path = data.path || '';//模型路径
    }
}

class C_VitsModel {
    constructor(data) {
        data = data || {};
        this.version = data.version || '';//模型版本
        this.name = data.name || '';//模型名称
        this.path = data.path || '';//模型路径
    }
}

class C_ResultEvaluationFilter {
    constructor() {
        this.taskId = 0;//推理任务id
        this.textIds = [];//推理文本id
        this.audioIds = [];//参考音频id
        this.compareParamIds = [];//比对参数id
    }
}

class C_ObjSoundFusionAudio {
    constructor(data) {
        data = data || {};
        this.id = data.id || 0; // 自增编号
        this.roleName = data.roleName || ''; // 角色名称
        this.audioName = data.audioName || ''; // 音频名称
        this.audioPath = data.audioPath || ''; // 音频路径
        this.content = data.content || ''; // 音频内容
        this.language = data.language || ''; // 音频语种
        this.category = data.category || ''; // 音频分类
        this.audioLength = data.audioLength || 0; // 音频时长
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime; // 创建时间
    }
    
}

class C_ObjInferenceTaskSoundFusionAudio {
    constructor(data) {
        data = data || {};
        this.id = data.id || 0; // 自增编号
        this.taskId = data.taskId || 0; // 任务ID
        this.compareParamId = data.compareParamId || 0; // 对比参数ID
        this.audioId = data.audioId || 0; // 融合音频ID
        this.roleName = data.roleName || ''; // 角色名称
        this.audioName = data.audioName || ''; // 音频名称
        this.audioPath = data.audioPath || ''; // 音频路径
        this.content = data.content || ''; // 音频内容
        this.language = data.language || ''; // 音频语种
        this.category = data.category || ''; // 音频分类
        this.audioLength = data.audioLength || 0; // 音频时长
        this.remark = data.remark || ''; // 备注
        this.createTime = data.createTime; // 创建时间
    }
    
}