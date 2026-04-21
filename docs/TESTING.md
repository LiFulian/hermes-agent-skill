# Universal Memory Skill - 测试方案

## 测试策略

### 1. 单元测试
验证各个模块独立功能

### 2. 集成测试
验证完整工作流

### 3. 手动测试
快速验证功能

---

## 快速手动测试（5分钟）

### 测试1：基础记忆提取

```python
from scripts.memory_extract import MemoryExtractor
from pathlib import Path

extractor = MemoryExtractor(Path("test_mem"))

# 测试对话
conv = "用户说我用Python开发，我偏好pytest测试"
entries = extractor.extract_from_conversation(conv)

print(f"提取到 {len(entries)} 条记忆")
assert len(entries) > 0, "应该提取到记忆"

# 验证内容
found = any("Python" in e.content for e in entries)
assert found, "应该包含Python"

# 验证保存
extractor.merge_into_memory(entries)
content = extractor.user_file.read_text()
assert "Python" in content, "Python应该被保存"

print("✅ 测试通过！")
```

运行：
```bash
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '.')
from scripts.memory_extract import MemoryExtractor

extractor = MemoryExtractor(Path('/tmp/test_mem'))
conv = '用户说我用Python开发'
entries = extractor.extract_from_conversation(conv)
extractor.merge_into_memory(entries)
print(f'提取: {len(entries)}条')
print('MEMORY:', extractor.memory_file.read_text()[:200])
print('USER:', extractor.user_file.read_text()[:200])
"
```

---

## 自动化测试

### 运行所有测试

```bash
# 运行pytest
pytest tests/ -v

# 带覆盖率
pytest tests/ -v --cov=scripts --cov=cli

# 运行特定测试
pytest tests/test_memory_extract.py -v
```

### 测试清单

| 测试 | 命令 | 预期 |
|------|------|------|
| 记忆提取 | `pytest tests/test_memory_extract.py -v` | 全部通过 |
| 记忆注入 | `pytest tests/test_memory_inject.py -v` | 全部通过 |
| 记忆清理 | `pytest tests/test_memory_cleanup.py -v` | 全部通过 |
| CLI命令 | `pytest tests/test_cli_commands.py -v` | 全部通过 |
| 技能格式 | `pytest tests/test_skill_format.py -v` | 全部通过 |
| 集成测试 | `pytest tests/integration/ -v` | 全部通过 |

---

## Demo测试

### 运行日历待办Demo

```bash
# 使用Python直接运行
cd universal-memory-skill
PYTHONPATH=. python3 demos/calendar_todo/demo_real_memory.py

# 预期输出
# - 提取多条记忆
# - 保存到 ~/.universal-memory/
```

### 验证记忆文件

```bash
# 查看记忆
cat ~/.universal-memory/MEMORY.md
cat ~/.universal-memory/USER.md

# 或使用CLI
universal-memory view
universal-memory stats
```

---

## CLI工具测试

### 测试命令

```bash
# 查看帮助
universal-memory --help

# 查看记忆
universal-memory view

# 搜索
universal-memory search "Python"

# 统计
universal-memory stats
```

### 预期结果

- `view` 显示记忆文件内容
- `search` 找到匹配的条目
- `stats` 显示字符统计

---

## 兼容性测试

### 测试不同工具

| 工具 | 测试方法 |
|------|---------|
| Claude Desktop | 添加自定义指令，验证AI读取记忆 |
| Cursor | 添加rules，验证记忆生效 |
| Trae | 配置skill，验证功能 |

### 验证方法

1. 在工具中输入：`"你记得我用什么语言吗？"`
2. 验证AI能回答正确
3. 在工具中输入新信息
4. 验证记忆被更新

---

## 性能测试

### 大文件测试

```bash
# 创建大记忆文件
for i in {1..50}; do
  echo "- 记忆条目 $i" >> ~/.universal-memory/MEMORY.md
done

# 运行清理
universal-memory stats

# 验证文件被清理到限制内
wc -c ~/.universal-memory/MEMORY.md
# 应该 < 2200
```

---

## 回归测试

每次修改代码后运行：

```bash
# 1. 运行所有pytest测试
pytest tests/ -v

# 2. 运行Demo
PYTHONPATH=. python3 demos/calendar_todo/demo_real_memory.py

# 3. 手动验证
cat ~/.universal-memory/MEMORY.md
```

全部通过才算合格。

---

## 问题排查

### 记忆提取失败

检查：
1. 对话是否包含关键字
2. 字符长度是否足够
3. 正则表达式是否匹配

### 记忆保存失败

检查：
1. 目录是否有写权限
2. 字符是否超限
3. 文件格式是否正确

### CLI不工作

检查：
1. 是否安装：`pip install -e .`
2. 是否在正确目录
3. Python路径是否正确

---

## 测试报告模板

```markdown
## 测试日期: YYYY-MM-DD

### 环境
- Python版本:
- 操作系统:
- 安装方式:

### 结果
- [ ] 单元测试
- [ ] 集成测试
- [ ] Demo测试
- [ ] CLI测试

### 问题
无 / 列出问题

### 结论
通过 / 需要修复
```
