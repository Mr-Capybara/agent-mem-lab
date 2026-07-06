# Project Initialization

更新日期：2026-07-06

本文件记录为了让整个研究和工程由 Codex 持续推进，需要补齐的初始化配置。

## 1. 当前已完成

- 已确定主线：`smolagents + Mem0`。
- 已建立精简计划文件：`agent_memory_project_plan.md`。
- 已建立状态文件：`PROJECT_STATUS.md`。
- 已建立规则文件：`PROJECT_RULES.md`。
- 已建立 Codex 接手入口：`AGENTS.md`。

## 2. 用户审核后再做

用户审核通过后执行：

1. 初始化 git 仓库。
2. 创建 `.gitignore`。
3. 创建 `.env.example`。
4. 创建 `pyproject.toml`。
5. 创建 `README.md`。
6. 创建 `configs/`。
7. 创建源码目录 `agent_lab/`。
8. 创建评测目录 `eval/`。
9. 创建 `tests/` 和 `traces/`。

## 3. 建议的基础文件

### `.gitignore`

应忽略：

- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`
- `.env`
- `traces/`
- `eval/reports/`
- `data/raw/`
- `data/cache/`
- 大模型、本地向量库、临时 benchmark 下载数据

### `.env.example`

建议包含：

```text
OPENAI_API_KEY=
OPENAI_BASE_URL=
LOCAL_MODEL_NAME=
LOCAL_VISION_MODEL_NAME=
MEM0_LLM_PROVIDER=
MEM0_EMBEDDER_PROVIDER=
MEM0_VECTOR_STORE_PROVIDER=
AGENT_TRACE_DIR=traces
```

### `pyproject.toml`

建议包含：

- Python 版本：`>=3.11`
- 运行依赖：`smolagents`、`mem0ai`、`pydantic`、`pyyaml`、`rich`
- 评测依赖：`pytest`、`pytest-cov`
- 代码质量：`ruff`
- 可选多模态依赖：`pillow`、`pytesseract` 或后续替代工具

### `configs/`

建议初始化：

```text
configs/
  agent.yaml
  memory.yaml
  eval.yaml
  model.local.yaml.example
```

配置职责：

- `agent.yaml`：agent 类型、工具开关、最大步数、trace 开关。
- `memory.yaml`：backend 类型、top-k、写入策略、命名空间。
- `eval.yaml`：数据集路径、backend 列表、输出路径。
- `model.local.yaml.example`：本地模型 endpoint 示例。

## 4. 建议的源码骨架

```text
agent_lab/
  __init__.py
  agent_runner.py
  trace.py
  prompts.py
  tools/
    __init__.py
    calculator.py
    files.py
    shell.py
    vision.py
  memory/
    __init__.py
    base.py
    no_memory.py
    raw_history.py
    mem0_backend.py
```

```text
eval/
  runner.py
  metrics.py
  datasets/
    custom_memory_cases.jsonl
  adapters/
    longmemeval.py
    locomo.py
  reports/
```

## 5. 初始化验收标准

P0 完成后应满足：

- 新会话 Codex 只读 `AGENTS.md` 就知道入口。
- `PROJECT_STATUS.md` 能说明当前进度。
- `PROJECT_RULES.md` 能约束后续实现。
- `agent_memory_project_plan.md` 不再冗余。
- 用户可以在审核后初始化 git。

P1 开始前应满足：

- Python 项目骨架存在。
- 依赖和配置文件有明确位置。
- trace 输出目录有规范。
- memory backend 接口设计可以落地。
