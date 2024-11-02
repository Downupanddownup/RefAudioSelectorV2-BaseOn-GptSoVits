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
    
    function createWave(param) {
        param = new Param(param)
        const audio = document.getElementById(param.audioId);

        audio.src = param.audioSrc

        // Create a second timeline
        const bottomTimeline = WaveSurfer.Timeline.create({
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

        const regionsManager = WaveSurfer.Regions.create()

        // Create an instance of WaveSurfer 
        const wavesurfer = WaveSurfer.create({
            container: param.container,
            waveColor: 'rgb(200, 0, 200)',
            progressColor: 'rgb(100, 0, 100)',
            media: audio,
            height: param.waveHeight,
            // minPxPerSec: 100,
            // sampleRate: 32000,
            plugins: [bottomTimeline,hover,regionsManager]
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


        if (param.type === 'spectrogram') {
            // 获取宿主元素
            const resultWaveForm = document.querySelector(param.container);

            // 获取第一个子 div
            const hostElement = resultWaveForm.querySelector('div:first-child');

            // 获取 Shadow Root
            const shadowRoot = hostElement.shadowRoot;
            $(shadowRoot).find('div[part=canvases]').hide()
        }

    }
    
    return {
        createWave: createWave
    }
    
})()