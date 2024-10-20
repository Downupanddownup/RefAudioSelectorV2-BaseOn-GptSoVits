const CommonSpace = (function () {

        function customJquery($) {
            // 初始化 _requestStates
            const _requestStates = {};

            // 新增一个名为 customAjax 的方法
            $.customAjax = function (settings) {
                // 获取请求的唯一标识符
                const requestKey = settings.url + settings.type + JSON.stringify(settings.data);

                // 检查是否有请求正在进行
                if (_requestStates[requestKey]) {
                    console.log('请求已在进行中，不再重复发送。');
                    return;
                }

                // 加载层
                const loadIndex = layui.layer.load(0);

                // 设置请求状态为进行中
                _requestStates[requestKey] = true;
                
                const complete = settings.complete;

                settings.complete = function (jqXHR, statusText) {

                    delete _requestStates[requestKey];
                    layui.layer.close(loadIndex)
                    
                    if (complete) {
                        complete(jqXHR, statusText)
                    }

                }

                // 调用原始的 $.ajax 方法
                return $.ajax(settings);
            }
        }


        function loadHtml(url, callback) {
            // 使用 $.ajax 加载 HTML 文件
            $.ajax({
                url: url, // 替换为你的HTML文件路径
                type: 'GET',
                dataType: 'html',
                success: function (data) {
                    // 成功加载后，将内容追加到文档末尾
                    $(document.body).append(data);
                    callback()
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error('加载HTML文件失败：', textStatus, errorThrown);
                }
            });
        }

        function loadHtmls(urls, callback) {
            const unLoads = new Set(urls)
            const allUrls = new Set(urls)
            allUrls.forEach(url => {
                loadHtml(url, function () {
                    unLoads.delete(url)
                    if (unLoads.size === 0) {
                        callback()
                    }
                })
            })
        }

        return {
            customJquery: customJquery,
            loadHtmls: loadHtmls
        }

    }

)
()
