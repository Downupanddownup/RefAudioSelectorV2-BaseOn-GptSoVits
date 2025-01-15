const RasApiSpace = (function ()  {
    
    class C_RasApi{
        constructor(){
            this.status = 'close'
            this.streamMode = 1// 是否启动流式推理：1 是， 0 否
            this.mediaType = 'aac'//音频格式
            console.log(2322)
            if ( localStorage.getItem('streamMode')) {
                console.log(2322,localStorage.getItem('streamMode'))
                this.streamMode = parseInt(localStorage.getItem('streamMode'))
            }
            if ( localStorage.getItem('mediaType')) {
                this.mediaType = localStorage.getItem('mediaType')
            }
            console.log(2322,this)
        }
        
        isOpen(){
            return this.status === 'open'
        }
        
        checkIsRunning(callback){
            const _this = this
            const timeout = 1000; // 1秒超时
            $.customAjax({
                url: RasApiUrl+'status',
                method: 'GET',
                timeout: timeout, // 设置超时时间为1秒
                success: function(response) {
                    _this.status = 'open'
                    if (callback) {
                        callback(true)
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    _this.status = 'close'
                    if (callback) {
                        callback(false)
                    }
                }
            });
        }

        startApi(callback){
            const _this = this
            $.customAjax({
                url: BaseUrl+'inference/start_ras_api',
                type: 'post',
                data:{
                    streamMode:_this.streamMode,
                    mediaType:_this.mediaType,
                },
                success: function(res){
                    if (res.code == 0) {
                        _this.status = 'open'
                        if (callback) {
                            callback(res)
                        } else {
                            layui.layer.msg(res.msg)
                        }
                    } else {
                        layui.layer.msg(res.msg)
                    }
                },
                error: function(res, msg){
                    layui.layer.msg(msg)
                }
            })
        }

        stopApi(callback){
            const _this = this
            $.customAjax({
                url: BaseUrl+'inference/stop_ras_api',
                type: 'post',
                success: function(res){
                    console.log('为什么')
                    if (res.code == 0) {
                        _this.status = 'close'
                        if (callback) {
                            callback(res)
                        } else {
                            layui.layer.msg(res.msg)
                        }
                    } else {
                        layui.layer.msg(res.msg)
                    }
                },
                error: function(res, msg){
                    layui.layer.msg(msg)
                }
            })
        }

        setModel(gptModelPath, vitsModelPath, callback) {
            const _this = this
            const data = {
                gpt_model_path:gptModelPath,
                sovits_model_path:vitsModelPath
            }
            $.customAjax({
                url: RasApiUrl+'set_model',
                type: 'post',
                data:JSON.stringify(data),
                success: function(res){
                    console.log(res)
                    if (res.code == 0) {
                        callback()
                    } else {
                        layui.layer.msg('模型设置失败：' + res)
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Error details:', jqXHR.responseText);
                    layui.layer.msg(textStatus)
                }
            })
        }

        setDefaultParams(params, callback) {
            const _this = this
            
            const data = {}
            if (params.refer_wav_path) {
                data.refer_wav_path = params.refer_wav_path
            }
            if (params.prompt_text) {
                data.prompt_text = params.prompt_text
            }
            if (params.prompt_language) {
                data.prompt_language = params.prompt_language
            }
            if (params.cut_punc) {
                data.cut_punc = params.cut_punc
            }
            if (params.top_k) {
                data.top_k = params.top_k
            }
            if (params.top_p) {
                data.top_p = params.top_p
            }
            if (params.temperature) {
                data.temperature = params.temperature
            }
            if (params.speed) {
                data.speed = params.speed
            }
            if (params.inp_refs) {//是个列表
                data.inp_refs = params.inp_refs
            }
            
            data.stream_mode = _this.streamMode
            data.media_type = _this.mediaType
            
            $.customAjax({
                url: RasApiUrl+'ras/set_default_params',
                type: 'post',
                data:JSON.stringify(data),
                success: function(res){
                    if (res == 'ok') {
                        callback()
                        layui.layer.msg('参数设置成功')
                    } else {
                        layui.layer.msg('参数设置失败：' + res)
                    }
                },
                error: function(res, msg){
                    layui.layer.msg(msg)
                }
            })
        }
        
    }

    const RasApi = new C_RasApi()
    
    function getInstance() {
        return RasApi
    }
    
    return {
        getInstance:getInstance, 
    }
    
})()