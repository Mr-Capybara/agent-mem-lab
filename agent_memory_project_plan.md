# Agent 记忆系统及自进化研究计划

更新日期：2026-07-06

## 1. 项目目标

本项目研究“agent 记忆系统及其自进化”。当前阶段只聚焦前三步：

1. 部署并跑通一个本地 agent，支持问答、简单任务执行、轻量多模态能力和自动化评测。
2. 接入一个可替换、可优化的记忆系统，作为后续实验对象。
3. 构造评测链路，验证“有记忆”相比“无记忆”的效果。

暂不追求成熟自进化算法，也不追求生产级复杂 agent。第一目标是搭建一个可重复、可解释、可扩展的实验台。

## 2. 已确定选型

```text
Agent 底座：smolagents
记忆系统起点：Mem0
实现语言：Python
工程方式：Codex 持续推进
核心要求：所有实验都可复现、可追踪、可替换 backend
```

选择理由：

- `smolagents` 轻量、可拆、工具接入直接，适合作为记忆系统实验底座。
- `Mem0` 接入成本低，有长期记忆定位和评测意识，适合作为第一版优化对象。
- 后续保留 `LangGraph + LangMem`、`Graphiti` 作为对照路线，但不作为第一阶段主线。

## 3. 能力边界

第一阶段 agent 应支持：

- 文本问答。
- 简单计算和代码任务。
- 受控文件读写。
- 受控 shell 或命令工具。
- 图片问答、截图理解、OCR/图表读数等轻量多模态能力。
- 简单网页浏览和信息抽取。
- 自动化评测调用。

第一阶段暂不追求：

- 完整桌面 GUI 自动操作。
- 长视频理解。
- 复杂音频编辑。
- 大规模多 agent 协作。
- 生产级权限、安全、部署系统。

## 4. 目标架构

```text
User / Eval Harness
        |
        v
Agent Runner
        |
        +-- Memory Adapter
        |       +-- NoMemoryBackend
        |       +-- RawHistoryBackend
        |       +-- Mem0Backend
        |       +-- Future: GraphitiBackend
        |
        +-- smolagents CodeAgent / ToolCallingAgent
        |       +-- controlled tools
        |
        +-- Trace Logger
                +-- task input
                +-- retrieved memories
                +-- memory context
                +-- tool calls
                +-- final answer
                +-- memory writes
                +-- metrics
```

关键原则：

- 长期记忆不直接绑定 `smolagents` 内部 memory，必须通过项目自定义 `MemoryBackend` 接口。
- 所有 backend 必须能跑同一套评测。
- 所有实验必须保存 trace。
- 不把业务逻辑写死到 Mem0 API 上。

## 5. 记忆类型

第一阶段至少区分以下记忆类型：

| 类型 | 含义 |
|---|---|
| `user_profile` | 用户稳定偏好，如语言、格式、风格 |
| `project_fact` | 项目事实，如技术栈、命令、约束 |
| `task_state` | 未完成任务、阶段状态、待办 |
| `episodic_trace` | 某次任务过程和结果 |
| `failure_lesson` | 失败经验、避免重复错误的策略 |
| `preference_update` | 用户偏好或事实更新 |

## 6. 评测设计

基础对照组：

1. `no_memory`：无长期记忆。
2. `raw_history`：朴素历史/检索 baseline。
3. `mem0`：Mem0 backend。

核心指标：

- `answer_accuracy`
- `task_success_rate`
- `retrieval_recall@k`
- `memory_precision`
- `conflict_resolution_accuracy`
- `abstention_accuracy`
- `latency`
- `token_cost`
- `tool_call_count`
- `regression_rate`

自建场景优先级高于公开 benchmark，因为本项目需要评测任务型 agent 的记忆收益。

首批自建场景：

| 场景 | 目的 |
|---|---|
| 用户偏好记忆 | 跨会话应用用户偏好 |
| 项目事实记忆 | 记住项目约束，减少重复探索 |
| 任务状态记忆 | 中断后恢复未完成任务 |
| 失败经验记忆 | 避免重复失败 |
| 事实更新与冲突 | 使用最新事实，抑制旧事实 |
| 无依据拒答 | 没有记忆依据时不编造 |
| 轻量多模态记忆 | 记住图片/截图/图表相关事实 |

公开 benchmark：

- LongMemEval：https://github.com/xiaowu0162/LongMemEval
- LoCoMo：https://github.com/snap-research/locomo
- LoCoMo-Plus：https://github.com/xjtuleeyf/Locomo-Plus

## 7. 阶段计划

| 阶段 | 目标 | 退出条件 |
|---|---|---|
| P0 | 初始化 Codex 可持续接手的项目文档和配置 | 状态、规则、计划、初始化清单齐备 |
| P1 | 跑通 `smolagents` 最小 agent | 能问答、调用工具、保存 trace |
| P2 | 接入记忆接口和 baseline | 可切换 `no_memory`、`raw_history`、`mem0` |
| P3 | 建立自建评测集 | 30-50 条样本可自动跑完 |
| P4 | 接入公开 benchmark 小样本 | LongMemEval 或 LoCoMo 至少跑通一个 |
| P5 | 误差分析 | 形成失败样例分类和优化假设 |
| P6 | 第一轮优化 | 至少一个核心指标提升且 regression 可控 |

## 8. 预期仓库结构

```text
agent-memory-lab/
  AGENTS.md
  README.md
  PROJECT_STATUS.md
  PROJECT_RULES.md
  PROJECT_INIT.md
  agent_memory_project_plan.md
  pyproject.toml
  .env.example
  .gitignore
  configs/
    agent.yaml
    memory.yaml
    eval.yaml
    model.local.yaml.example
  agent_lab/
    agent_runner.py
    trace.py
    prompts.py
    tools/
    memory/
  eval/
    runner.py
    metrics.py
    datasets/
    adapters/
    reports/
  traces/
  tests/
```

## 9. 当前执行入口

后续每次 Codex 接手本项目时，应先读：

1. `PROJECT_STATUS.md`
2. `PROJECT_RULES.md`
3. `agent_memory_project_plan.md`
4. `PROJECT_INIT.md`

任务状态只维护在 `PROJECT_STATUS.md`。规则和约束只维护在 `PROJECT_RULES.md`。本文件只保留目标、架构和路线，不再承担任务看板职责。
