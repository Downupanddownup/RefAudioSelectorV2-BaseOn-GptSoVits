class AudioController {
    constructor(audioElements) {
        this.currentPlayingAudio = null;
        if (audioElements) {
            this.registerEventListeners(audioElements);
        }
    }

    registerEventListeners(audioElements) {
        const _this = this;
        audioElements.forEach(audioElement => {
           _this.registerEventListener(audioElement)
        });
    }
    registerEventListener(audioElement) {
        // 添加播放事件监听器
        audioElement.addEventListener('play', () => {
            if (this.currentPlayingAudio && this.currentPlayingAudio !== audioElement) {
                this.currentPlayingAudio.pause(); // 如果有其他音频在播放，则先暂停
            }
            this.currentPlayingAudio = audioElement; // 更新当前播放的音频引用
        });

        // 添加暂停事件监听器
        audioElement.addEventListener('pause', () => {
            if (this.currentPlayingAudio === audioElement) {
                this.currentPlayingAudio = null;
            }
        });

        // 添加播放结束事件监听器
        audioElement.addEventListener('ended', () => {
            if (this.currentPlayingAudio === audioElement) {
                this.currentPlayingAudio = null;
            }
        });
    }

    dispatchClickEvent(audioElement) {
        console.log('播放/暂停按钮被点击');
        if (audioElement.paused || audioElement.currentTime === 0) {
            // 如果音频当前是暂停状态或尚未开始播放，则播放音频
            audioElement.play();
            console.log('正在播放音频');
        } else {
            // 如果音频正在播放，则暂停音频
            audioElement.pause();
            console.log('音频已暂停');
        }
    }
    
}


function isTrue(condition, ifTrue, ifFalse) {
    return condition ? ifTrue : ifFalse;
}

function refreshListData(listId){
    // 数据重载 - 仅与数据相关的属性(options)能参与到重载中
    layui.table.reloadData(listId, {
        // where: {}, // 数据异步请求时携带的字段集 --- 属性设置有效，因属于数据相关属性
        scrollPos: true, // 设定重载数据或切换分页时的滚动条的位置状态 --- 属性设置有效
    });
}

function reloadListDataBySearchParams(listId,params){
    // 数据重载 - 仅与数据相关的属性(options)能参与到重载中
    layui.table.reloadData(listId, {
        where: params, // 数据异步请求时携带的字段集 --- 属性设置有效，因属于数据相关属性
        scrollPos: true, // 设定重载数据或切换分页时的滚动条的位置状态 --- 属性设置有效
    });
}

function startStreamAudio(audio_url, requestBody, audioId, finishCallback) {
    // 创建一个 Audio 元素
    const audioElement =  document.getElementById(audioId); // 使用已有的 audio 元素

    // 创建 MediaSource 实例
    const mediaSource = new MediaSource();
    audioElement.src = URL.createObjectURL(mediaSource);

    // 监听 durationchange 事件，以便在时长变化时更新 UI
    audioElement.addEventListener('durationchange', () => {
        console.log('音频时长已更新:', audioElement.duration);
    });


    mediaSource.addEventListener('sourceopen', function() {
        const audioSourceBuffer = mediaSource.addSourceBuffer('audio/aac'); // 根据音频格式选择适合的 MIME 类型

        // 定义一个队列来存储待追加的数据块
        const pendingBuffers = [];
        let appending = false;
        let finished = false;
        let firstBufferReceived = false;
        
        // 获取流式音频数据
        const fetchAudioStream = async () => {
            const response = await fetch(audio_url, {
                method: 'POST', // 请求方法
                headers: {
                    'Content-Type': 'application/json', // 设置请求体的内容类型
                },
                body: JSON.stringify(requestBody) // 将请求体转换为 JSON 字符串
            }); // 替换为后台音频流的 URL
            const reader = response.body.getReader();

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    if (!audioSourceBuffer.updating) {
                        mediaSource.endOfStream(); // 当流结束时调用
                        console.log('流已结束2');
                    }
                    finished = true
                    break;
                }
                
                console.log('分段接收value')
                
                // audioSourceBuffer.appendBuffer(value); // 动态将音频数据追加到 SourceBuffer 中

                // 将数据块加入待追加队列
                pendingBuffers.push(value);

                // 如果当前没有正在进行的 appendBuffer 操作，则开始追加
                if (!appending) {
                    processPendingBuffers();
                }
            }
            
        };

        // 处理待追加的数据队列
        function processPendingBuffers() {
            if (pendingBuffers.length > 0 && !appending) {
                const buffer = pendingBuffers.shift();
                appending = true;
                audioSourceBuffer.appendBuffer(buffer);
                audioSourceBuffer.addEventListener('updateend', () => {
                    console.log('数据块已追加');
                    appending = false;

                    // 在接收到第一个数据块时开始播放音频
                    if (!firstBufferReceived) {
                        firstBufferReceived = true;
                        console.log('接收到第一个数据块，开始播放音频');
                        audioElement.play().catch(error => {
                            console.error('播放失败:', error);
                        });

                        // 添加一个事件监听器来检测音频播放结束
                        audioElement.addEventListener('ended', () => {
                            console.log('音频播放完成');
                            finishCallback()
                        }, { once: true }); // 使用一次性的监听器
                    }

                    if (finished && pendingBuffers.length === 0) {
                        mediaSource.endOfStream(); // 当流结束时调用
                        console.log('流已结束1');
                    } else {
                        processPendingBuffers(); // 继续处理队列中的其他数据块
                    }
                }, { once: true });
            }
        }

        fetchAudioStream().catch(error => {
            console.error('Error streaming audio:', error);
        });
    });
}

async function fetchAndPlayAudio(audio_url, requestBody, audioId) {

    // 加载层
    const loadIndex = layui.layer.load(0);
    
    // 通过 fetch 请求流式获取音频数据
    const response = await fetch(audio_url, {
        method: 'POST', // 请求方法
        headers: {
            'Content-Type': 'application/json', // 设置请求体的内容类型
        },
        body: JSON.stringify(requestBody) // 将请求体转换为 JSON 字符串
    }); // 后端返回流式音频的 URL
    const reader = response.body.getReader();
    let chunks = []; // 用于存储音频数据的所有片段
    let receivedLength = 0; // 记录接收的字节总数

    // 循环读取每个数据块，直到读取完成
    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break; // 读取完成
        }
        chunks.push(value); // 将每个数据块存储到 chunks 数组中
        receivedLength += value.length; // 更新接收到的数据总长度
    }

    // 将所有数据块合并成一个完整的 Uint8Array
    let audioArray = new Uint8Array(receivedLength);
    let position = 0;
    for (let chunk of chunks) {
        audioArray.set(chunk, position);
        position += chunk.length;
    }

    // 将 Uint8Array 转换为 Blob
    const audioBlob = new Blob([audioArray], { type: 'audio/wav' }); // 根据实际的音频类型设置 Blob 类型
    const audioUrl = URL.createObjectURL(audioBlob);
    
    // 获取现有的 audio 元素并更新其 src 属性
    const audioElement = document.getElementById(audioId); // 使用已有的 audio 元素
    audioElement.src = audioUrl; // 更新音频文件的 URL

    layui.layer.close(loadIndex)
    
    audioElement.play(); // 播放音频
}

