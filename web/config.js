const SysConfig = (function () {
    
    const languageList = [
        {
            name: '中文',
            code: 'all_zh'
        },
        {
            name: '粤语',
            code: 'all_yue'
        },
        {
            name: '英文',
            code: 'en'
        },
        {
            name: '日文',
            code: 'all_ja'
        },
        {
            name: '韩文',
            code: 'all_ko'
        },
        {
            name: '中英混合',
            code: 'zh'
        },
        {
            name: '粤英混合',
            code: 'yue'
        },
        {
            name: '日英混合',
            code: 'ja'
        },
        {
            name: '韩英混合',
            code: 'ko'
        },
        {
            name: '多语种混合',
            code: 'auto'
        },
        {
            name: '多语种混合(粤语)',
            code: 'auto_yue'
        }
    ]
    
    const defaultGptSovitsVersion = 'v2'
    const defaultTopK = 1
    const defaultTopP = 0.1
    const defaultTemperature = 0.1
    const defaultTextDelimiter = `,.;?!、，。？！；：…"`
    const defaultSpeed = 1.0
    
    return {
        languageList: languageList,
        defaultGptSovitsVersion: defaultGptSovitsVersion,
        defaultTopK: defaultTopK,
        defaultTopP: defaultTopP,
        defaultTemperature: defaultTemperature,
        defaultTextDelimiter: defaultTextDelimiter,
        defaultSpeed: defaultSpeed,
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