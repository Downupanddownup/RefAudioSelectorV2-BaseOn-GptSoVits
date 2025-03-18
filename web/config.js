const SysConfig = (function () {
    
    const openTips = false //是否开启提示
    
    const languageList = [
        {
            name: '中文(all_zh)',
            code: 'all_zh'
        },
        {
            name: '粤语(all_yue)',
            code: 'all_yue'
        },
        {
            name: '英文(en)',
            code: 'en'
        },
        {
            name: '日文(all_ja)',
            code: 'all_ja'
        },
        {
            name: '韩文(all_ko)',
            code: 'all_ko'
        },
        {
            name: '中英混合(zh)',
            code: 'zh'
        },
        {
            name: '粤英混合(yue)',
            code: 'yue'
        },
        {
            name: '日英混合(ja)',
            code: 'ja'
        },
        {
            name: '韩英混合(ko)',
            code: 'ko'
        },
        {
            name: '多语种混合(auto)',
            code: 'auto'
        },
        {
            name: '多语种混合(粤语)(auto_yue)',
            code: 'auto_yue'
        }
    ]
    
    const kpt = `
         <div style="color: yellow">以下内容说明来自官方文档：</div>
         <a style="color: white" href="https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/xyyqrfwiu3e2bgyk" target="_blank">
         关于top_p,top_k和temperature
         这三个值都是用来控制采样的。在推理的时候要挑出一个最好的token，但机器并不知道哪个是最好的。于是先按照top_k挑出前几个token，top_p在top_k的基础上筛选token。最后temperature控制随机性输出。
         比如总共有100个token，top_k设置5，top_p设置0.6，temperature设置为0.5。那么就会从100个token中先挑出5个概率最大的token，这五个token的概率分别是（0.3，0.3，0.2，0.2，0.1），那么再挑出累加概率不超过0.6的token（0.3和0.3），
         再从这两个token中随机挑出一个token输出，其中前一个token被挑选到的几率更大。以此类推
        </a>
    `
    
    const temperature = `
    <div style="color: yellow">以下内容说明来自deepseek：</div>
    <div style="color: white">temperature 控制生成随机性：0-1 更确定，1 为默认，1+ 更随机。</div>
    ${kpt}
    `
    
    const topK = `
    <div style="color: yellow">以下内容说明来自deepseek：</div>
    <div style="color: white">topK 控制候选词数量：按概率排序，仅从最高 K 个词中采样，K 越小输出越集中，K 越大输出越多样。</div>
    ${kpt}
    `
    
    const topP = `
    <div style="color: yellow">以下内容说明来自deepseek：</div>
    <div style="color: white">topP（核采样）控制候选词范围：按概率排序，仅从累积概率超过 P 的最高概率词中采样（P 取值范围 0-1），P 越小输出越集中，P 越大输出越多样。</div>
    ${kpt}
    `
    
    const tippyDesc = {
        'gptSovitsVersion': 'GptSoVits模型版本',
        'gptModelName': 'Gpt模型名称',
        'vitsModelName': 'SoVits模型名称',
        'topK': topK,
        'topP': topP,
        'temperature': temperature,
        'textDelimiter': '文本分隔符，GptSoVits模型不适合一次性推理长文本，设置此参数可将推送文本在api服务端进行二次切分',
        'speed': '设置音频语速，1为默认',
        'sampleSteps': '采样步数，仅v3有效',
        'ifSr': '启动超分会将音频采样频率从24000超分为48000',
        'inpRefsList': '融合音频，在【参考音频】tab下，点击【融合音频】进入管理界面,可选项：通过选择多个音频（建议同性），平均融合他们的音色。如不选择此项，音色由参考音频控制。如是微调模型，建议参考音频全部在微调训练集音色内，底模不用管。',
     }
    
    const defaultGptSovitsVersion = 'v3'
    // const defaultTopK = 12
    const defaultTopK = 15
    // const defaultTopP = 0.6
    const defaultTopP = 1
    // const defaultTemperature = 0.6
    const defaultTemperature = 1
    const defaultTextDelimiter = `,.;?!、，。？！；：…"`
    const defaultSpeed = 1.0
    const defaultSampleSteps = 32 //采样步数
    const defaultIfSr = 0 //0 不超分 1 超分
    
    const defaultDialogWidth = '95%'
    const defaultDialogHeight = '95%'
    
    return {
        tippyDesc: tippyDesc,
        languageList: languageList,
        defaultGptSovitsVersion: defaultGptSovitsVersion,
        defaultTopK: defaultTopK,
        defaultTopP: defaultTopP,
        defaultTemperature: defaultTemperature,
        defaultTextDelimiter: defaultTextDelimiter,
        defaultSpeed: defaultSpeed,
        defaultSampleSteps: defaultSampleSteps,
        defaultIfSr: defaultIfSr,
        defaultDialogWidth: defaultDialogWidth,
        defaultDialogHeight: defaultDialogHeight,
        openTips: openTips
    }
})()

const BaseUrl = `http://localhost:${window.location.port}/`
// const BaseUrl = `http://localhost:9000/`
const RasApiUrl = (() => {
    const url = window.location.href;
    const params = new URLSearchParams(url.split('?')[1]);
    let apiPort = params.get('apiPort'); // 假设apiPort总是存在

    console.log('API Port:', apiPort);

    // apiPort = 8002
    return `http://localhost:${apiPort}/`;
})()