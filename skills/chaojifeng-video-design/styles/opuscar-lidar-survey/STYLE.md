# 点云测绘

采用点云测绘的材质、构图、运动与声画语法组织当前题材。

## 使用顺序

先确定本片主线与镜头目的，再完整读取 [上游风格规则](STYLE.upstream.md)。选用其中的材质、色彩、文字、运动、镜头、声音、原生动作与失败修复；本包收录章节为Essence, and what it is not、Materials & rendering、Colour logic、Type & subtitles、Motion quality、Camera grammar、Sound palette、Native moves、Pitfalls of the medium、Engine、Variation space。

本片的事实、品牌、用户指定音乐、语言、画幅和交付节奏优先。固定模型、120 BPM、双语字幕、必须虚构产品、指定开头结尾、固定静默或运镜数量属于来源约束，按本片明确需求判断；改变风格核心时记录覆盖理由。原生材质与动作需要对应实现，导航色板不代表本风格外观。

## 实现与案例

本片结构确定后再读 [案例说明](DEMO.md)，按其 Engine 章节定位 `demo/` 中的代码；从中复用笔刷、遮罩、材质、角色、相机或声画排程。源代码保留原状，先复制到项目并修正资源路径，不能直接运行库内的 build.sh。共享工具位于 `../../vendor/lemo-opuscar/`；这是源码参考，需要本片环境实际探测与接入。

读取 [素材来源](demo/CREDITS) 后，先复用本片授权资产，再补字体、声音或模型。源码、素材就绪、关键帧、成片导出、观看和听审分别登记；本包当前未通过本机整片制作验收。

## 组合与扩展

单片颜色与音色写 plan.design.style_overrides；稳定个人风格在项目外置集合中用新 ID 和 extends 登记。borrows 只声明借用来源，具体借用的动作和冲突处理写入镜头，不自动合并场景或覆盖声音。
