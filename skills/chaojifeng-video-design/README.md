# 超级峰的视频设计方法论

一个帮助 AI Agent 设计和制作视频的 Skill。把主题、产品和素材变成可修改的分镜与制作计划，组织镜头、文字、旁白、音乐和节奏，再完成预览、审片、返修与成片交付。

适合产品演示、知识讲解、音乐科普、说唱科普、资讯、图片成片、故事和品牌短片。也可以只做方案、分镜、单个动效或已有作品的局部修改。

| 视频任务 | 可选风格 | 随库样片 | 基础动效 | 表达指导 | 组合配方 |
| --- | --- | --- | --- | --- | --- |
| **8 类** | **66 套** | **59 条** | **12 项** | **64 项** | **18 类** |

具体制作沿用项目已有工具，渲染、配音和导出由运行 Skill 的 Agent 环境提供。

[开始使用](#开始使用) · [本库能力与来历](#能力从哪里来) · [七套基础风格](#本库维护的七套基础风格) · [59 套集成风格](#开源集成的-59-套影片风格) · [风格画廊](assets/gallery/index.html)

## 能力从哪里来

本库把创作方法、风格资源和制作工具组织在一起。下面按实际来源说明各部分，便于选择和继续扩展。

| 组成 | 来历与维护 | 能带来什么 |
| --- | --- | --- |
| 导演方法、场景编排、表达目录与组合配方 | 本库结合创作实践和外部研究，原创归纳与适配 | 从观众要理解什么出发，安排主线、镜头、证据、声音和修改 |
| 7 套基础风格 | 本库原有配置与规则，持续维护 | 产品、阅读、关系图、影像、拼贴和发布片的常用起点 |
| 59 套影片风格、代表帧、案例与样片 | 集成自 [LemoLab · Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 补充水墨、版画、纪实、像素、卡通、材质与 3D 等表达 |
| 统一风格包、中文查询、外置集合和离线画廊 | 本库参考 Lemo-Opuscar 的工程分层后独立适配 | 让原有与集成风格进入同一目录，可查询、比较、派生和复用 |
| 计划与交付规范、素材与媒体检查、声音事件审计等工具 | 本库独立实现 | 检查时间、引用、文件、实际媒体信息和交付完整性 |

本库原创的部分集中在方法归纳、任务编排、配置、计划规范、工具和实践案例。设计与导演方法也参考了社区项目和创作者经验，具体借鉴与独立实现的关系见 [方法来源](references/sources.md)。

## 8 类视频任务

![八类视频场景的组织链路与观众所得](assets/diagrams/scenario-routes.png)

| 场景 | 怎样组织内容 | 观众所得 |
| --- | --- | --- |
| 产品演示 | 真实任务 → 关键操作 → 结果证据 | 看懂产品能做什么 |
| 知识讲解 | 核对事实 → 建立关系 → 逐层解释 | 理解概念、关系或过程 |
| 资讯呈现 | 核对来源 → 梳理变化 → 组织证据 | 知道发生了什么 |
| 图片成片 | 素材排序 → 焦点移动 → 转场接力 | 图片连成一段表达 |
| 故事视频 | 人物目标 → 事件推进 → 转折收束 | 跟随一个故事 |
| 功能动效 | 初始状态 → 操作触发 → 变化反馈 | 看懂交互如何发生 |
| 品牌形象短片 | 品牌主张 → 视觉母题 → 记忆落点 | 记住品牌的感受 |
| 音乐与视觉表演 | 乐段结构 → 动机变奏 → 高潮释放 | 体验声音与画面的共振 |

知识讲解还包含概念知识科普和嘻哈知识科普两种编排。可以由旁白、音乐、歌词、过程或关系领拍，按题材选择。

## 本库的导演与制作能力

| 能力 | 在作品里怎样使用 | 进一步阅读 |
| --- | --- | --- |
| 主线与镜头设计 | 明确观众变化、每镜焦点、揭示顺序、稳定停留与下一镜接力 | [创意导演](references/creative-direction.md) |
| 首帧与前三秒 | 用主体、任务或变化建立开场，检查重点和信息密度 | [开场设计](references/opening-design.md) |
| 产品任务证明 | 围绕真实操作组织界面、结果和对照，让功能有画面依据 | [产品表达](references/product-expression.md) |
| 概念知识科普 | 梳理事实、关系、载体与逐层揭示，按真实音乐和阅读时间编排 | [科普编排](references/knowledge-music-direction.md) |
| 嘻哈知识科普 | 先核知识与可唱歌词，再按真实音轨安排画面、字幕和声音落点 | [说唱编排](references/knowledge-rap-direction.md) |
| 旁白、字幕与音乐 | 先取得实际音频量时，安排乐段、主声、音效、字幕和接缝 | [声音与节奏](references/sound-and-rhythm.md) |
| 素材选择与调度 | 选择录屏、照片、影像、图形、生成素材与 3D，保留各自职责 | [素材路由](references/asset-routing.md) |
| 局部修改与审片 | 按镜头、对象或时间窗修改，复验受影响的字幕、声音与接缝 | [审片与修改](references/review-and-revision.md) |
| 连续制作或分阶段审阅 | 明确要求直接成片时连续完成；需要分镜审阅时在约定节点停下 | [制作流程](references/production-workflow.md) |

## 本库维护的七套基础风格

这些风格沿用本库原有 ID，可以直接作为常用视频的起点，再组合下面的表达与配方。

| 基础风格 | 画面方向 | 适合怎样的内容 |
| --- | --- | --- |
| [清晰产品](styles/product-minimal/STYLE.md) | 克制留白，突出界面和操作 | 产品介绍、功能演示、任务证明 |
| [纸面编辑](styles/paper-editorial/STYLE.md) | 纸面阅读与编辑排版 | 知识讲解、资料解释、阅读型内容 |
| [暗色技术](styles/dark-tech/STYLE.md) | 暗色空间与清晰的信息层次 | 技术说明、信息流、状态变化 |
| [单色图解](styles/mono-diagram/STYLE.md) | 用位置、线条和单色强调关系 | 系统机制、流程、概念解释 |
| [影像叙事](styles/cinematic-photo/STYLE.md) | 由照片和影像主体承担叙事 | 人物、旅行、图片成片、影像故事 |
| [鲜明拼贴](styles/vivid-collage/STYLE.md) | 图片切块、鲜明颜色与尺度变化 | 节奏短片、活动、品牌与音乐视觉 |
| [双底色发布片](styles/dual-ground-launch/STYLE.md) | 两块底色串联问题与解答 | 产品发布、功能章节、任务前后变化 |

## 创作案例与实践积累

### 小圆角

https://github.com/user-attachments/assets/d87f8264-0a95-40d6-adbb-4e7e0afa32d3

22 秒竖屏片段，将圆角滑动、九张批量处理与小卡环形展示串成一段。点击播放器观看，可通过音量按钮开启声音。

### AI 闯关记

https://github.com/user-attachments/assets/bced29b5-a55a-4f92-85a5-865c6730752a

约 18.6 秒横屏高亮，将开机倒数与“升级闯关”副歌串联。点击播放器观看，可通过音量按钮开启声音。

两部作品均在 Cursor 中协作制作。选段、方法对应和创作来源见 [案例说明](examples/showcase/README.md)。

## 开源集成的 59 套影片风格

以下风格、代表帧与样片来自 [LemoLab · Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar)，感谢作者开放分享。本库将它们接入统一风格包和中文目录，保留规则、案例说明、可用文本源码与样片，供当前作品选择和改编。

点画面查看风格规则，点“样片”打开本仓库中的视频。59 条样片随库分发，下载完整目录后可在 [风格画廊](assets/gallery/index.html) 离线播放；其中三条保留画面并移除了受限音轨。来源与变更见 [素材清单](THIRD_PARTY_NOTICES.md)。

### 剪辑与纪实 · 8 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-caption-news/STYLE.md"><img src="styles/opuscar-caption-news/preview.jpg" alt="字幕新闻" width="300"></a><br><b>字幕新闻</b><br><sub>Caption News</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-caption-news/STYLE.md">规则</a> · <a href="styles/opuscar-caption-news/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-city-symphony/STYLE.md"><img src="styles/opuscar-city-symphony/preview.jpg" alt="延时交响" width="300"></a><br><b>延时交响</b><br><sub>Time-lapse Symphony</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-city-symphony/STYLE.md">规则</a> · <a href="styles/opuscar-city-symphony/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-countdown/STYLE.md"><img src="styles/opuscar-countdown/preview.jpg" alt="实时倒计时分屏" width="300"></a><br><b>实时倒计时分屏</b><br><sub>Live Countdown Split-screen</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-countdown/STYLE.md">规则</a> · <a href="styles/opuscar-countdown/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-kino-montage/STYLE.md"><img src="styles/opuscar-kino-montage/preview.jpg" alt="构成主义蒙太奇" width="300"></a><br><b>构成主义蒙太奇</b><br><sub>Constructivist Montage</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-kino-montage/STYLE.md">规则</a> · <a href="styles/opuscar-kino-montage/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-news-package/STYLE.md"><img src="styles/opuscar-news-package/preview.jpg" alt="电视新闻包装" width="300"></a><br><b>电视新闻包装</b><br><sub>Broadcast News Package</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-news-package/STYLE.md">规则</a> · <a href="styles/opuscar-news-package/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-newsreel/STYLE.md"><img src="styles/opuscar-newsreel/preview.jpg" alt="1920s 新闻影片" width="300"></a><br><b>1920s 新闻影片</b><br><sub>1920s Newsreel</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-newsreel/STYLE.md">规则</a> · <a href="styles/opuscar-newsreel/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-telestrator/STYLE.md"><img src="styles/opuscar-telestrator/preview.jpg" alt="体育战术板" width="300"></a><br><b>体育战术板</b><br><sub>Sports Telestrator</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-telestrator/STYLE.md">规则</a> · <a href="styles/opuscar-telestrator/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-visual-investigation/STYLE.md"><img src="styles/opuscar-visual-investigation/preview.jpg" alt="视觉调查" width="300"></a><br><b>视觉调查</b><br><sub>Visual Investigation</sub><br><sub>资讯呈现／故事视频／图片成片</sub><br><a href="styles/opuscar-visual-investigation/STYLE.md">规则</a> · <a href="styles/opuscar-visual-investigation/sample.mp4">样片</a></td>
</tr>
</table>

### 实证影像 · 8 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-archive-lighttable/STYLE.md"><img src="styles/opuscar-archive-lighttable/preview.jpg" alt="档案灯台" width="300"></a><br><b>档案灯台</b><br><sub>Archive Light Table</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-archive-lighttable/STYLE.md">规则</a> · <a href="styles/opuscar-archive-lighttable/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-briefing-board/STYLE.md"><img src="styles/opuscar-briefing-board/preview.jpg" alt="工程简报板" width="300"></a><br><b>工程简报板</b><br><sub>Engineering Briefing Board</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-briefing-board/STYLE.md">规则</a> · <a href="styles/opuscar-briefing-board/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-data-physical/STYLE.md"><img src="styles/opuscar-data-physical/preview.jpg" alt="数据实物化" width="300"></a><br><b>数据实物化</b><br><sub>Data Physicalization</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-data-physical/STYLE.md">规则</a> · <a href="styles/opuscar-data-physical/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-lidar-survey/STYLE.md"><img src="styles/opuscar-lidar-survey/preview.jpg" alt="点云测绘" width="300"></a><br><b>点云测绘</b><br><sub>LiDAR Survey</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-lidar-survey/STYLE.md">规则</a> · <a href="styles/opuscar-lidar-survey/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-microscope/STYLE.md"><img src="styles/opuscar-microscope/preview.jpg" alt="显微叙事" width="300"></a><br><b>显微叙事</b><br><sub>Microscope Story</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-microscope/STYLE.md">规则</a> · <a href="styles/opuscar-microscope/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-satellite-briefing/STYLE.md"><img src="styles/opuscar-satellite-briefing/preview.jpg" alt="卫星简报" width="300"></a><br><b>卫星简报</b><br><sub>Satellite Briefing</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-satellite-briefing/STYLE.md">规则</a> · <a href="styles/opuscar-satellite-briefing/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-teardown/STYLE.md"><img src="styles/opuscar-teardown/preview.jpg" alt="产品拆解" width="300"></a><br><b>产品拆解</b><br><sub>Exploded Teardown</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-teardown/STYLE.md">规则</a> · <a href="styles/opuscar-teardown/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-white-model/STYLE.md"><img src="styles/opuscar-white-model/preview.jpg" alt="白模投影" width="300"></a><br><b>白模投影</b><br><sub>Projection on White Model</sub><br><sub>知识讲解／资讯呈现／产品演示</sub><br><a href="styles/opuscar-white-model/STYLE.md">规则</a> · <a href="styles/opuscar-white-model/sample.mp4">样片</a></td>
</tr>
</table>

### 手绘与绘画 · 7 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-crayon-book/STYLE.md"><img src="styles/opuscar-crayon-book/preview.jpg" alt="蜡笔儿童绘本" width="300"></a><br><b>蜡笔儿童绘本</b><br><sub>Crayon Picture Book</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-crayon-book/STYLE.md">规则</a> · <a href="styles/opuscar-crayon-book/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-impasto/STYLE.md"><img src="styles/opuscar-impasto/preview.jpg" alt="油画厚涂" width="300"></a><br><b>油画厚涂</b><br><sub>Impasto Oil Painting</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-impasto/STYLE.md">规则</a> · <a href="styles/opuscar-impasto/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-ink-wash/STYLE.md"><img src="styles/opuscar-ink-wash/preview.jpg" alt="中国水墨" width="300"></a><br><b>中国水墨</b><br><sub>Chinese Ink Wash</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-ink-wash/STYLE.md">规则</a> · <a href="styles/opuscar-ink-wash/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-one-line/STYLE.md"><img src="styles/opuscar-one-line/preview.jpg" alt="一笔画" width="300"></a><br><b>一笔画</b><br><sub>One-line Drawing</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-one-line/STYLE.md">规则</a> · <a href="styles/opuscar-one-line/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-urban-sketch/STYLE.md"><img src="styles/opuscar-urban-sketch/preview.jpg" alt="钢笔淡彩" width="300"></a><br><b>钢笔淡彩</b><br><sub>Urban Sketch · Pen &amp; Wash</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-urban-sketch/STYLE.md">规则</a> · <a href="styles/opuscar-urban-sketch/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-watercolor/STYLE.md"><img src="styles/opuscar-watercolor/preview.jpg" alt="水彩笔刷" width="300"></a><br><b>水彩笔刷</b><br><sub>Watercolor Brush</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-watercolor/STYLE.md">规则</a> · <a href="styles/opuscar-watercolor/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-whiteboard/STYLE.md"><img src="styles/opuscar-whiteboard/preview.jpg" alt="白板讲解" width="300"></a><br><b>白板讲解</b><br><sub>Whiteboard Explainer</sub><br><sub>故事视频／知识讲解／品牌形象短片</sub><br><a href="styles/opuscar-whiteboard/STYLE.md">规则</a> · <a href="styles/opuscar-whiteboard/sample.mp4">样片</a></td>
</tr>
</table>

### 东方传统 · 4 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-paper-lantern/STYLE.md"><img src="styles/opuscar-paper-lantern/preview.jpg" alt="纸雕灯影" width="300"></a><br><b>纸雕灯影</b><br><sub>Paper-cut Lightbox</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-paper-lantern/STYLE.md">规则</a> · <a href="styles/opuscar-paper-lantern/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-papercut-red/STYLE.md"><img src="styles/opuscar-papercut-red/preview.jpg" alt="红色窗花剪纸" width="300"></a><br><b>红色窗花剪纸</b><br><sub>Red Paper-cut</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-papercut-red/STYLE.md">规则</a> · <a href="styles/opuscar-papercut-red/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-shadow-puppet/STYLE.md"><img src="styles/opuscar-shadow-puppet/preview.jpg" alt="皮影戏" width="300"></a><br><b>皮影戏</b><br><sub>Shadow Puppetry</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-shadow-puppet/STYLE.md">规则</a> · <a href="styles/opuscar-shadow-puppet/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-ukiyoe/STYLE.md"><img src="styles/opuscar-ukiyoe/preview.jpg" alt="浮世绘" width="300"></a><br><b>浮世绘</b><br><sub>Ukiyo-e</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-ukiyoe/STYLE.md">规则</a> · <a href="styles/opuscar-ukiyoe/sample.mp4">样片</a></td>
</tr>
</table>

### 印刷与版画 · 5 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-engraving/STYLE.md"><img src="styles/opuscar-engraving/preview.jpg" alt="铜版画" width="300"></a><br><b>铜版画</b><br><sub>Copperplate Engraving</sub><br><sub>资讯呈现／故事视频／品牌形象短片</sub><br><a href="styles/opuscar-engraving/STYLE.md">规则</a> · <a href="styles/opuscar-engraving/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-halftone-dossier/STYLE.md"><img src="styles/opuscar-halftone-dossier/preview.jpg" alt="复古半调案卷" width="300"></a><br><b>复古半调案卷</b><br><sub>Halftone Dossier</sub><br><sub>资讯呈现／故事视频／品牌形象短片</sub><br><a href="styles/opuscar-halftone-dossier/STYLE.md">规则</a> · <a href="styles/opuscar-halftone-dossier/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-risograph/STYLE.md"><img src="styles/opuscar-risograph/preview.jpg" alt="Risograph 孔版印刷" width="300"></a><br><b>Risograph 孔版印刷</b><br><sub>Risograph Print</sub><br><sub>资讯呈现／故事视频／品牌形象短片</sub><br><a href="styles/opuscar-risograph/STYLE.md">规则</a> · <a href="styles/opuscar-risograph/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-silkscreen-poster/STYLE.md"><img src="styles/opuscar-silkscreen-poster/preview.jpg" alt="丝印旅行海报" width="300"></a><br><b>丝印旅行海报</b><br><sub>Silkscreen Travel Poster</sub><br><sub>资讯呈现／故事视频／品牌形象短片</sub><br><a href="styles/opuscar-silkscreen-poster/STYLE.md">规则</a> · <a href="styles/opuscar-silkscreen-poster/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-woodcut/STYLE.md"><img src="styles/opuscar-woodcut/preview.jpg" alt="木刻版画" width="300"></a><br><b>木刻版画</b><br><sub>Woodcut Print</sub><br><sub>资讯呈现／故事视频／品牌形象短片</sub><br><a href="styles/opuscar-woodcut/STYLE.md">规则</a> · <a href="styles/opuscar-woodcut/sample.mp4">样片</a></td>
</tr>
</table>

### 图形与排版 · 7 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-art-deco/STYLE.md"><img src="styles/opuscar-art-deco/preview.jpg" alt="装饰艺术" width="300"></a><br><b>装饰艺术</b><br><sub>Art Deco</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-art-deco/STYLE.md">规则</a> · <a href="styles/opuscar-art-deco/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-ascii-crt/STYLE.md"><img src="styles/opuscar-ascii-crt/preview.jpg" alt="ASCII / CRT 终端" width="300"></a><br><b>ASCII / CRT 终端</b><br><sub>ASCII / CRT Terminal</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-ascii-crt/STYLE.md">规则</a> · <a href="styles/opuscar-ascii-crt/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-blueprint/STYLE.md"><img src="styles/opuscar-blueprint/preview.jpg" alt="蓝图 / 工程制图" width="300"></a><br><b>蓝图 / 工程制图</b><br><sub>Blueprint</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-blueprint/STYLE.md">规则</a> · <a href="styles/opuscar-blueprint/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-pictogram-motion/STYLE.md"><img src="styles/opuscar-pictogram-motion/preview.jpg" alt="象形运动图形" width="300"></a><br><b>象形运动图形</b><br><sub>Pictogram Motion</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-pictogram-motion/STYLE.md">规则</a> · <a href="styles/opuscar-pictogram-motion/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-spy-titles/STYLE.md"><img src="styles/opuscar-spy-titles/preview.jpg" alt="60s 间谍片头" width="300"></a><br><b>60s 间谍片头</b><br><sub>60s Spy Title Sequence</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-spy-titles/STYLE.md">规则</a> · <a href="styles/opuscar-spy-titles/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-stained-glass/STYLE.md"><img src="styles/opuscar-stained-glass/preview.jpg" alt="彩色玻璃窗" width="300"></a><br><b>彩色玻璃窗</b><br><sub>Stained Glass</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-stained-glass/STYLE.md">规则</a> · <a href="styles/opuscar-stained-glass/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-swiss-motion/STYLE.md"><img src="styles/opuscar-swiss-motion/preview.jpg" alt="瑞士动态排版" width="300"></a><br><b>瑞士动态排版</b><br><sub>Swiss Motion Graphics</sub><br><sub>知识讲解／功能动效／品牌形象短片</sub><br><a href="styles/opuscar-swiss-motion/STYLE.md">规则</a> · <a href="styles/opuscar-swiss-motion/sample.mp4">样片</a></td>
</tr>
</table>

### 信息与发布 · 5 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-dark-keynote/STYLE.md"><img src="styles/opuscar-dark-keynote/preview.jpg" alt="暗色科技发布" width="300"></a><br><b>暗色科技发布</b><br><sub>Dark Tech Keynote</sub><br><sub>产品演示／知识讲解／资讯呈现</sub><br><a href="styles/opuscar-dark-keynote/STYLE.md">规则</a> · <a href="styles/opuscar-dark-keynote/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-dataviz/STYLE.md"><img src="styles/opuscar-dataviz/preview.jpg" alt="数据叙事" width="300"></a><br><b>数据叙事</b><br><sub>Data Storytelling</sub><br><sub>产品演示／知识讲解／资讯呈现</sub><br><a href="styles/opuscar-dataviz/STYLE.md">规则</a> · <a href="styles/opuscar-dataviz/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-hologram-hud/STYLE.md"><img src="styles/opuscar-hologram-hud/preview.jpg" alt="科幻全息界面" width="300"></a><br><b>科幻全息界面</b><br><sub>Sci-fi Hologram HUD</sub><br><sub>产品演示／知识讲解／资讯呈现</sub><br><a href="styles/opuscar-hologram-hud/STYLE.md">规则</a> · <a href="styles/opuscar-hologram-hud/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-iso-infographic/STYLE.md"><img src="styles/opuscar-iso-infographic/preview.jpg" alt="等距信息图" width="300"></a><br><b>等距信息图</b><br><sub>Isometric Infographic</sub><br><sub>产品演示／知识讲解／资讯呈现</sub><br><a href="styles/opuscar-iso-infographic/STYLE.md">规则</a> · <a href="styles/opuscar-iso-infographic/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-living-screencast/STYLE.md"><img src="styles/opuscar-living-screencast/preview.jpg" alt="活体实机录屏" width="300"></a><br><b>活体实机录屏</b><br><sub>Living Screencast</sub><br><sub>产品演示／知识讲解／资讯呈现</sub><br><a href="styles/opuscar-living-screencast/STYLE.md">规则</a> · <a href="styles/opuscar-living-screencast/sample.mp4">样片</a></td>
</tr>
</table>

### 卡通与动画 · 4 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-cel-anime-80s/STYLE.md"><img src="styles/opuscar-cel-anime-80s/preview.jpg" alt="80 年代赛璐璐动画" width="300"></a><br><b>80 年代赛璐璐动画</b><br><sub>80s Cel Anime</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-cel-anime-80s/STYLE.md">规则</a> · <a href="styles/opuscar-cel-anime-80s/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-midcentury-toon/STYLE.md"><img src="styles/opuscar-midcentury-toon/preview.jpg" alt="50s 扁平卡通" width="300"></a><br><b>50s 扁平卡通</b><br><sub>Mid-century Cartoon</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-midcentury-toon/STYLE.md">规则</a> · <a href="styles/opuscar-midcentury-toon/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-rubber-hose/STYLE.md"><img src="styles/opuscar-rubber-hose/preview.jpg" alt="1930s 橡皮管卡通" width="300"></a><br><b>1930s 橡皮管卡通</b><br><sub>1930s Rubber Hose Cartoon</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-rubber-hose/STYLE.md">规则</a> · <a href="styles/opuscar-rubber-hose/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-scifi-toon/STYLE.md"><img src="styles/opuscar-scifi-toon/preview.jpg" alt="科幻情景喜剧卡通" width="300"></a><br><b>科幻情景喜剧卡通</b><br><sub>Sci-Fi Sitcom Toon</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-scifi-toon/STYLE.md">规则</a> · <a href="styles/opuscar-scifi-toon/sample.mp4">样片</a></td>
</tr>
</table>

### 游戏 · 4 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-game-show/STYLE.md"><img src="styles/opuscar-game-show/preview.jpg" alt="综艺节奏扁平" width="300"></a><br><b>综艺节奏扁平</b><br><sub>Game Show Flat</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-game-show/STYLE.md">规则</a> · <a href="styles/opuscar-game-show/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-hd-2d/STYLE.md"><img src="styles/opuscar-hd-2d/preview.jpg" alt="HD-2D" width="300"></a><br><b>HD-2D</b><br><sub>HD-2D</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-hd-2d/STYLE.md">规则</a> · <a href="styles/opuscar-hd-2d/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-microgame/STYLE.md"><img src="styles/opuscar-microgame/preview.jpg" alt="微游戏快闪" width="300"></a><br><b>微游戏快闪</b><br><sub>Microgame Frenzy</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-microgame/STYLE.md">规则</a> · <a href="styles/opuscar-microgame/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-pixel-rpg/STYLE.md"><img src="styles/opuscar-pixel-rpg/preview.jpg" alt="16-bit 像素 RPG" width="300"></a><br><b>16-bit 像素 RPG</b><br><sub>16-bit Pixel RPG</sub><br><sub>故事视频／知识讲解／音乐与视觉表演</sub><br><a href="styles/opuscar-pixel-rpg/STYLE.md">规则</a> · <a href="styles/opuscar-pixel-rpg/sample.mp4">样片</a></td>
</tr>
</table>

### 电影与时代 · 2 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-backrooms/STYLE.md"><img src="styles/opuscar-backrooms/preview.jpg" alt="后室 / 新怪谈" width="300"></a><br><b>后室 / 新怪谈</b><br><sub>Liminal Found Footage</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-backrooms/STYLE.md">规则</a> · <a href="styles/opuscar-backrooms/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-silent-film/STYLE.md"><img src="styles/opuscar-silent-film/preview.jpg" alt="1920s 默片" width="300"></a><br><b>1920s 默片</b><br><sub>1920s Silent Film</sub><br><sub>故事视频／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-silent-film/STYLE.md">规则</a> · <a href="styles/opuscar-silent-film/sample.mp4">样片</a></td>
</tr>
</table>

### 材质与 3D · 5 套

<table>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-brick-toy/STYLE.md"><img src="styles/opuscar-brick-toy/preview.jpg" alt="积木玩具" width="300"></a><br><b>积木玩具</b><br><sub>Brick Toy</sub><br><sub>产品演示／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-brick-toy/STYLE.md">规则</a> · <a href="styles/opuscar-brick-toy/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-glass-product/STYLE.md"><img src="styles/opuscar-glass-product/preview.jpg" alt="玻璃质感产品" width="300"></a><br><b>玻璃质感产品</b><br><sub>Glass Product Render</sub><br><sub>产品演示／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-glass-product/STYLE.md">规则</a> · <a href="styles/opuscar-glass-product/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-lowpoly-island/STYLE.md"><img src="styles/opuscar-lowpoly-island/preview.jpg" alt="低多边形等距" width="300"></a><br><b>低多边形等距</b><br><sub>Low-poly Isometric Island</sub><br><sub>产品演示／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-lowpoly-island/STYLE.md">规则</a> · <a href="styles/opuscar-lowpoly-island/sample.mp4">样片</a></td>
</tr>
<tr>
<td width="33%" valign="top"><a href="styles/opuscar-paper-popup/STYLE.md"><img src="styles/opuscar-paper-popup/preview.jpg" alt="纸片立体书" width="300"></a><br><b>纸片立体书</b><br><sub>Paper Pop-up Book</sub><br><sub>产品演示／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-paper-popup/STYLE.md">规则</a> · <a href="styles/opuscar-paper-popup/sample.mp4">样片</a></td>
<td width="33%" valign="top"><a href="styles/opuscar-tilt-shift/STYLE.md"><img src="styles/opuscar-tilt-shift/preview.jpg" alt="移轴微缩" width="300"></a><br><b>移轴微缩</b><br><sub>Tilt-Shift Miniature</sub><br><sub>产品演示／品牌形象短片／音乐与视觉表演</sub><br><a href="styles/opuscar-tilt-shift/STYLE.md">规则</a> · <a href="styles/opuscar-tilt-shift/sample.mp4">样片</a></td>
</tr>
</table>

## 怎样把这些能力组合起来

场景决定要完成的任务，风格决定材质与视觉语言，配方安排整片内容，表达和动效处理局部。它们可以按当前主题重新组合。

| 想做的作品 | 可以怎样开始 |
| --- | --- |
| 产品发布片 | 产品任务证明 + 清晰产品或玻璃产品风格 + 操作重点标注 + 结果揭示 |
| 概念知识科普 | 逐层递进 + 单色图解或等距信息图 + 旁白或音乐编排 |
| 嘻哈知识科普 | 事实与歌词 + 像素或综艺节奏风格 + 逐句字幕与真实音轨 |
| 资讯短片 | 证据板 + 字幕新闻或新闻包装 + 原始资料与数据 |
| 图片与品牌短片 | 真实图片到主画面 + 影像叙事或鲜明拼贴 + 音乐动机与转场 |

### 18 类组合配方

配方是本库依据创作研究与实践形成的编排，包含输入、镜头步骤、表达组合、检查问题和调整方法。

| 配方 | 怎样组织内容 |
| --- | --- |
| [同一对象的界面旅程](catalog/recipes.json) | 让同一界面对象经过多个状态，保持空间与动作连续。 |
| [跟随信号讲清系统](catalog/recipes.json) | 跟随信号或信息单元，解释系统中的路径和变化。 |
| [从整体进入微观](catalog/recipes.json) | 从整体进入局部与微观，逐层建立尺度参照。 |
| [真实图片到主画面](catalog/recipes.json) | 保留真实图片的主体，用裁切、排版和镜头突出重点。 |
| [音乐事件成为可见动作](catalog/recipes.json) | 把音乐中的事件变成可见的动作与变化。 |
| [文字承担叙事动作](catalog/recipes.json) | 让文字的出现、位置和运动承担叙事。 |
| [数据与比较讲清差异](catalog/recipes.json) | 建立共同基准，再呈现数值、关系与差异。 |
| [有表达目标的品牌形象片](catalog/recipes.json) | 围绕品牌主张，用一个视觉母题反复推进。 |
| [用真实任务证明产品价值](catalog/recipes.json) | 从用户任务进入实际操作，以可见结果收束。 |
| [同片段逐层增加能力](catalog/recipes.json) | 在同一片段上逐层呈现变化，让差异可比较。 |
| [物即解释讲清机制](catalog/recipes.json) | 让物体的结构、位置和运转过程承担解释。 |
| [逐层递进讲清抽象概念](catalog/recipes.json) | 先建立载体和关系，再逐层加入新信息。 |
| [证据板讲清资讯](catalog/recipes.json) | 将资料、事实和对照组织成清晰的资讯线索。 |
| [发布片情绪弧](catalog/recipes.json) | 围绕问题、转折、证明和行动安排发布片节奏。 |
| [功能章节串联](catalog/recipes.json) | 用连续章节呈现一组相关功能。 |
| [产品音乐叙事](catalog/recipes.json) | 把产品动作、歌词、音乐段落与画面变化一起编排。 |
| [概念知识科普](catalog/recipes.json) | 按所选音乐组织知识层次、关键词、字幕与揭示落点。 |
| [嘻哈知识科普](catalog/recipes.json) | 让核对后的知识进入可唱歌词，再按真实音轨编排声画。 |

### 64 项表达指导

表达条目由本库归纳与适配，用来说明局部手法的目的、输入、参数与检查方式。完整说明可在 [表达目录](assets/gallery/expressions.html) 中查看。

| 类别 | 已收录的表达 |
| --- | --- |
| 叙事 · 9 项 | 目标到证据、跟随一个信息单元、连续尺度解释、视觉能量起落、同一主体贯穿变化、痛点证据到判决阶梯、成品即证据，节选标明、平行承诺章节、行动即调用 |
| 镜头 · 4 项 | 推近与退回语境、路线导览镜头、运动补偿构图、拉远揭示与点击穿越 |
| 转场 · 6 项 | 共享形体过渡、构图匹配切换、遮挡后揭示、对象突破画框、沿切线连续离轨、动作因果接缝 |
| 视觉 · 9 项 | 动作与计量联动、媒体空间阵列、结构分解与装回、受控粒子场、连续材质变化、目标框与语义标注、有边界的处理与结果揭示、量级鞭甩与逐位计数、可识别外壳的复刻界面 |
| 动画 · 4 项 | 有目标的弹性落定、前后沿差动伸缩、沿路径生长与流过、填充与转移 |
| 文字 · 6 项 | 随语义变化的文字重点、沿曲线排字、字向补偿、先读后运动、打字叙述者、判决牌与三种声线 |
| 声音 · 5 项 | 音乐拍点映射、可见事件触发声音、按频段响应画面、把注意留给主要声音、转折落拍与接缝浅谷 |
| 交互 · 2 项 | 可见直接操控、把交互体验变成导览片 |
| 风格统一 · 2 项 | 统一视觉与运动气质、双底色世界 |
| 制作组织 · 6 项 | 可定位的统一时间、首尾连续循环、先锁关系与节奏再换肤、能力探测与可信回退、内钟压缩、停留预算 |
| 知识表达 · 11 项 | 物即解释、逐层递进、层间桥接、部件登场四问、一次完整运行、反事实探针、落地标签、真值账本、受控表达、证据板、模型边界与延伸指路 |

### 12 项基础动效

出现 · 离场 · 强调 · 路径描绘 · 建立关系 · 数值变化 · 状态替换 · 镜头聚焦 · 遮罩切换 · 逐项呈现 · 层间视差 · 稳定停留

配方、表达和动效提供设计与实现指导，实际画面由当前工程与可用工具完成；它们可以从 [目录](catalog/) 查询和继续扩展。

## 本库增加的工程与使用能力

| 能力 | 怎样使用 |
| --- | --- |
| 精确选择风格 | 用规范 ID、中文名或英文名查询，先看规则再进入制作 |
| 新增与派生风格 | 新建独立包，继承一个基底，按需要声明局部借用 |
| 项目与个人集合 | 将自己的变体放在外置集合，内置目录生成时排除这些内容 |
| 可视化选择 | 在画廊搜索、筛选、并排对比，复制风格 ID 或创作指令 |
| 样片离线播放 | 代表帧与 59 条样片随仓库分发，保持目录即可本地浏览 |
| 自动生成目录 | 风格元数据生成索引和画廊，新增包后统一更新 |
| 文件与依赖检查 | 检测命名冲突、缺失引用、循环依赖、文件变化和计划锁 |
| 媒体与交付检查 | 探测实际视频与音频，核对排程、字幕、声音事件和交付文件 |

```sh
python3 scripts/stylepacks.py resolve 中国水墨
python3 scripts/stylepacks.py init brand-ink --into /project/video/styles --extends opuscar-ink-wash
python3 scripts/stylepacks.py validate --style-root /project/video/styles
```

扩展规范见 [维护说明](MAINTAINING.md) 和 [风格包合同](references/style-pack-contract.md)。导演与技术分层、风格规则与案例分开维护等工程方法参考了 Lemo-Opuscar，本库保留自己的交付方式、合同与工具接口。

## 方法借鉴与社区支持

除完整集成的 Lemo-Opuscar 风格外，本库还从以下项目与作品研究中吸收方法，并形成自己的编排和检查规则。

| 参考项目 | 在本库中的借鉴 |
| --- | --- |
| [huashu-design](https://github.com/alchaincyf/huashu-design) | 方向、分镜、关键帧与声音审查 |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 内容槽位、风格和布局组织 |
| [OpenDesign](https://github.com/nexu-io/open-design) | 观众所得、焦点、变换与停留 |
| [guizang-social-card-skill](https://github.com/op7418/guizang-social-card-skill) | 内容与证据如何进入画面、首帧与短动态 |
| [guizang-product-video-skill](https://github.com/op7418/guizang-product-video-skill) | 产品任务、真实组件与旁白量时 |
| [HyperFrames launches](https://github.com/heygen-com/hyperframes-launches) | 产品任务证明、发布片组织与声画编排 |
| [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | 表达母题、提示描述与作品关系的研究线索 |

这些项目提供方法启发；本库对应的归纳、合同和适配关系记在 [来源说明](references/sources.md) 与条目的来源字段中。感谢创作者开放分享。

## 安装

将仓库克隆到你的 Agent 能加载的 Skill 目录。以 Codex 为例，目标目录不存在时执行下面的命令。

```sh
git clone https://github.com/mileson/chaojifeng-video-design.git ~/.codex/skills/chaojifeng-video-design
```

已有同名 Skill 时，先检查自己的改动与私人素材，避免覆盖。其他支持 `SKILL.md` 的 Agent 可将完整目录放到对应的 Skill 路径，保留相对目录结构。

## 开始使用

在 Agent 中调用 `$chaojifeng-video-design` 并描述目标，例如下面几种任务。

最短可以这样写：

> 用 $chaojifeng-video-design 做一期关于【主题】的概念知识科普视频，一次性完成。

也可以指定音乐：

> 用 $chaojifeng-video-design，以我提供的【音乐文件】制作【主题】的概念知识科普视频，按这首曲子的结构编排，直接完成成片。

> 为这个产品制作一条 30 秒竖版介绍视频。使用项目中已有的截图和素材，先确认要证明的任务，再完成镜头、声音、成片和必要编辑源。

> 把这组图片组织成一条 20 秒视频，保留主体，安排画面重点与转场。音乐使用我提供的获准音轨。

> 只修改第 3 个镜头，让操作结果更容易看清，并复验相关字幕和声音落点。

> 我只需要分镜方案。请先核实 TCP 三次握手的事实，再用逐层递进的画面解释。

Agent 会根据已有项目和工具选择实现方式。此仓库包含创作方法、合同、示例和检查脚本；生成、渲染、配音与导出需要宿主提供相应能力。它不附带通用视频渲染器，也不要求固定模型或引擎。

明确要求“一次性完成、直接成片、无需试片”时，Agent 连续完成制作、内部检查和必要返修；要求分阶段审阅时，才在约定节点等待。只要方案、分镜或局部修改，也可以直接说明范围。

## 浏览和检查

在仓库根目录执行。查询与合同检查脚本使用 Python 3.10 或更新版本及标准库；媒体探测和部分测试还需要现有的 FFmpeg、ffprobe。无需安装 Python 第三方包。

```sh
python3 scripts/catalog.py --kind scenario list
python3 scripts/catalog.py --kind recipe get product-task-proof
python3 scripts/catalog.py --kind expression get visual.target-callout
python3 scripts/validate_plan.py examples/product-demo.plan.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

打开 [风格画廊](assets/gallery/index.html)，用代表画面浏览全部 66 种风格，可搜索、按分类或视频任务筛选、并排对比，并复制当前风格的创作指令。59 张代表帧已嵌入 HTML，59 条样片随仓库一起分发，下载完整仓库后可直接离线播放；基础风格按实际参数呈现。需要动作与配方时进入 [表达目录](assets/gallery/expressions.html)。也可以直接阅读 [Skill 入口](SKILL.md)、[计划合同](references/plan-contract.md) 和 [执行与交付](references/runtime-and-delivery.md)。图册与计划示例用于理解和检查结构，实际作品仍需渲染、观看与试听。

## 音乐和声音

“概念知识科普”配方支持**一个音乐池、多首候选、一首默认**。选择顺序为：用户明确指定 → 项目已选 → 配方当前默认。新增候选与更换默认分别处理；单次指定只影响当前作品。换曲后重新分析实际乐段、拍点和映射，不沿用旧曲的节奏结论。

当前 [音乐目录](catalog/music.json) 保留“知识分享背景音乐神曲”的元信息，作为该配方的初始默认引用；仓库不附带音源。使用默认曲目前，需将获准的同一文件关联到本机位置表，脚本会核对哈希和实际时长。也可以直接指定自己的音乐文件，无需先修改音乐池：

```sh
python3 scripts/music_library.py search --recipe knowledge-music-explainer --limit 5
python3 scripts/music_library.py select --recipe knowledge-music-explainer --source-file /project/music/chosen.wav
```

其他配方按各自配置与任务选曲。按 [音乐导演说明](references/music-direction.md) 添加自己获准使用的曲目与片段，记录实际文件哈希、时长、来源和使用范围。音源位置通过项目内的 `*.local.json` 或 `CJF_VIDEO_MUSIC_REGISTRY` 关联，不提交到仓库。

```sh
python3 scripts/music_library.py validate-catalog
python3 scripts/music_library.py search --scenario product-demo --emotion curious --role establish --limit 5
python3 scripts/build_music_atlas.py
```

添加曲目后重新生成图册；仅导入音源位置表不会新增曲目。默认音源缺失或哈希变化时，选择工具返回具体缺口，不静默换曲。

[概念知识科普编排](references/knowledge-music-direction.md) 说明音乐地图、字幕与旁白分支、阅读窗和声音提示；可选的 [声画任务表](templates/knowledge-music-score.json) 通过 `explainer_timing_audit.py` 检查已声明的阅读窗与时间映射。结构检查不代替测拍、连续观看或听审。

旁白参考由使用者自行提供，按 [讲解与声音参考](references/explainer-narration.md) 检查授权、降噪派生、准确读稿和实际听感。仓库附带上述 59 条风格样片；私人声音、单独的付费歌曲和模型权重由使用者自行准备。

## 目录

| 位置 | 内容 |
| --- | --- |
| `SKILL.md` | 轻量入口与任务路由 |
| `DIRECTOR.md` / `TECHNIQUE.md` | 导演方法与制作能力适配 |
| `MAINTAINING.md` | 扩展、导入、生成与回归 |
| `styles/` | 独立风格包、完整风格规则与案例源码 |
| `vendor/lemo-opuscar/` | 锁定的共享文本源码、许可证与哈希清单 |
| `references/` | 导演、知识表达、镜头、声音与验收方法 |
| `catalog/` | 场景、风格、动效、表达与配方目录 |
| `templates/` | 计划、交付记录、声音事件表与其他模板 |
| `examples/` | 计划、知识包结构示例与成片案例 |
| `scripts/` | 查询、校验、探测、图册构建和离线测试 |
| `assets/` | 可视化风格画廊、动效配方目录和音乐图册 |
| `evals/` | 尚未执行的创作评测题目 |

检查通过只说明对应结构或测量条件成立。画面、听感、事实与观众理解需要分别验收，未做的检查保留未验证状态。

## 许可与来源

本库原创代码、文档、模板和画廊程序采用 [MIT License](LICENSE)。集成的 Lemo-Opuscar 代码和文档保留其 MIT 许可；59 条样片与代表帧采用其 CC BY 4.0 许可，具体素材署名和三条无声样片的变更见 [第三方说明](THIRD_PARTY_NOTICES.md)。

两部创作案例的使用范围见 [案例说明](examples/showcase/README.md#使用范围)。其他字体、音乐、模型和素材按各自条件使用。
