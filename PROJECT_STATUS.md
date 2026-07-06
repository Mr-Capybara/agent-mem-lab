# Project Status

更新日期：2026-07-06

## 当前结论

已确定第一阶段主线：

```text
Agent 底座：smolagents
Memory 起点：Mem0
工程推进：Codex 持续维护
当前阶段：P1 最小 agent 工程骨架
```

## 当前阶段目标

P1：在已完成文档和项目骨架基础上，跑通 `smolagents` 最小 agent。

退出条件：

- `agent_memory_project_plan.md` 精简为主计划。
- `PROJECT_STATUS.md` 记录任务状态。
- `PROJECT_RULES.md` 记录项目规则。
- `PROJECT_INIT.md` 记录初始化配置。
- `AGENTS.md` 作为 Codex 接手入口。
- 用户已审核通过并初始化 git 仓库。

## 任务看板

状态取值：

- `TODO`：尚未开始。
- `DOING`：正在进行。
- `DONE`：已完成。
- `BLOCKED`：阻塞。
- `DEFER`：明确延后。

| ID | 状态 | 优先级 | 任务 | 产出 |
|---|---|---|---|---|
| P0-T1 | DONE | P0 | 确定 `smolagents + Mem0` 主线 | 主计划 |
| P0-T2 | DONE | P0 | 精简原计划文件 | `agent_memory_project_plan.md` |
| P0-T3 | DONE | P0 | 新建任务状态文件 | `PROJECT_STATUS.md` |
| P0-T4 | DONE | P0 | 新建项目规则文件 | `PROJECT_RULES.md` |
| P0-T5 | DONE | P0 | 新建初始化配置文件 | `PROJECT_INIT.md` |
| P0-T6 | DONE | P0 | 新建 Codex 接手入口文件 | `AGENTS.md` |
| P0-T7 | DONE | P0 | 用户审核文档体系 | 用户确认 |
| P0-T8 | DONE | P0 | 初始化 git 仓库 | `.git/` |
| P0-T9 | DONE | P0 | 创建工程骨架 | `pyproject.toml`、`configs/`、`agent_lab/`、`eval/` |
| P1-T1 | DONE | P1 | 安装并跑通 `smolagents` 最小样例 | smoke test |
| P1-T2 | DONE | P1 | 实现 `AgentRunner` | `agent_lab/agent_runner.py` |
| P1-T3 | DOING | P1 | 实现受控工具集 | `agent_lab/tools/` |
| P1-T4 | DONE | P1 | 实现 trace logger | `agent_lab/trace.py` |
| P2-T1 | DONE | P2 | 定义 `MemoryBackend` 接口 | `agent_lab/memory/base.py` |
| P2-T2 | DONE | P2 | 实现 `NoMemoryBackend` | baseline |
| P2-T3 | DONE | P2 | 实现 `RawHistoryBackend` | baseline |
| P2-T4 | TODO | P2 | 实现 `Mem0Backend` | memory backend |
| P3-T1 | TODO | P3 | 定义自建评测 JSONL schema | dataset schema |
| P3-T2 | TODO | P3 | 构造 30-50 条自建样本 | custom cases |
| P3-T3 | TODO | P3 | 实现评测 runner | `eval/runner.py` |
| P4-T1 | TODO | P4 | 接入 LongMemEval 小样本 | adapter |
| P4-T2 | TODO | P4 | 接入 LoCoMo 小样本 | adapter |
| P5-T1 | TODO | P5 | 建立误差分析分类 | report |

## 最近决策记录

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-07-06 | 选用 `smolagents` 作为 agent 底座 | 轻量、可拆、适合接记忆系统 |
| 2026-07-06 | 选用 `Mem0` 作为记忆系统起点 | 接入快，适合作为第一版优化对象 |
| 2026-07-06 | 文档拆分为计划、状态、规则、初始化、入口 | 便于 Codex 跨会话持续推进 |
| 2026-07-06 | 先创建无网络依赖的工程骨架 | 便于后续安装依赖前先稳定接口和规则 |
| 2026-07-06 | 使用 Homebrew 安装 `uv` 和 Python 3.11 | 建立正式项目运行环境 |
| 2026-07-06 | 将 Mem0 本地状态目录重定向到项目 `.local/mem0` | 避免默认写入 `~/.mem0` |
| 2026-07-06 | `AgentRunner` 接入真实 `smolagents` loop | 通过离线 FakeModel 保持可重复测试 |

## 验证记录

| 日期 | 验证 | 结果 | 备注 |
|---|---|---|---|
| 2026-07-06 | 标准库 smoke check | PASS | 验证 `NoMemoryBackend`、`RawHistoryBackend`、calculator；本机默认 `python3` 为 3.9.6 |
| 2026-07-06 | `python3 -m pytest` | NOT RUN | 当前系统 Python 未安装 pytest；待创建正式 3.11/uv 环境后运行 |
| 2026-07-06 | `.venv` pytest | PASS | Python 3.11.15，3 tests passed |
| 2026-07-06 | `.venv` ruff | PASS | `ruff check --no-cache .` passed |
| 2026-07-06 | smolagents smoke | PASS | 使用本地 FakeModel 初始化 `ToolCallingAgent` 并调用测试工具 |
| 2026-07-06 | Mem0 import | PASS | 设置 `MEM0_DIR=.local/mem0` 后 import 成功 |
| 2026-07-06 | AgentRunner integration | PASS | 4 tests passed；验证 memory_context、ToolCallingAgent、trace JSONL |

## 下次接手建议

1. 实现受控 shell 工具的安全版本。
2. 实现轻量 vision 工具占位到可配置接口。
3. 开始 P2-T4：接入 `Mem0Backend`，并保持 `MEM0_DIR` 项目内重定向。
4. 为 `AgentRunner` 增加真实 OpenAI-compatible model 配置入口。
