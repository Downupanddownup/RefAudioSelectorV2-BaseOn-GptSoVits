const SysConfig = (function () {
    
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
    
    const defaultGptSovitsVersion = 'v2'
    const defaultTopK = 12
    const defaultTopP = 0.6
    const defaultTemperature = 0.6
    const defaultTextDelimiter = `,.;?!、，。？！；：…"`
    const defaultSpeed = 1.0
    
    const defaultDialogWidth = '95%'
    const defaultDialogHeight = '95%'
    
    return {
        languageList: languageList,
        defaultGptSovitsVersion: defaultGptSovitsVersion,
        defaultTopK: defaultTopK,
        defaultTopP: defaultTopP,
        defaultTemperature: defaultTemperature,
        defaultTextDelimiter: defaultTextDelimiter,
        defaultSpeed: defaultSpeed,
        defaultDialogWidth: defaultDialogWidth,
        defaultDialogHeight: defaultDialogHeight
    }
})()

const BaseUrl = `http://localhost:8000/`
const RasApiUrl = (() => {
    const url = window.location.href;
    const params = new URLSearchParams(url.split('?')[1]);
    const apiPort = params.get('apiPort'); // 假设apiPort总是存在

    console.log('API Port:', apiPort);

    return `http://localhost:${8001}/`;
})()