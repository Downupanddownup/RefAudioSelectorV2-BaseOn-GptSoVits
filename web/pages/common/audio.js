
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



async function fetchAudioBlob(audio_url) {

    // 通过 fetch 请求流式获取音频数据
    const response = await fetch(audio_url); // 后端返回流式音频的 URL
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

    return {
        audioBlob: audioBlob,
        audioUrl: audioUrl
    }

}

async function mergeSlices(blob, timeRanges) {
    console.log('timeRanges', timeRanges)
    const arrayBuffer = await blob.arrayBuffer();
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

    const channels = audioBuffer.numberOfChannels;
    const rate = audioBuffer.sampleRate;

    // 计算最终合并后的AudioBuffer长度
    const totalFrames = timeRanges.reduce((sum, {start, end}) => sum + (Math.floor(end * rate) - Math.floor(start * rate)), 0);
    console.log('totalFrames', totalFrames)
    // const newAudioBuffer = audioCtx.createBuffer(channels, totalFrames, rate);
    const newAudioBuffer = new AudioContext().createBuffer(channels, totalFrames, rate);

    let currentOffset = 0;

    for (const {start, end} of timeRanges) {
        const startOffset = Math.floor(start * rate);
        const endOffset = Math.floor(end * rate);
        const frameCount = endOffset - startOffset;
        
        console.log('startOffset', startOffset)
        const tempArray = new Float32Array(frameCount);

        // 创建临时Array存放复制的buffer数据
        for (let channel = 0; channel < channels; channel++) {
            audioBuffer.copyFromChannel(tempArray, channel, startOffset);
            newAudioBuffer.copyToChannel(tempArray, channel, currentOffset);
        }

        currentOffset += frameCount;
    }

    return bufferToWave(newAudioBuffer, totalFrames);
}


async function sliceBlob(blob, startTime, endTime) {
    const arrayBuffer = await blob.arrayBuffer();
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    // 解码音频数据
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

    // 声道数量和采样率
    const channels = audioBuffer.numberOfChannels;
    const rate = audioBuffer.sampleRate;

    //  计算提取的样本范围
    const startOffset = Math.floor(startTime * rate);
    const endOffset = Math.floor(endTime * rate);
    // 对应的帧数
    const frameCount = endOffset - startOffset;

    // 创建同样采用率、同样声道数量，长度是前3秒的空的AudioBuffer
    const newAudioBuffer = new AudioContext().createBuffer(channels, endOffset - startOffset, rate);
    // 创建临时的Array存放复制的buffer数据
    const anotherArray = new Float32Array(frameCount);
    // 声道的数据的复制和写入
    const offset = 0;
    for (let channel = 0; channel < channels; channel++) {
        audioBuffer.copyFromChannel(anotherArray, channel, startOffset);
        newAudioBuffer.copyToChannel(anotherArray, channel, offset);
    }

    // newAudioBuffer就是全新的复制的3秒长度的AudioBuffer对象
    return bufferToWave(newAudioBuffer, frameCount);
}


// Convert AudioBuffer to a Blob using WAVE representation
function bufferToWave(abuffer, len) {
    let numOfChan = abuffer.numberOfChannels,
        length = len * numOfChan * 2 + 44,
        buffer = new ArrayBuffer(length),
        view = new DataView(buffer),
        channels = [], i, sample,
        offset = 0,
        pos = 0;

    // write WAVE header
    // "RIFF"
    setUint32(0x46464952);
    // file length - 8                      
    setUint32(length - 8);
    // "WAVE"                     
    setUint32(0x45564157);
    // "fmt " chunk
    setUint32(0x20746d66);
    // length = 16                       
    setUint32(16);
    // PCM (uncompressed)                               
    setUint16(1);
    setUint16(numOfChan);
    setUint32(abuffer.sampleRate);
    // avg. bytes/sec
    setUint32(abuffer.sampleRate * 2 * numOfChan);
    // block-align
    setUint16(numOfChan * 2);
    // 16-bit (hardcoded in this demo)
    setUint16(16);
    // "data" - chunk
    setUint32(0x61746164);
    // chunk length                   
    setUint32(length - pos - 4);

    // write interleaved data
    for(i = 0; i < abuffer.numberOfChannels; i++)
        channels.push(abuffer.getChannelData(i));

    while(pos < length) {
        // interleave channels
        for(i = 0; i < numOfChan; i++) {
            // clamp
            sample = Math.max(-1, Math.min(1, channels[i][offset]));
            // scale to 16-bit signed int
            sample = (0.5 + sample < 0 ? sample * 32768 : sample * 32767)|0;
            // write 16-bit sample
            view.setInt16(pos, sample, true);
            pos += 2;
        }
        // next source sample
        offset++
    }

    // create Blob
    return new Blob([buffer], {type: "audio/wav"});

    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }

    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
}


function downloadAudio(audioPath, filename) {
    fetch(audioPath, {
        method: 'GET',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok ${response.status}`);
            }
            // 创建一个 Blob 对象，并使用 URL.createObjectURL 方法创建一个临时的 URL
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename); // 自定义下载的文件名
            document.body.appendChild(link);
            link.click(); // 触发点击下载
            document.body.removeChild(link); // 移除下载链接
            window.URL.revokeObjectURL(url); // 释放 URL 对象
        })
        .catch(e => console.error('There has been a problem with your fetch operation:', e));
}