# 开发规范

本文档为在 **chan-skills** 仓库内开发时的**强制与推荐约定**，与根目录 [`rule.md`](../rule.md) 一并遵守。

---

## 1. 技能包物理结构（不可破坏）

### 1.1 `skills/chanjing-content-creation-skill/` 根级四对象

仅允许存在（逻辑上）：

| 路径 | 层级 | 职责 |
|------|------|------|
| `SKILL.md` | 顶层 | 唯一路由入口 + **运行时契约** |
| `common/` | L1 | 跨产品复用的非领域业务基础设施 |
| `products/` | L2 | 单一产品能力，每目录一个产品 |
| `orchestration/` | L3 | 跨产品编排场景 |

**依赖方向（强制）**

- `common` **不得**依赖 `products` / `orchestration`。  
- `products` **不得**依赖 `orchestration`。  
- `orchestration` **可以**调用 `products` 下脚本或通过子进程/API 组合能力。

### 1.2 命名（与 `rule.md` 一致）

- 产品目录：**小写英文**（如 `chanjing-tts`）。  
- 编排场景目录：**小写 + 下划线**（如 `chanjing-one-click-video-creation`）。  
- 产品手册：`{产品目录名}_SKILL.md`。  
- 编排手册：`{场景目录名}_SKILL.md`。  
- 可执行代码：**一律**在对应目录的 `scripts/` 下（含 `cli_capabilities.py`）。

### 1.3 红线（摘自 `rule.md` §七，开发时自检）

- 禁止改动上述**三层目录名称**与既定结构语义。  
- 禁止在 **L1 `common/`** 编写**某一产品线专属**的业务规则或 CLI（领域常量、 argparse 组合应留在 L2/L3）。  
- 禁止在 **L2 `products/`** 内实现**跨产品编排主流程**（编排归 L3）。  
- 禁止在产品目录根散落可执行入口（须在 `scripts/`）。

---

## 2. `common/` 与 `rule.md` 的同步说明

`rule.md` §四曾约定 L1 仅 `base.py`、`exceptions.py`、`logger.py`，且其它能力可**合并进 `base.py`**。  
当前仓库为控制体积，已将部分能力拆出为独立模块（以包根 [`SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md) 描述为准），例如：

- `open_api_client.py`：带 `access_token` 的 JSON GET/POST  
- `file_upload.py`：上传与 `file_detail` 轮询  
- `asset_download.py`：结果 URL 下载  
- `open_ai_creation.py` / `open_aigc_person.py`：域 API 薄封装  

**规范**

- 新增「多产品复用」逻辑时：**优先**放入 `common/` 新模块或经评审后合并入 `base.py`；**禁止**在 `common` 写单产品 argparse 主流程。  
- 修改这些模块时：保持对现有 **L2/L3 脚本** 的 **CLI 行为兼容**（参数、退出码、stdout 格式），除非走明确版本迁移。

---

## 3. 脚本与 Python 约定

### 3.1 导入路径

- 各 `products/.../scripts/`、`orchestration/.../scripts/` 下脚本通过  
  `Path(__file__).resolve().parents[3] / "common"`  
  将 `common` 加入 `sys.path`（深度与「脚本位于 `.../chanjing-content-creation-skill/<layer>/<name>/scripts/`」一致）。  
- 凭证薄入口：同目录 `_auth.py` → `from base import resolve_chanjing_access_token` 等（与产品保持一致）。

### 3.2 可执行文件

- 许多 CLI **无 `.py` 后缀**，仍以 Python 执行；`common` 内保持 **`.py` 模块**，由脚本 import。  
- 新增脚本时：在目标 `scripts/` 下添加；更新对应 `cli_capabilities.py` 的 `operations` 列表（若适用）。

### 3.3 错误与异常

- Open API 封装层可使用 `common/exceptions.py` 中类型（如 `SkillHTTPError`）；CLI 层应对用户输出 **stderr + 非零退出码**，与现有脚本风格一致。

---

## 4. 文档与「运行时契约」义务（`rule.md` §五、§六）

凡脚本涉及：**外网 HTTPS**、**凭据读写**、**本地下载/落盘**、**子进程** 或 **浏览器引导**：

1. 变更实现后须同步更新包根 [`SKILL.md`](../skills/chanjing-content-creation-skill/SKILL.md) **「运行时契约」** 与 frontmatter **`description`**。  
2. 编排相关交叉引用须与 [`orchestration/CONTRACT_SKILL.md`](../skills/chanjing-content-creation-skill/orchestration/CONTRACT_SKILL.md)、场景 `README.md` 等保持一致。  
3. **禁止**在注册描述中写「无依赖」而代码实际读取环境变量或写盘。

---

## 5. `cli_capabilities.py` 与「重脚本」分离

- **`cli_capabilities.py`**：能力目录（`list` / `config` / `usage`）及可选 `run_skill_script` 薄封装；**保持短小**。  
- **重逻辑**（如 `run_render.py`）：独立脚本文件，**不要**与 `cli_capabilities.py` 合并，以免破坏全仓库统一模式与可测试性。

---

## 6. 变更检查清单（提交前）

- [ ] 未违反 L1/L2/L3 职责与依赖方向  
- [ ] 新/改脚本已考虑凭证、环境变量、输出路径；已更新根 `SKILL.md` 契约（如需要）  
- [ ] 产品手册或编排手册中与行为不一致的段落已修订  
- [ ] `cli_capabilities.py` 与真实脚本名一致  
- [ ] 未将密钥、真实 AK/SK 写入仓库

---

## 7. 仓库根目录与 `rule.md` §七

`rule.md` §七第 1 条禁止在「技能包根」随意增加根级对象；**本仓库**在 **monorepo 根**下允许存在 `develop/`、`docs/` 等**非技能包**目录，**不得**把这类目录塞进 `skills/chanjing-content-creation-skill/` 的包内四对象中。
