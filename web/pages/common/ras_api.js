const RasApiSpace = (function ()  {
    
    class C_RasApi{
        constructor(){
            this.status = 'close'
        }
        
        isOpen(){
            return this.status === 'open'
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
                    console.log('为什么')
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