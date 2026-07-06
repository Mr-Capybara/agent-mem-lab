# Project Rules

更新日期：2026-07-06

本文件记录项目长期规则。后续 Codex 或其他 agent 接手时必须先读本文件。

## 1. 项目边界

- 第一阶段固定使用 `smolagents + Mem0`。
- 不在第一阶段引入重型多 agent 平台。
- 不在第一阶段追求完整桌面 GUI agent。
- 不在第一阶段做成熟自进化算法。
- 所有架构必须允许替换 memory backend。

## 2. 工程规则

- 使用 Python。
- 包管理器优先使用 `uv`。
- 代码必须保持模块小而清晰。
- 不把业务逻辑写死到 Mem0 API 上。
- 任何 memory backend 都必须实现统一 `MemoryBackend` 接口。
- 配置必须外置到 `configs/` 或 `.env`，不要硬编码密钥、模型地址、路径。
- 所有实验输出写入 `traces/` 或 `eval/reports/`，不要混在源码目录。

## 3. Agent 执行安全

- 不直接暴露任意 shell 给 agent。
- shell 能力必须通过受控工具封装。
- 受控 shell 至少要限制工作目录、命令白名单或危险命令拦截。
- 文件读写默认限制在项目目录或实验 sandbox 目录。
- 不允许 agent 自动执行删除、重置、覆盖大量文件等危险操作。
- 多模态工具默认只做图片、截图、OCR、图表读数等轻量任务。

## 4. 记忆系统规则

- 长期记忆由外部 `MemoryBackend` 管理，不依赖 `smolagents` 内部 memory。
- 每次 agent 调用前记录检索到的 `retrieved_memories`。
- 每次 prompt 注入前记录实际注入的 `memory_context`。
- 每次写入记忆时记录 `memory_writes`。
- 记忆必须带元数据：`user_id`、`project_id`、`session_id`、`memory_type`、`source`、`timestamp`。
- 对事实更新和偏好更新必须保留时间或版本信息。
- 没有依据的记忆问题必须允许 agent 拒答，不得鼓励编造。

## 5. 评测规则

- 所有能力都要能通过自动化评测调用。
- 至少保留三组 baseline：`no_memory`、`raw_history`、`mem0`。
- 同一批 case 必须能在不同 backend 下重复运行。
- 每次评测必须保存配置、模型、backend、输入、输出、trace、metrics。
- 优先自建小样本闭环，再接公开 benchmark。
- 新优化必须报告收益和 regression。

## 6. 文档维护规则

- `PROJECT_STATUS.md` 是唯一任务状态源。
- `PROJECT_RULES.md` 是唯一规则源。
- `agent_memory_project_plan.md` 只维护目标、路线、架构，不放详细任务看板。
- `PROJECT_INIT.md` 维护初始化配置和环境清单。
- 完成任务后必须更新 `PROJECT_STATUS.md`。
- 改变规则前必须更新 `PROJECT_RULES.md`，并在状态文件记录决策。

## 7. Codex 工作规则

- 每次开始新会话，先读 `AGENTS.md`。
- 再读 `PROJECT_STATUS.md` 和 `PROJECT_RULES.md`。
- 若任务涉及路线或架构，再读 `agent_memory_project_plan.md`。
- 若任务涉及初始化、依赖、配置，再读 `PROJECT_INIT.md`。
- 不要依赖上个会话的隐式上下文。
- 重要实验结论必须落文档。
