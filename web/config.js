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
    
    return {
        languageList: languageList
    }
})()

const BaseUrl = `http://localhost:${window.location.port}/`
const RasApiUrl = (() => {
    const url = window.location.href;
    const params = new URLSearchParams(url.split('?')[1]);
    const apiPort = params.get('apiPort'); // 假设apiPort总是存在

    console.log('API Port:', apiPort);

    return `http://localhost:${apiPort}/`;
})()