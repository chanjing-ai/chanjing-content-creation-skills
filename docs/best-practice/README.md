# 文档中心（chan-skills）

本目录是**面向使用者**的速用说明与最佳实践摘录，**不替代**技能包内的执行真源。实现细节、参数与 CLI 以各手册 `*_SKILL.md` 与 `scripts/` 为准。

---

## 文档与代码的对应关系

| 读者 | 建议阅读 |
|------|----------|
| 想在对话里一句话说清需求 | 下文「四条原则」「通用模板」+ 各产品 [`*-best-practice.md`](./) |
| 要查目录结构、模块职责、该跑哪个脚本 | 仓库 [`develop/architecture.md`](../develop/architecture.md)、[`develop/features-guide.md`](../develop/features-guide.md) |
| Agent / 集成方 | 包入口 [`skills/chanjing-content-creation-skill/SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md)（路由 + **运行时契约**），再打开命中的 **`{名}_SKILL.md`** |

**技能包物理路径（本仓库内嵌）：**

```text
skills/chanjing-content-creation-skill/
├── SKILL.md                 # 全局入口：路由、环境变量、凭据、ffmpeg、落盘等
├── common/                  # L1 公共基础
├── products/<product>/      # L2：各产品 <product>_SKILL.md + scripts/
└── orchestration/           # L3：编排场景 + CONTRACT_SKILL.md
```

一键成片等本地拼接依赖 **ffmpeg / ffprobe**；凭据默认 **`~/.chanjing/credentials.json`**（可用 **`CHANJING_CONFIG_DIR`** 覆盖）。详见包根 `SKILL.md`「运行时契约」。

---

## 先记住 4 条

1. 先说你要做什么，不要只说「帮我生成一个」。
2. 说清用途和人群，不要只说「高级一点」「好看一点」。
3. 说清你最在意什么，比如真实感、转化感、品牌统一。
4. 先要 1 个版本确认，再批量做。

---

## 通用模板

> 我想做【内容类型】，用于【业务场景】，给【目标人群】看。  
> 我最在意【真实感 / 转化感 / 品牌统一 / 创意感】。  
> 风格希望是【风格描述】。  
> 请先给我【1个版本 / 3个方向】。

---

## 跟 OpenClaw / Agent 这样说，更容易触发 skill

1. 不确定用哪个能力时，先看 **[`SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md)**（仅全局路由）；命中后打开对应 **`{产品或场景}_SKILL.md`**，由其调度 **`scripts/`**。编排约定与状态码见 **[`orchestration/CONTRACT_SKILL.md`](../skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md)**。
2. 直接说条件和目标。
3. 尽量带上能力关键词，例如：口播、数字人、复刻声音、文本驱动唇形、语音驱动唇形、对口型、修改口型、视频翻译、海报、**一键成片**、**workflow**。
4. 若已知道能力，可直接点名：「请用蝉镜数字人技能」「请用 chanjing-tts」「请用对口型 skill」「请用一键成片编排」等。
5. 先说「先出 1 个版本」，比一上来「批量做 50 个」更容易执行对。

---

## 能力速查（意图 → 产品/场景）

| 你想做的事 | 技能包内目录（L2 / L3） | 人类速用文档 |
|------------|-------------------------|--------------|
| 先把蝉镜账号、AK/SK 搞定 | `products/chanjing-credentials-guard` | [凭据守卫速用](./chanjing-credentials-guard-best-practice.md) |
| 文字变声音（不要求像某人） | `products/chanjing-tts` | [TTS 速用](./chanjing-tts-best-practice.md) |
| 声音像某个人、长期复用 | `products/chanjing-tts-voice-clone` | [声音复刻速用](./chanjing-tts-voice-clone-best-practice.md) |
| 文本/语音驱动唇形、对口型、视频翻译（有现成视频素材） | `products/chanjing-avatar` | [Avatar 速用](./chanjing-avatar-best-practice.md) |
| 标准数字人口播（公共/固定形象） | `products/chanjing-video-compose` | [数字人合成速用](./chanjing-video-compose-best-practice.md) |
| 训练可长期复用的定制数字人 | `products/chanjing-customised-person` | [定制数字人速用](./chanjing-customised-person-best-practice.md) |
| 没人设素材，先文生形象再考虑视频 | `products/chanjing-text-to-digital-person` | [文生数字人速用](./chanjing-text-to-digital-person-best-practice.md) |
| 海报、创意图、创意视频（通用创作任务） | `products/chanjing-ai-creation` | [AI 创作速用](./chanjing-ai-creation-best-practice.md) |
| 选题或完整分镜工作流 → 口播 + 数字人 + AI 画面 + 本地 mp4 | `orchestration/chanjing-one-click-video-creation` | [一键成片速用](./chanjing-one-click-video-creation-best-practice.md) |

---

## 最佳实践短文目录

- [`chanjing-credentials-guard-best-practice.md`](./chanjing-credentials-guard-best-practice.md)
- [`chanjing-tts-best-practice.md`](./chanjing-tts-best-practice.md)
- [`chanjing-tts-voice-clone-best-practice.md`](./chanjing-tts-voice-clone-best-practice.md)
- [`chanjing-avatar-best-practice.md`](./chanjing-avatar-best-practice.md)
- [`chanjing-video-compose-best-practice.md`](./chanjing-video-compose-best-practice.md)
- [`chanjing-customised-person-best-practice.md`](./chanjing-customised-person-best-practice.md)
- [`chanjing-text-to-digital-person-best-practice.md`](./chanjing-text-to-digital-person-best-practice.md)
- [`chanjing-ai-creation-best-practice.md`](./chanjing-ai-creation-best-practice.md)
- [`chanjing-one-click-video-creation-best-practice.md`](./chanjing-one-click-video-creation-best-practice.md)

---

## 给 Agent 的真源链接（执行前必读）

| 用途 | 路径 |
|------|------|
| 包入口（路由 + 运行时契约） | [`skills/chanjing-content-creation-skill/SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md) |
| 跨场景契约 | [`skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md`](../skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md) |
| 编排总览 | [`skills/chanjing-content-creation-skill/orchestration/README.md`](../skills/chanjing-content-creation-skill/orchestration/README.md) |
| 一键成片手册 | [`skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md`](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation_SKILL.md) |
| workflow 字段契约 | [`skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/examples/workflow-contract.md`](../skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/examples/workflow-contract.md) |
| 各 L2 执行真值 | `skills/chanjing-content-creation-skill/products/<product>/<product>_SKILL.md` |
| 各产品能力目录入口 | `skills/chanjing-content-creation-skill/products/<product>/scripts/cli_capabilities.py` |
