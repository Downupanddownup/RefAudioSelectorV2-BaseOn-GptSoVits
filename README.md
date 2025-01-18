# RefAudioSelectorV2-BaseOn-GptSoVits

1. 为什么开发这个项目

   2024年五一的时候发布了一个v1版本，用来简化参考音频的筛选。但是那个功能做的比较粗糙，在后面做模型训练的过程中，发现了很多不足之处，所以基于当时的体验，我设计了这个v2版本，进一步降低筛选参考音频的时间成本。
2. 项目有什么亮点
    1. 对参考音频做了集中管理，无论是后续做人工校准，还是切换参考音频，都很方便

       ![](readmeimage/image_7b2pMBqPC9.png)
    2. 添加更全面的参数对比，除了参考音频对比，还添加了Gpt模型、SoVits模型、topK、topP、temperature、文本分隔符、音频语速、融合音频等单变量对比，以及 组合模型、kpt三参数等多变量对比

       ![](readmeimage/image_y6WqprcVTA.png)
    3. 结果音频按时长排序，不同参考音频对模型推理的语速效果是存在影响的，根据推理结果音频的排序，可以快速确定一批需要重点关注的音频对象

       ![](readmeimage/image_acQ04bTHLQ.png)
    4. 音频结果可视化，添加结果音频频谱图，可以直观的发现大段电音、复读、吞句、以及频繁换气之类的问题，减轻耳朵的负担

       ![](readmeimage/image_4UOV7eCnQ0.png)
    5. 提供了结果音频打分功能，可以记录自己对此推理结果的评分，便于后续筛选
    6. 音频分类，对于参考音频片段多的角色，比如一千以上的参考音频片段，提供了基于阿里的说话识别模型，进行音频分类的功能

       ![](readmeimage/image_fRhEpffp4w.png)
    7. 参考音频切分，对于10s以上的参考音频，以及整体不错，但是存在部分瑕疵，需要微调的参考音频，可以利用音频切分功能进行拆分

       ![](readmeimage/image_FbAtRkSOyY.png)
3. 主体流程
    1. 按照【分类-名称】创建角色，比如，男性-张三

       ![](readmeimage/image_yWDrHt_0gN.png)
    2. 将GptSoVits模型生成的list文件导入到本系统中

       ![](readmeimage/image_KrRi3UDBQW.png)
    3. （可选）对导入的参考音频进行分类

       ![](readmeimage/image_KU3oDkr1cL.png)

       ![](readmeimage/image_FX66QtZUJS.png)

       ![](readmeimage/image_g0mqvulKlO.png)

       ![](readmeimage/image_fRhEpffp4w.png)

       ![](readmeimage/image_YcY0kXc8_H.png)
    4. 创建基于参考音频参数的对比任务

       ![](readmeimage/image_su3njR3Vmj.png)

       ![](readmeimage/image_y6WqprcVTA.png)
    5. 推理结果音频

       ![](readmeimage/image_PD-VnUc7zy.png)
    6. 在结果评测界面依次评测音频，并打分

       ![](readmeimage/image_nAg-AWlPpR.png)

       ![](readmeimage/image_4UOV7eCnQ0.png)
    7. 在长文测试环节，挑选最高评分音频进行测试并打分

       ![](readmeimage/image_LOHpqc5yWt.png)

       ![](readmeimage/image_tXDEFnIB77.png)

       ![](readmeimage/image_O9gmlSN_WO.png)

       ![](readmeimage/image_VyB9xrpL2-.png)

       ![](readmeimage/image_e8au0Pi3G7.png)
    8. 将最符合期望的音频放入成品管理

       ![](readmeimage/image_nTfFgfISP2.png)

       ![](readmeimage/image_uEEVwZkVe3.png)
    9. 如果没有找到合适的参考音频，可以前往推理任务界面调整对比参数，比如降低Gpt模型轮数，重新启动流程。
    10. 如果绝大部分结果音频的质量都非常糟糕，应考虑寻找更高质量的基础音频重新训练模型
    11. 如果发现某个参考音频非常契合期望，但是存在部分瑕疵，可以对此音频进行分割，挑选子音频进行推理测试，或许能找到更完美的推理结果

        ![](readmeimage/image_FbAtRkSOyY.png)
4. 技术结构
    1. 以SQLite作为数据库
    2. 用layui设计前端界面
    3. 后端采用python
    4. 依赖GptSoVits项目和其运行环境
    5. 对GptSoVits项目的少部分代码做了调整，主要是切换模型加载的路径（我将GSV项目的工作目录切换到了本项目下，因此GSV模型加载路径需要调整），以及处理一个阿里说话人识别模型在windows环境下运行存在的兼容性问题

