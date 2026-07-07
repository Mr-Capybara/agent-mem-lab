# Agent 记忆系统及自进化研究计划

更新日期：2026-07-07

## 目标

构建一个本地 agent 记忆系统实验台，用于研究长期记忆、任务经验记忆和后续自进化。当前只做前三步：

1. 跑通本地 agent：问答、简单任务、轻量多模态、自动化评测。
2. 接入可替换记忆系统：先 `Mem0`，同时保留 baseline。
3. 构建评测链路：验证有记忆相对无记忆的效果。

## 固定选型

```text
Agent：smolagents
Memory：Mem0 起点，NoMemory/RawHistory baseline
模型：qwen3.7-plus OpenAI-compatible；offline fake model 用于测试
语言：Python 3.11
依赖：uv
```

## 当前目标：CLI agent v0

先做一个不 toy 的本地工程助理：

- 命令行多轮交互。
- qwen/offline provider 可切换。
- calculator、文件读写、受控 shell。
- 每轮保存 trace。
- 能回答项目问题、读写小文件、跑测试/ruff/git status/git diff。
- 暂不要求 Mem0 长期记忆，但接口要保持可接入。

## 目标架构

```text
CLI / Eval Harness
  -> AgentRunner
      -> MemoryBackend: no_memory | raw_history | mem0
      -> smolagents ToolCallingAgent
      -> controlled tools: calculator | files | shell | future vision
      -> JsonlTraceWriter
```

关键原则：

- 长期记忆不依赖 `smolagents` 内部 memory。
- 所有 backend 跑同一套评测。
- 测试不依赖真实模型。
- 真实模型能力通过环境变量配置。

## 记忆类型

| 类型 | 用途 |
|---|---|
| `user_profile` | 用户偏好 |
| `project_fact` | 项目事实和约束 |
| `task_state` | 未完成任务状态 |
| `episodic_trace` | 单次任务过程和结果 |
| `failure_lesson` | 失败经验 |
| `preference_update` | 偏好/事实更新 |

## 评测方向

| 场景 | 验证点 |
|---|---|
| 用户偏好记忆 | 跨会话应用偏好 |
| 项目事实记忆 | 遵守项目约束，减少重复探索 |
| 任务状态记忆 | 中断后恢复 |
| 失败经验记忆 | 避免重复失败 |
| 事实更新与冲突 | 使用最新事实 |
| 无依据拒答 | 不幻觉式回忆 |
| 轻量多模态记忆 | 图片/截图事实记忆 |

公开 benchmark 后续接入：LongMemEval、LoCoMo、LoCoMo-Plus。

## 阶段路线

| 阶段 | 目标 |
|---|---|
| P0 | 文档、仓库、环境初始化 |
| P1 | CLI agent v0：可交互、可用基础工具、可保存 trace |
| P2 | Mem0Backend 接入和 baseline 对照 |
| P3 | 自建评测集 30-50 条 |
| P4 | 接入公开 benchmark 小样本 |
| P5 | 误差分析和第一轮记忆优化 |
