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


## 真实模型 smoke

本项目支持 qwen3.7-plus 的 OpenAI-compatible 接入。不要把真实 API Key 写入仓库；只在本地 shell 或未跟踪 `.env` 中设置：

```bash
export AGENT_MODEL_PROVIDER=wq_openai_compatible
export WQ_API_KEY=...
export WQ_BASE_URL=http://wanqing.internal/api/gateway/v1/endpoints
export WQ_MODEL_ID=ep-1rl9f4-1783391033049812063
.venv/bin/python scripts/run_agent_once.py --provider wq_openai_compatible "请用一句话介绍太阳系。"
```

离线 smoke 不需要外部模型：

```bash
.venv/bin/python scripts/run_agent_once.py --provider offline "请用一句话介绍太阳系。" --trace /private/tmp/agent-mem-lab-offline-manual.jsonl
```
