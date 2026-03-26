# chan-skills 用户开发手册（引导）

本目录为**仓库级**开发说明，供贡献者与内部维护使用。  
**不属于**蝉镜技能包物理包体：`rule.md` 所指的「技能包根级四对象」位于 [`skills/chanjing-content-creation-skill/`](../skills/chanjing-content-creation-skill/) 内；`develop/` 不参与 Agent 技能安装路径。

---

## 文档地图

| 文档 | 内容 |
|------|------|
| [开发规范](./development-standards.md) | **必读**：目录规则、`rule.md` 对齐、代码与文档义务、红线 |
| [架构与目录](./architecture.md) | L1/L2/L3、`common` 模块、依赖方向、编排与脚本关系 |
| [功能引导](./features-guide.md) | 从入口到各产品/场景的能力索引与典型路径 |

---

## 仓库顶层目录结构（概览）

```
chan-skills/
├── develop/                    # 本开发手册（人类阅读）
├── docs/                       # 补充最佳实践等（非技能路由）
├── rule.md                     # 技能包目录与文档强制规则
├── README.md / README.zh-CN.md # 仓库说明与安装
├── skills/
│   └── chanjing-content-creation-skill/   # 蝉镜内容创作技能包（真值入口见下）
└── outputs/                    # 本地运行产物（通常不入库；见 .gitignore）
```

---

## 技能包内结构（功能载体）

核心开发工作集中在：

```
skills/chanjing-content-creation-skill/
├── SKILL.md                 # 唯一顶层路由 + 运行时契约
├── common/                  # L1 公共代码（鉴权、HTTP、上传/下载、域 API 等）
├── products/                # L2 按产品拆分的能力与 scripts/
└── orchestration/           # L3 跨产品编排 + CONTRACT_SKILL.md
```

**阅读顺序建议**

1. 根 [`SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md)：契约、环境变量、副作用类别。  
2. 目标能力：打开对应 **`{名}_SKILL.md`**（`products/` 或 `orchestration/` 下）。  
3. 实现与命令行：进入该目录的 `scripts/`，必要时读 `cli_capabilities.py` 与具体无后缀或 `.py` 脚本。

---

## 功能引导（一句话）

- **先配凭证**：`chanjing-credentials-guard`（AK/SK、`access_token`）。  
- **单点能力**：TTS、口型数字人、视频合成、定制数字人、文生数字人、通用 AI 创作等 → 各 **L2 `products/<名>/`**。  
- **组合成片**：一键短视频流水线 → **L3 `orchestration/chanjing-one-click-video-creation/`**（`run_render.py` 等）。

更细的表格、入口脚本与手册路径见 [功能引导](./features-guide.md)。

---

## 与 `rule.md` 的关系

- 技能包内改动须遵守仓库根目录 [`rule.md`](../rule.md)。  
- 若 `rule.md` 正文与当前 `common/` 实际文件列表不完全一致，以 **实现与包根 `SKILL.md` 描述为准**，并在 [开发规范](./development-standards.md) 中说明了推荐做法。
