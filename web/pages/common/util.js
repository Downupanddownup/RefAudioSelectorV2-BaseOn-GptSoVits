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

function getExtension(filePath) {
    if (!filePath) {
        return '';
    }
    // 从右向左找到第一个点的位置，以此作为扩展名的开始位置
    const lastDotIndex = filePath.lastIndexOf('.');
    // 如果找不到点或者点位于文件路径的开头（即没有扩展名），则返回空字符串
    if (lastDotIndex === -1 || lastDotIndex === filePath.length - 1) {
        return '';
    }
    // 提取扩展名
    return filePath.substring(lastDotIndex + 1);
}

function createXmSelect(el, dataList, callback) {
    const choiceList = dataList.map(item => {
        return {
            name: item.name,
            value: item.name,
            selected: item.selected
        }
    })

    xmSelect.render({
        el: el,
        tips: '选择或新建',
        searchTips: '选择或新建',
        radio: true,
        clickClose: true,
        filterable: true,
        create: function(val, arr){
            if(arr.length === 0){
                return {
                    name: val,
                    value: val,
                }
            }
        },
        model: {
            icon: 'hidden',
            label: {
                type: 'text',
            }
        },
        data: choiceList,
        on: function(data){
            //arr:  当前多选已选中的数据
            const arr = data.arr;
            //change, 此次选择变化的数据,数组
            const change = data.change;
            //isAdd, 此次操作是新增还是删除
            const isAdd = data.isAdd;

            //可以return一个数组, 代表想选中的数据
            //return []
            console.log('xm-select', data)
            const selectedName = arr[0].value

            if (selectedName) {
                if (!choiceList.find(item => item.value === selectedName)) {
                    choiceList.forEach(item => item.selected = false)
                    choiceList.push({
                        name: selectedName,
                        value: selectedName,
                        selected: true
                    })
                }
                xmSelect.get(el, true).update({
                    data:choiceList
                })
            }
            
            if (callback) {
                callback(data)
            }

        },
    })
}

function setTips(el, content) {
    tippy(el, {
        content:content,
        allowHTML:true,
        interactive:true,
        duration: [200, 200],
        animation:'scale',
        inertia: true,
        arrow: true,
        theme: 'material',
        // delay: [500, 200]
    });
}
