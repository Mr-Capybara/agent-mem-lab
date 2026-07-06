# Agent Memory Lab

本项目用于研究 agent 记忆系统及其自进化。

当前第一阶段固定主线：

- Agent 底座：`smolagents`
- 记忆系统起点：`Mem0`
- 目标：构建可复现、可追踪、可替换 memory backend 的实验台

## 文档入口

新会话或新 agent 接手时先读：

1. `AGENTS.md`
2. `PROJECT_STATUS.md`
3. `PROJECT_RULES.md`
4. `agent_memory_project_plan.md`
5. `PROJECT_INIT.md`

## 当前阶段

当前处于 P0/P1 交界：

- P0：项目文档与初始化配置
- P1：跑通最小 `smolagents` agent

## 基础命令

依赖尚未安装前，可先运行标准库测试：

```bash
python -m pytest
```

后续安装依赖后再补充 `uv` 命令和 agent smoke test。
