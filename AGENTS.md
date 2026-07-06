# AGENTS.md

本文件是 Codex 或其他代码 agent 接手本项目时的入口。

## 必读顺序

每次新会话开始，先读：

1. `PROJECT_STATUS.md`
2. `PROJECT_RULES.md`
3. `agent_memory_project_plan.md`
4. `PROJECT_INIT.md`

## 当前项目主线

```text
Agent 底座：smolagents
Memory 起点：Mem0
目标：构建 agent 记忆系统实验台
阶段：P0 初始化
```

## 工作方式

- 任务状态只更新 `PROJECT_STATUS.md`。
- 项目规则只更新 `PROJECT_RULES.md`。
- 计划路线只更新 `agent_memory_project_plan.md`。
- 初始化配置只更新 `PROJECT_INIT.md`。
- 不依赖隐式上下文。
- 重要决策必须落文档。

## 开始任务前检查

1. 当前任务属于哪个阶段？
2. `PROJECT_STATUS.md` 中对应任务状态是什么？
3. 是否违反 `PROJECT_RULES.md`？
4. 是否需要更新初始化配置？
5. 完成后是否需要更新状态文件？
