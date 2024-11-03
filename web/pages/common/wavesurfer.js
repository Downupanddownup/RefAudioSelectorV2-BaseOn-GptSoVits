const WavesurferSpace = (function () {
    class Param {
        constructor(data) {
            this.container = data.container || '';
            this.audioId = data.audioId || '';
            this.audioSrc = data.audioSrc || '';
            this.waveHeight = data.waveHeight || 128;
            this.spectrogramHeight = data.spectrogramHeight || 128;
            this.type = data.type || 'waveform';// waveform, spectrogram, all
            this.zoom = data.zoom || 'open';// close open
        }
    }
    
    class WavesurferManager {
        constructor(data) {
            this.wavesurfer = data.wavesurfer || null
            this.regionManager = data.regionManager || null
            this.shadowRoot = data.shadowRoot || null
            this.audioElement = data.audioElement || null
            this.loop = false
        }

        randomColor() {
            const random = (min, max) => Math.random() * (max - min) + min
            return `rgba(${random(0, 255)}, ${random(0, 255)}, ${random(0, 255)}, 0.5)`
        }
        
        registerDragSelection(callback){
            const _this = this
            _this.regionManager.on('region-created', (region) => {
                console.log('region-created', region)
                region.content = `区域${_this.regionManager.getRegions().length}`
                const regionObj = $(_this.shadowRoot).find(`div[part='region ${region.id}']`)
                regionObj.find('div[part=region-content]').html(region.content)
                regionObj.css('background-color', _this.randomColor())
                if (callback) {
                    callback(region)
                }
            })

            _this.regionManager.enableDragSelection({
                content: `标题`,
                color: _this.randomColor(),
            })
        }

        registerLoop(){
            const _this = this
            let activeRegion = null
            _this.regionManager.on('region-in', (region) => {
                console.log('region-in', region)
                activeRegion = region
            })
            _this.regionManager.on('region-out', (region) => {
                console.log('region-out', region)
                if (activeRegion === region) {
                    if (_this.loop) {
                        region.play()
                    } else {
                        activeRegion = null
                    }
                }
            })
            _this.regionManager.on('region-clicked', (region, e) => {
                e.stopPropagation() // prevent triggering a click on the waveform
                activeRegion = region
                region.play()
                region.setOptions({ color: _this.randomColor() })
            })
        }

        playIntervals(regionIds) {
            const _this = this
            const audio = _this.audioElement

            // 重置音频播放
            audio.currentTime = 0;
            audio.pause();
            _this.currentIntervalIndex = 0

            // 定义更新播放状态的函数
            function updatePlayback() {
                const currentInterval = _this.getRegionById(regionIds[_this.currentIntervalIndex])
                
                // 检查当前时间是否超过当前区间结束时间
                if (audio.currentTime >= currentInterval.end) {
                    audio.pause();
                    _this.currentIntervalIndex++;
                    if (_this.currentIntervalIndex < regionIds.length) {
                        playNextInterval();
                    } else {
                        // 所有区间播放完毕，可以做一些结束处理
                        console.log("All intervals played.");
                    }
                }

                // 请求下一帧更新
                requestAnimationFrame(updatePlayback);
            }

            // 播放下一个区间
            function playNextInterval() {
                const nextInterval = _this.getRegionById(regionIds[_this.currentIntervalIndex])
                audio.currentTime = nextInterval.start;

                audio.play();
                // 开始更新播放状态
                requestAnimationFrame(updatePlayback);
            }

            // 开始播放第一个区间
            playNextInterval();
        }
        
        getRegionById(id){
            return this.regionManager.getRegions().find(region => region.id === id)
        }
        
        removeRegion(id){
            const region = this.getRegionById(id)
            if (region) {
                region.remove()
            }
        }
        
    }
    
    function createWave(param) {
        param = new Param(param)
        const audio = document.getElementById(param.audioId);

        audio.src = param.audioSrc

        // Create a second timeline
        const timeline = WaveSurfer.Timeline.create({
            height: 10,
            timeInterval: 0.1,
            primaryLabelInterval: 1,
            style: {
                fontSize: '10px',
                color: '#6A3274',
            },
        })

        const hover =  WaveSurfer.Hover.create({
            lineColor: '#ff0000',
            lineWidth: 2,
            labelBackground: '#555',
            labelColor: '#fff',
            labelSize: '11px',
        })

        const regions = WaveSurfer.Regions.create()

        // Create an instance of WaveSurfer 
        const wavesurfer = WaveSurfer.create({
            container: param.container,
            waveColor: 'rgb(200, 0, 200)',
            progressColor: 'rgb(100, 0, 100)',
            media: audio,
            height: param.waveHeight,
            // minPxPerSec: 100,
            // sampleRate: 32000,
            // interact:true,
            plugins: [timeline,hover,regions]
        })

        if (param.zoom === 'open') {
            // Initialize the Zoom plugin
            wavesurfer.registerPlugin(
                WaveSurfer.Zoom.create({
                    // the amount of zoom per wheel step, e.g. 0.5 means a 50% magnification per scroll
                    scale: 0.5,
                    // Optionally, specify the maximum pixels-per-second factor while zooming
                    maxZoom: 100,
                }),
            )
        }

        
        if (['spectrogram', 'all'].includes(param.type)) {
            // Initialize the Spectrogram plugin
            wavesurfer.registerPlugin(
                WaveSurfer.Spectrogram.create({
                    labels: true,
                    height: param.spectrogramHeight,
                    scale: 'linear',
                    splitChannels: true,
                })
            )
        }

        // 获取宿主元素
        const resultWaveForm = document.querySelector(param.container);

        // 获取第一个子 div
        const hostElement = resultWaveForm.querySelector('div:first-child');

        // 获取 Shadow Root
        const shadowRoot = hostElement.shadowRoot;

        if (param.type === 'spectrogram') {
          
            $(shadowRoot).find('div[part=canvases]').hide()
        }
        
        return new WavesurferManager({
            wavesurfer: wavesurfer,
            regionManager: regions,
            shadowRoot: shadowRoot,
            audioElement: audio
        })

    }
    
    return {
        createWave: createWave
    }
    
})()