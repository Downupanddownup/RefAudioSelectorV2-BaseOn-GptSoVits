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


function initTextarea(id) {
    $('#'+id).on('input',function () {
        $(this).css('height',$('#'+id)[0].scrollHeight+'px')
    })
    $('#'+id).css('height',$('#'+id)[0].scrollHeight+'px').css('overflow','hidden')
}

