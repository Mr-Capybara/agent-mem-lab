# AGENTS.md

Codex/agent 接手本项目时先读本文件。

## 必读顺序

1. `PROJECT_STATUS.md`：当前事实、进度、下一步。
2. `PROJECT_RULES.md`：长期工程和实验规则。
3. `agent_memory_project_plan.md`：目标架构和阶段路线。
4. `PROJECT_INIT.md`：仅在改初始化/依赖/目录结构时阅读。

## 当前主线

```text
项目目录：/Users/yinzehua/code/agent-mem-lab
Agent 底座：smolagents
Memory 起点：Mem0
模型：qwen3.7-plus，OpenAI-compatible，key 只读 WQ_API_KEY
当前目标：做出 CLI agent v0，本地工程助理可交互可执行基础任务
```

## 工作规则

- 开始任务前读 `PROJECT_STATUS.md` 和 `PROJECT_RULES.md`。
- 不依赖上个会话隐式上下文。
- 每轮先告诉用户准备做什么，得到同意后实施。
- 任务状态只更新 `PROJECT_STATUS.md`。
- 改长期规则才更新 `PROJECT_RULES.md`。
- 重要改动完成后运行测试/lint，更新状态，并 commit。
- 真实 API key 不得写入仓库、命令记录、测试或示例配置。
