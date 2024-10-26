
class AudioRequestBody {
    constructor(data) {
        this.requestBody = data.requestBody || '';
        this.isEffective = data.isEffective || false;
    }
}

class TTSPlayer {
    constructor(data) {
        this.audioUrl = data.audioUrl || ''; // 后台TTS服务URL
        this.audioId = data.audioId || ''; // 音频元素的ID
        this.mediaType = data.mediaType || 'aac';
        this.requestBodies = data.requestBodies.map(item => new AudioRequestBody(item)) || [];
        this.currentIndex = data.currentIndex || 0;
        this.audioStartCallback = data.audioStartCallback || function(index) {};
        this.audioQueue = []; // 音频播放队列
        this.isPlaying = false; // 标记是否正在播放
        this.hasLoadFinished = false; // 标记是否已经全部加载完成

        this.audioElement = document.getElementById(this.audioId);

        console.log('requestBodies', this.requestBodies)

    }

    getIsEffectiveItem() {
        const _this = this
        if (_this.currentIndex >= _this.requestBodies.length) {
            return {
                audioChunk: null,
                index: -1
            }
        }
        let audioChunk = _this.requestBodies[_this.currentIndex]
        let index = _this.currentIndex
        _this.currentIndex++
        do {
            if (audioChunk.isEffective) {
                return {
                    audioChunk: audioChunk,
                    index: index
                }
            }
            audioChunk = _this.requestBodies[_this.currentIndex]
            index = _this.currentIndex
            _this.currentIndex++
        } while (_this.currentIndex < _this.requestBodies.length)
        return {
            audioChunk: null,
            index: -1
        }
    }

    async start() {
        const _this = this
        // 开始播放首段音频

        const { audioChunk, index } = this.getIsEffectiveItem()
        if (!audioChunk) {
            return
        }

        _this.audioStartCallback(index)
        if (_this.currentIndex >= _this.requestBodies.length) {
            _this.hasLoadFinished = true
        }
        this.loadFirstAudioChunk(audioChunk.requestBody, () => _this.playNextAudio());
        await _this.loadNextAudioChunks()
        await _this.loadNextAudioChunks()
    }

    // 使用 MediaSource 加载首段音频
    loadFirstAudioChunk(requestBody, finishCallback) {
        const _this = this
        // 创建一个 Audio 元素
        const audioElement =  _this.audioElement;

        // 创建 MediaSource 实例
        const mediaSource = new MediaSource();
        audioElement.src = URL.createObjectURL(mediaSource);

        mediaSource.addEventListener('sourceopen', function() {
            const audioSourceBuffer = mediaSource.addSourceBuffer('audio/'+_this.mediaType); // 根据音频格式选择适合的 MIME 类型

            // 定义一个队列来存储待追加的数据块
            const pendingBuffers = [];
            let appending = false;
            let finished = false;
            let firstBufferReceived = false;

            // 获取流式音频数据
            const fetchAudioStream = async () => {
                const response = await fetch(_this.audioUrl, {
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
    } // 预加载下一个音频块，并将其加入播放队列
    async loadNextAudioChunks() {
        const _this = this
        let num = 0
        const { audioChunk, index } = this.getIsEffectiveItem()
        if (!audioChunk) {
            return
        }
        console.log('开始加载音频:'+index)
        const audioData = await this.fetchTTSStream(audioChunk.requestBody);
        this.audioQueue.push({
            audioData: audioData,
            index: index
        }); // 将音频数据加入队列
        console.log('完成音频加载:'+index)
        if (_this.currentIndex >= _this.requestBodies.length) {
            _this.hasLoadFinished = true
        }
    }

    // 异步获取 TTS 服务返回的音频流
    async fetchTTSStream(requestBody) {
        const _this = this
        const response = await fetch(_this.audioUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        const reader = response.body.getReader();
        const audioChunks = [];
        let done, value;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            audioChunks.push(value);
        }

        return new Blob(audioChunks, { type: 'audio/' + _this.mediaType });
    }

    // 播放下一段音频
    // 播放下一段音频
    playNextAudio() {
        const _this = this;

        if (_this.hasLoadFinished && _this.audioQueue.length === 0) {
            return
        }

        let count = 0;

        const checkInterval = 100; // 设置轮询间隔（毫秒）
        // 定义一个定时器，定期检查音频队列
        const checkForAudioToPlay = setInterval(() => {

            if (count >= 100) {
                clearInterval(checkForAudioToPlay); // 一旦开始播放，停止轮询
            }
            count++;

            // console.log('当前音频队列数：', _this.audioQueue)
            if (_this.audioQueue.length > 0 && !_this.isPlaying) {
                clearInterval(checkForAudioToPlay); // 一旦开始播放，停止轮询
                const { audioData, index} = _this.audioQueue.shift(); // 从队列中获取下一段音频
                _this.audioElement.src = URL.createObjectURL(audioData);
                _this.isPlaying = true;

                // 播放当前音频
                _this.audioElement.play().then(() => {
                    // console.log('开始播放:' + index);
                    _this.audioStartCallback(index)
                    _this.loadNextAudioChunks(); // 播放时继续加载下一段音频
                }).catch(error => {
                    console.error('播放失败:', error);
                });

                // 播放结束后继续播放下一段
                _this.audioElement.addEventListener('ended', async () => {
                    _this.isPlaying = false;
                    _this.playNextAudio(); // 播放下一段
                }, { once: true });
            }
        }, checkInterval); // 每隔 100 毫秒检查一次队列

    }
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