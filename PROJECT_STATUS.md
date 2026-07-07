# Project Status

更新日期：2026-07-07

## 当前状态

```text
阶段：P1 agent 能力接入
短期目标：CLI agent v0，本地工程助理，可交互、可调用基础工具、可保存 trace
工作区：/Users/yinzehua/code/agent-mem-lab
Git 状态：上次检查为 clean
```

已确定：

- Agent 底座：`smolagents`
- Memory 起点：`Mem0`
- 模型入口：qwen3.7-plus OpenAI-compatible
- qwen endpoint：`ep-1rl9f4-1783391033049812063`
- qwen base URL：`http://wanqing.internal/api/gateway/v1/endpoints`
- API key：只允许从 `WQ_API_KEY` 环境变量读取，不能写入仓库

## 已完成

| 项 | 状态 | 说明 |
|---|---|---|
| 文档入口 | DONE | `AGENTS.md`、`PROJECT_STATUS.md`、`PROJECT_RULES.md`、计划文件已建立 |
| 工程骨架 | DONE | `agent_lab/`、`configs/`、`eval/`、`tests/`、`scripts/` |
| Python 环境 | DONE | Homebrew `uv`、Python 3.11、`.venv`、`uv.lock` |
| Memory 接口 | DONE | `MemoryBackend`、`NoMemoryBackend`、`RawHistoryBackend` |
| Trace | DONE | `AgentTrace`、`JsonlTraceWriter` |
| smolagents 接入 | DONE | `AgentRunner` 使用真实 `ToolCallingAgent` loop |
| 离线模型 | DONE | `OfflineFinalAnswerModel`，保证测试不依赖外部 API |
| qwen 配置入口 | DONE | `model_factory` 支持 `wq_openai_compatible` |
| 手动运行脚本 | DONE | `scripts/run_agent_once.py` |

## 待完成

| 优先级 | 任务 | 目标 |
|---|---|---|
| P0 | CLI agent v0 | 多轮命令行交互，qwen/offline 可切换，trace 持久化 |
| P0 | 受控工具集 | calculator、文件读写、受控 shell 白名单 |
| P0 | qwen live smoke | 用户本地设置 `WQ_API_KEY` 后验证真实模型调用 |
| P1 | Mem0Backend | 接入 Mem0，仍保留 no_memory/raw_history baseline |
| P1 | 自建评测 schema | 为偏好、项目事实、任务状态、失败经验构造 JSONL |
| P2 | 轻量 vision | 图片/截图理解接口，先做能力边界与 smoke |

## 最近提交

```text
f26b153 Add qwen OpenAI-compatible model configuration
821b436 Integrate AgentRunner with smolagents offline mode
3c44398 Set up Python environment and smolagents smoke test
f8efffd Initialize agent memory lab scaffold
d23a8e6 init
```

## 验证记录

最近一次有效验证：

```text
pytest: 7 passed
ruff: All checks passed
offline manual smoke: PASS
secret scan: 未发现真实 key 写入仓库
qwen live smoke: NOT RUN，当前执行环境未设置 WQ_API_KEY
```

pytest 有过 `.pytest_cache` 写入 warning，不影响测试结果。

## 下一轮建议

建议直接做 **CLI agent v0**，不要再只补骨架：

1. 实现 `scripts/chat_agent.py`。
2. 支持 `--provider offline|wq_openai_compatible`。
3. 支持多轮输入、`/exit`、`/status`、`/trace`。
4. 接入 calculator 和受控文件工具。
5. 受控 shell 先只开放低风险命令：`pwd`、`ls`、`python -m pytest`、`ruff check`、`git status`、`git diff`。
6. 每轮写 JSONL trace。
7. 跑 pytest/ruff，更新本文件，commit。
