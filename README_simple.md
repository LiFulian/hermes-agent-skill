# Universal Memory Skill - 通用记忆技能

> 给任何AI工具添加记忆能力，跨会话记住用户的偏好和工作习惯

## 3分钟快速开始

### 1. 安装
```bash
git clone <repo-url>
cd universal-memory-skill
pip install -e .
```

### 2. 创建记忆目录
```bash
mkdir -p ~/.universal-memory
```

### 3. 给AI配置记忆

把下面这段话添加到你的AI工具的自定义指令/系统提示中：

```
你有一个记忆系统，记忆文件在 ~/.universal-memory/
- 会话开始时读取 MEMORY.md 和 USER.md
- 发现重要信息时自动更新记忆文件
- MEMORY.md：存储项目信息和工作模式
- USER.md：存储用户偏好和习惯
```

### 完成！

现在你的AI就能跨会话记住：
- 你的偏好（用什么工具、什么语言）
- 你的项目（做什么、怎么做）
- 你的习惯（什么时候工作、喜欢什么方式）

---

## 🤖 AI使用指南

如果你是AI智能体，按以下步骤使用记忆系统：

### AI的职责

1. **会话开始时**：读取 `~/.universal-memory/MEMORY.md` 和 `~/.universal-memory/USER.md`
2. **会话中**：识别重要信息并更新记忆
3. **会话结束时**：确保记忆已保存

### 记忆文件格式

**USER.md**（用户偏好）：
```markdown
# User Profile

## Preferences
- 语言：Python
- 工具：Cursor
- 测试：pytest

## Projects
- 项目名：描述

## Coding Style
- 命名：snake_case
- 类型：必须用type hints
```

**MEMORY.md**（项目记忆）：
```markdown
# Agent Memory

## Project Context
- 项目：描述
- 技术栈：Python/FastAPI

## Learned Patterns
- 这个项目的常见问题

## Key Facts
- 部署在AWS
```

### AI操作指南

**读取记忆**：
```python
memory_file = Path("~/.universal-memory/MEMORY.md")
user_file = Path("~/.universal-memory/USER.md")

memory_content = memory_file.read_text()
user_content = user_file.read_text()
```

**更新记忆**：
```python
# 添加新记忆时：
# 1. 读取现有内容
# 2. 判断类型（USER.md存偏好，MEMORY.md存项目）
# 3. 追加或更新
# 4. 保持简洁，不超过限制
```

**重要原则**：
- 只记住真正重要的信息
- 保持简洁（USER.md ≤ 1500字符，MEMORY.md ≤ 2200字符）
- 优先更新而非添加
- 删除过时信息

### AI应记住什么

✅ **应记住**：
- 用户明确说过的偏好
- 项目关键信息
- 技术决策和约束
- 工作流程和习惯

❌ **不应记住**：
- 临时会话信息
- 明显的常识
- 敏感信息（密码、密钥）

---

## 工作原理

```
用户告诉AI → AI记住 → 下次会话自动应用
"我用Python"    →  "Python"写入USER.md → 以后默认用Python
"下周一开会"    →  "周一开会"写入MEMORY.md → 下次提到自动关联
```

## 查看记忆

```bash
# 查看当前记忆
cat ~/.universal-memory/MEMORY.md
cat ~/.universal-memory/USER.md

# 或者用CLI
universal-memory view
```

## 记忆示例

```markdown
# USER.md
- 语言：Python
- 日历：Google日历
- 提醒：提前30分钟

# MEMORY.md
- 产品团队Q2规划会议（周一10点）
- 每周五发周报
- 项目：网页爬虫
```

## 支持的工具

Claude / Cursor / Trae / Windsurf / ChatGPT / Copilot / 任何AI工具

## 项目结构

```
universal-memory-skill/
├── skills/              # AI使用的记忆指令
│   ├── memory.md        # 核心记忆技能
│   └── memory-reflect.md
├── scripts/             # Python辅助脚本
│   ├── memory_extract.py   # 提取记忆
│   └── memory_inject.py    # 注入记忆
├── cli/                # 命令行工具
│   └── universal-memory   # view/search/stats
├── tests/              # 测试
└── demos/              # 示例
```

## 开发者

```bash
# 运行测试
pytest tests/ -v

# 运行Demo
python demos/calendar_todo/demo_real_memory.py

# 查看记忆文件
universal-memory view
```

## 限制

- MEMORY.md 最多2200字符
- USER.md 最多1500字符
- AI会自动清理和去重

## 许可证

MIT
