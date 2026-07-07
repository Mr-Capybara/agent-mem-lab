# Project Rules

更新日期：2026-07-07

## 硬约束

- 第一阶段固定主线：`smolagents + Mem0 + Python`。
- 包管理器优先使用 `uv`。
- 真实 API key 只能来自本地环境变量或未跟踪 `.env`，不得写入仓库、测试、配置示例、commit message 或命令输出。
- qwen3.7-plus 使用 OpenAI-compatible 接口：`WQ_API_KEY`、`WQ_BASE_URL`、`WQ_MODEL_ID`。
- 长期记忆必须通过统一 `MemoryBackend` 接口接入，不能把业务逻辑写死到 Mem0。
- 所有实验和 agent 运行必须能保存 trace。
- 默认不做完整桌面 GUI agent，不做生产运维 agent，不做任意 shell agent。

## 安全边界

- 不直接暴露任意 shell 给 agent。
- shell 工具必须限制工作目录、命令白名单、超时和危险命令。
- 禁止 agent 自动执行删除、重置、批量覆盖、权限变更、后台常驻进程等高风险操作。
- 文件读写默认限制在项目目录或显式 sandbox 目录。
- 多模态第一阶段只做图片、截图、OCR/图表读数等轻量能力。

## 工程规则

- 配置外置到 `configs/` 或环境变量，不硬编码路径、密钥、模型地址。
- 测试默认使用 offline model，不依赖真实 API。
- 新增真实 API 能力时必须有 offline fallback。
- 代码保持小模块；新增能力要配测试。
- 运行输出写入 `traces/` 或 `eval/reports/`，不要混入源码目录。

## 评测规则

- baseline 至少保留：`no_memory`、`raw_history`、`mem0`。
- 同一批 case 必须能在不同 backend 下重复运行。
- 每次评测记录配置、模型、backend、输入、输出、trace、metrics。
- 优先自建小样本闭环，再接 LongMemEval/LoCoMo。
- 新优化必须报告收益和 regression。

## 文档规则

- `PROJECT_STATUS.md` 是唯一任务状态源。
- `PROJECT_RULES.md` 是唯一长期规则源。
- `agent_memory_project_plan.md` 只放目标架构和阶段路线。
- 完成任务后更新状态文件；改变长期约束才更新规则文件。
