const RasApiSpace = (function ()  {
    
    class C_RasApi{
        constructor(){
            this.status = 'close'
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

        startApi(streamMode,callback){
            const _this = this
            $.customAjax({
                url: BaseUrl+'inference/start_ras_api',
                type: 'post',
                data:{
                    streamMode:streamMode ? 1 : 0
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
        
    }

    const RasApi = new C_RasApi()
    
    function getInstance() {
        return RasApi
    }
    
    return {
        getInstance:getInstance, 
    }
    
})()