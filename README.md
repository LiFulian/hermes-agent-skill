# Universal Memory Skill / 通用记忆技能

> Give any AI agent Hermes-like persistent memory capabilities / 让任何AI工具都具有Hermes Agent级别的持久记忆能力

![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tests](https://img.shields.io/badge/Tests-71%20passed-4CAF50)
![Coverage](https://img.shields.io/badge/Coverage-79%25-4CAF50)

## What is This? / 这是什么？

Universal Memory Skill transforms any AI agent into a persistent, learning-capable assistant / 将任何AI智能体转变为具有持久记忆、学习能力的助手

- **Cross-session memory** / 跨会话记忆：AI remembers your preferences, projects, and patterns / 记住你的偏好、项目和工作模式
- **Automatic memory management** / 自动记忆管理：No manual note-taking / 无需手动记录，AI自动提取和保存重要信息
- **Universal compatibility** / 通用兼容性：Works with any AI IDE or tool / 适用于任何AI IDE或工具

## Quick Start / 快速开始

### Installation / 安装

```bash
git clone https://github.com/LiFulian/hermes-agent-skill.git
cd hermes-agent-skill
pip install -e .
```

### Configuration / 配置

Add to your AI tool's custom instructions / 添加到AI工具的自定义指令：

```
You have persistent memory at ~/.universal-memory/
- Read MEMORY.md and USER.md at session start
- Update memory when important info is discovered
- MEMORY.md: Project context and patterns
- USER.md: User preferences and habits

你有一个记忆系统，记忆文件在 ~/.universal-memory/
- 会话开始时读取 MEMORY.md 和 USER.md
- 发现重要信息时自动更新记忆文件
```

## Memory Files / 记忆文件

### USER.md - User Profile / 用户档案

```markdown
# User Profile / 用户档案

## Preferences / 偏好
- Language: Python / 语言：Python
- IDE: Cursor
- Testing: pytest / 测试：pytest

## Projects / 项目
- Web Scraper / 网页爬虫
```

### MEMORY.md - Agent Memory / 智能体记忆

```markdown
# Agent Memory / 智能体记忆

## Project Context / 项目背景
- Tech stack: Python, FastAPI / 技术栈

## Key Facts / 关键事实
- Deployment: AWS Lambda / 部署在AWS
```

**Limits / 限制**：USER.md ≤ 1500 chars，MEMORY.md ≤ 2200 chars

## How It Works / 工作原理

```
User → AI remembers → Next session applies
"我用Python" → Python写入USER.md → 以后默认用Python
"I prefer pytest" → pytest写入USER.md → 以后默认用pytest
```

## CLI Tools / 命令行工具

```bash
universal-memory view      # View memory / 查看记忆
universal-memory search    # Search memory / 搜索记忆
universal-memory stats     # Show stats / 显示统计
universal-memory save      # Save info / 保存信息
```

## Compatibility / 兼容性

Works with / 支持：Claude, Cursor, Trae, Windsurf, ChatGPT, Copilot, Ollama, any AI tool

See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md) for details / 查看详细配置说明

## Development / 开发

```bash
# Run tests / 运行测试
pytest tests/ -v

# Run demo / 运行示例
python demos/calendar_todo/demo_runner.py
```

## License / 许可证

MIT License - Free to use / MIT许可证 - 免费使用

## Support / 支持

- Docs / 文档：[docs/](docs/)
- Issues：[GitHub Issues](https://github.com/LiFulian/hermes-agent-skill/issues)
- Discussions：[GitHub Discussions](https://github.com/LiFulian/hermes-agent-skill/discussions)
