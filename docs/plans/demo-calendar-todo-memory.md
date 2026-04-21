# Demo Project: 日程待办记忆增强 - 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建一个交互式Demo项目，通过模拟用户创建日程待办场景，展示Universal Memory Skill如何跨会话记住用户偏好和工作模式

**Architecture:** 创建多个Python脚本模拟不同会话场景，使用pytest运行场景并验证记忆文件正确更新，最终生成对比报告

**Tech Stack:** Python 3.8+, pytest, 已有的memory_extract/inject/cleanup脚本

---

## 项目概述

### 演示流程

```
会话1: 首次交互 - 用户创建第一个日程
  ↓ AI提取偏好并保存记忆
  
会话2: 后续交互 - 用户创建待办
  ↓ AI使用记忆中的偏好
  
会话3: 更多交互 - 用户设置重复提醒
  ↓ AI主动应用已知的模式
  
会话4: 复杂场景 - 批量创建一周日程
  ↓ AI根据记忆个性化推荐
  
输出: 记忆文件对比报告
```

### 文件结构

```
demos/
└── calendar-todo/
    ├── scenarios/
    │   ├── session_1_first_meeting.py      # 场景1：首次会议
    │   ├── session_2_create_todo.py         # 场景2：创建待办
    │   ├── session_3_recurring_reminder.py  # 场景3：重复提醒
    │   └── session_4_batch_create.py        # 场景4：批量创建
    ├── test_demo.py                         # 测试和验证
    ├── demo_runner.py                       # Demo运行器
    ├── expected_memory/                     # 期望的记忆结果
    │   ├── after_session_1.md
    │   ├── after_session_2.md
    │   └── after_session_4.md
    └── README.md                            # Demo说明
```

### 场景详细设计

#### 场景1：首次创建会议

**用户对话模拟：**
```
用户：帮我创建一个会议，下周一上午10点和产品团队开会讨论Q2规划
AI：好的，我注意到你偏好在工作日上午安排会议，这个会议要设置提醒吗？
用户：是的，提前30分钟提醒我，我通常用Google日历
```

**应提取的记忆：**
- USER.md: 使用Google日历
- USER.md: 偏好工作日上午安排会议
- MEMORY.md: 产品团队成员
- MEMORY.md: 提醒偏好：提前30分钟

---

#### 场景2：创建待办任务

**用户对话模拟：**
```
用户：我需要添加几个待办事项
AI：好的，我看到你使用Google日历，要同步到日历吗？
用户：好的。第一个是完成项目文档，截止日期是周五
AI：没问题。根据你的偏好，要设置什么时间的提醒？
用户：提前一天吧，我通常在下午处理文档工作
```

**应提取的记忆（新增）：**
- USER.md: 提醒偏好更新：重要事项提前1天
- MEMORY.md: 用户下午处理文档工作
- MEMORY.md: 待办与Google日历集成

---

#### 场景3：重复提醒设置

**用户对话模拟：**
```
用户：帮我设置一个每周例会，每周一下午3点，提醒我准备周报
AI：好的，我注意到你偏好提前准备，要设置提前多久提醒？
用户：提前2小时吧。还有，我每周五下午要发周报给团队
```

**应提取的记忆（新增）：**
- USER.md: 周报提醒：提前2小时
- MEMORY.md: 每周一下午3点例会
- MEMORY.md: 周五下午发周报给团队

---

#### 场景4：批量创建一周日程

**用户对话模拟：**
```
用户：帮我把下周的日程排一下
AI：根据你的习惯，我建议：
- 周一上午：团队例会（已存在）
- 周二到周四上午：项目工作时间
- 周五下午：周报和回顾
需要我这样创建吗？

用户：很好，另外加上周三下午的产品评审，还有周四的技术分享
```

**展示AI的个性化能力：**
- 根据记忆推荐时间安排
- 避免与已有日程冲突
- 应用用户的提醒偏好

---

## 实施步骤

### Task 1: 创建Demo目录结构和场景数据

**Files:**
- Create: `demos/calendar-todo/scenarios/__init__.py`
- Create: `demos/calendar-todo/scenarios/session_1_first_meeting.py`
- Create: `demos/calendar-todo/scenarios/session_2_create_todo.py`
- Create: `demos/calendar-todo/scenarios/session_3_recurring_reminder.py`
- Create: `demos/calendar-todo/scenarios/session_4_batch_create.py`

**Step 1: 创建目录结构**

```bash
mkdir -p demos/calendar-todo/scenarios
mkdir -p demos/calendar-todo/expected_memory
touch demos/calendar-todo/scenarios/__init__.py
```

**Step 2: 编写场景1 - 首次会议**

文件: `demos/calendar-todo/scenarios/session_1_first_meeting.py`

```python
"""场景1：首次创建会议 - 建立用户偏好"""

SESSION_1_CONVERSATION = """
用户：帮我创建一个会议，下周一上午10点和产品团队开会讨论Q2规划

AI助手：好的，我为你创建了以下日程：
📅 会议：产品团队Q2规划会议
🕐 时间：下周一 10:00-11:00
👥 参与人：产品团队
📝 主题：Q2规划讨论

我注意到这是你第一次创建会议，请问：
1. 你需要设置提醒吗？
2. 你通常使用哪个日历系统？

用户：是的，提前30分钟提醒我，我通常用Google日历

AI助手：好的，已设置：
⏰ 提醒：提前30分钟
📆 同步到：Google日历

我记下了你的偏好，以后创建日程会自动应用这些设置。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "使用Google日历",
        "偏好工作日上午安排会议",
        "提醒偏好：提前30分钟",
    ],
    "memory_md": [
        "产品团队成员",
        "Q2规划项目",
    ]
}

def get_conversation():
    return SESSION_1_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
```

**Step 3: 编写场景2 - 创建待办**

文件: `demos/calendar-todo/scenarios/session_2_create_todo.py`

```python
"""场景2：创建待办任务 - AI使用记忆中的偏好"""

SESSION_2_CONVERSATION = """
用户：我需要添加几个待办事项

AI助手：好的，我看到你使用Google日历，要同步到日历吗？
根据你之前的偏好，我会为待办设置提醒。

用户：好的。第一个是完成项目文档，截止日期是周五

AI助手：已创建待办：
✅ 任务：完成项目文档
📅 截止：周五
⏰ 提醒：提前1天（根据你的偏好调整）

还有什么需要添加的？

用户：第二个是准备产品演示，下周三之前完成

AI助手：已创建：
✅ 任务：准备产品演示
📅 截止：下周三
⏰ 提醒：提前30分钟（默认偏好）

用户：好的，我通常在下午处理文档工作

AI助手：好的，我记下了。以后会尽量在下午安排文档类任务。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "提醒偏好更新：重要事项提前1天",
        "下午处理文档工作",
    ],
    "memory_md": [
        "待办与Google日历集成",
        "产品演示任务",
    ]
}

def get_conversation():
    return SESSION_2_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
```

**Step 4: 编写场景3 - 重复提醒**

文件: `demos/calendar-todo/scenarios/session_3_recurring_reminder.py`

```python
"""场景3：重复提醒设置 - 发现定期模式"""

SESSION_3_CONVERSATION = """
用户：帮我设置一个每周例会，每周一下午3点，提醒我准备周报

AI助手：好的，我已创建重复日程：
🔄 每周例会
📅 时间：每周一 15:00
⏰ 提醒：提前2小时

我注意到你偏好提前准备，这样安排可以吗？

用户：好的。还有，我每周五下午要发周报给团队

AI助手：已记录：
📝 每周五下午：发送周报给产品团队

你的周报流程已设置：
1. 周一例会收集信息
2. 周五下午编写并发送
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "周报提醒：提前2小时",
    ],
    "memory_md": [
        "每周一下午3点例会",
        "周五下午发周报给团队",
        "周报流程：周一收集→周五发送",
    ]
}

def get_conversation():
    return SESSION_3_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
```

**Step 5: 编写场景4 - 批量创建**

文件: `demos/calendar-todo/scenarios/session_4_batch_create.py`

```python
"""场景4：批量创建一周日程 - AI主动应用记忆"""

SESSION_4_CONVERSATION = """
用户：帮我把下周的日程排一下

AI助手：根据你的习惯和已有安排，我建议：

📅 下周日程安排：
周一：
- 10:00-11:00 产品团队Q2规划会议
- 15:00-16:00 每周例会（提醒：提前2小时）

周二到周四：
- 上午：项目工作时间（你的偏好）
- 下午：会议和协作时间

周五：
- 下午：周报编写和发送（提醒：提前1天准备）

需要调整吗？

用户：很好，另外加上周三下午的产品评审，还有周四的技术分享

AI助手：已添加：
✅ 周三下午：产品评审
✅ 周四下午：技术分享

完整日程已同步到Google日历，所有提醒已按你的偏好设置。
"""

EXPECTED_MEMORY_UPDATES = {
    "user_md": [
        "上午：项目工作时间",
        "下午：会议和协作时间",
    ],
    "memory_md": [
        "周三下午：产品评审",
        "周四下午：技术分享",
        "AI能主动推荐日程安排",
    ]
}

def get_conversation():
    return SESSION_4_CONVERSATION

def get_expected_updates():
    return EXPECTED_MEMORY_UPDATES
```

**Step 6: Commit**

```bash
git add demos/calendar-todo/scenarios/
git commit -m "feat: add calendar/todo demo scenarios"
```

---

### Task 2: 创建Demo运行器

**Files:**
- Create: `demos/calendar-todo/demo_runner.py`
- Create: `demos/calendar-todo/test_demo.py`

**Step 1: 编写Demo运行器**

文件: `demos/calendar-todo/demo_runner.py`

```python
"""Demo运行器 - 执行场景并验证记忆更新"""

import sys
import tempfile
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.memory_extract import MemoryExtractor
from scripts.memory_inject import MemoryInjector
from scripts.memory_cleanup import MemoryCleaner


class DemoRunner:
    def __init__(self, memory_dir: Path = None):
        if memory_dir is None:
            memory_dir = Path(tempfile.mkdtemp())
        self.memory_dir = memory_dir
        self.extractor = MemoryExtractor(memory_dir)
        self.injector = MemoryInjector(memory_dir)
        self.cleaner = MemoryCleaner(memory_dir)
        
    def run_session(self, conversation: str, session_name: str) -> Dict:
        print(f"\n{'='*60}")
        print(f"运行场景: {session_name}")
        print(f"{'='*60}")
        
        print("\n📖 对话内容:")
        print(conversation[:500] + "..." if len(conversation) > 500 else conversation)
        
        print("\n🔍 提取记忆...")
        entries = self.extractor.extract_from_conversation(conversation)
        print(f"  提取到 {len(entries)} 条记忆条目")
        
        print("\n💾 保存到记忆文件...")
        stats = self.extractor.merge_into_memory(entries)
        print(f"  MEMORY.md: {stats['memory_length']} 字符")
        print(f"  USER.md: {stats['user_length']} 字符")
        
        print("\n📋 当前记忆内容:")
        print("\n--- MEMORY.md ---")
        print(self.extractor.memory_file.read_text())
        print("\n--- USER.md ---")
        print(self.extractor.user_file.read_text())
        
        return {
            "session": session_name,
            "entries_extracted": len(entries),
            "memory_stats": stats,
        }
    
    def run_all_sessions(self, sessions: List[Dict]) -> List[Dict]:
        results = []
        
        print(f"\n{'#'*60}")
        print(f"# Universal Memory Skill - 日程待办Demo")
        print(f"# 共 {len(sessions)} 个场景")
        print(f"{'#'*60}")
        
        for i, session in enumerate(sessions, 1):
            result = self.run_session(
                session["conversation"],
                f"场景{i}: {session['name']}"
            )
            results.append(result)
            
            # 场景间清理
            self.cleaner.cleanup()
        
        return results
    
    def generate_report(self, results: List[Dict]):
        print(f"\n{'='*60}")
        print(f"📊 Demo 报告")
        print(f"{'='*60}")
        
        print(f"\n✅ 共运行 {len(results)} 个场景")
        
        for result in results:
            print(f"\n{result['session']}:")
            print(f"  - 提取记忆: {result['entries_extracted']} 条")
            print(f"  - MEMORY.md: {result['memory_stats']['memory_length']} 字符")
            print(f"  - USER.md: {result['memory_stats']['user_length']} 字符")
        
        print(f"\n{'='*60}")
        print(f"✨ Demo 完成！")
        print(f"记忆文件位置: {self.memory_dir}")
        print(f"{'='*60}")


def main():
    from demos.calendar_todo.scenarios import (
        session_1_first_meeting,
        session_2_create_todo,
        session_3_recurring_reminder,
        session_4_batch_create,
    )
    
    sessions = [
        {
            "name": "首次创建会议",
            "conversation": session_1_first_meeting.get_conversation(),
        },
        {
            "name": "创建待办任务",
            "conversation": session_2_create_todo.get_conversation(),
        },
        {
            "name": "设置重复提醒",
            "conversation": session_3_recurring_reminder.get_conversation(),
        },
        {
            "name": "批量创建一周日程",
            "conversation": session_4_batch_create.get_conversation(),
        },
    ]
    
    runner = DemoRunner()
    results = runner.run_all_sessions(sessions)
    runner.generate_report(results)


if __name__ == "__main__":
    main()
```

**Step 2: 编写测试**

文件: `demos/calendar-todo/test_demo.py`

```python
"""Demo测试 - 验证记忆正确提取和更新"""

import pytest
import tempfile
from pathlib import Path

from demos.calendar_todo.demo_runner import DemoRunner
from demos.calendar_todo.scenarios import (
    session_1_first_meeting,
    session_2_create_todo,
    session_3_recurring_reminder,
    session_4_batch_create,
)


@pytest.fixture
def demo_runner():
    return DemoRunner()


class TestSession1:
    def test_extract_from_first_meeting(self, demo_runner):
        conversation = session_1_first_meeting.get_conversation()
        entries = demo_runner.extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
    
    def test_memory_updated_after_session_1(self, demo_runner):
        conversation = session_1_first_meeting.get_conversation()
        entries = demo_runner.extractor.extract_from_conversation(conversation)
        demo_runner.extractor.merge_into_memory(entries)
        
        memory_content = demo_runner.extractor.memory_file.read_text()
        user_content = demo_runner.extractor.user_file.read_text()
        combined = memory_content + user_content
        
        # 验证关键信息被记住
        assert "Google" in combined or "日历" in combined


class TestSession2:
    def test_memory_persists_across_sessions(self, demo_runner):
        # 先运行场景1
        conversation_1 = session_1_first_meeting.get_conversation()
        entries_1 = demo_runner.extractor.extract_from_conversation(conversation_1)
        demo_runner.extractor.merge_into_memory(entries_1)
        
        # 再运行场景2
        conversation_2 = session_2_create_todo.get_conversation()
        entries_2 = demo_runner.extractor.extract_from_conversation(conversation_2)
        demo_runner.extractor.merge_into_memory(entries_2)
        
        # 验证记忆保留
        memory_content = demo_runner.extractor.memory_file.read_text()
        user_content = demo_runner.extractor.user_file.read_text()
        combined = memory_content + user_content
        
        assert "Google" in combined or "日历" in combined


class TestFullWorkflow:
    def test_all_sessions_complete(self, demo_runner):
        sessions = [
            session_1_first_meeting.get_conversation(),
            session_2_create_todo.get_conversation(),
            session_3_recurring_reminder.get_conversation(),
            session_4_batch_create.get_conversation(),
        ]
        
        for conversation in sessions:
            entries = demo_runner.extractor.extract_from_conversation(conversation)
            demo_runner.extractor.merge_into_memory(entries)
        
        # 验证记忆文件存在且不为空
        assert demo_runner.extractor.memory_file.exists()
        assert demo_runner.extractor.user_file.exists()
        assert len(demo_runner.extractor.memory_file.read_text()) > 0
        assert len(demo_runner.extractor.user_file.read_text()) > 0
    
    def test_memory_respects_limits(self, demo_runner):
        sessions = [
            session_1_first_meeting.get_conversation(),
            session_2_create_todo.get_conversation(),
            session_3_recurring_reminder.get_conversation(),
            session_4_batch_create.get_conversation(),
        ]
        
        for conversation in sessions:
            entries = demo_runner.extractor.extract_from_conversation(conversation)
            demo_runner.extractor.merge_into_memory(entries)
        
        memory_content = demo_runner.extractor.memory_file.read_text()
        user_content = demo_runner.extractor.user_file.read_text()
        
        assert len(memory_content) <= demo_runner.extractor.MEMORY_MD_MAX_CHARS
        assert len(user_content) <= demo_runner.extractor.USER_MD_MAX_CHARS
```

**Step 3: Commit**

```bash
git add demos/calendar-todo/demo_runner.py demos/calendar-todo/test_demo.py
git commit -m "feat: add demo runner and tests"
```

---

### Task 3: 创建Demo文档和运行脚本

**Files:**
- Create: `demos/calendar-todo/README.md`
- Create: `demos/calendar-todo/run_demo.sh`

**Step 1: 编写Demo说明**

文件: `demos/calendar-todo/README.md`

```markdown
# 日历待办记忆增强 Demo

这个Demo展示Universal Memory Skill如何通过模拟用户创建日程待办场景，让AI智能体跨会话记住用户偏好。

## 运行Demo

```bash
# 方式1: 使用脚本
./run_demo.sh

# 方式2: 直接运行Python
python demos/calendar-todo/demo_runner.py

# 方式3: 运行测试
pytest demos/calendar-todo/test_demo.py -v
```

## 场景说明

### 场景1: 首次创建会议
用户首次使用，建立基础偏好（Google日历、工作日上午、提前30分钟提醒）

### 场景2: 创建待办任务
AI展示已记住的偏好，并根据新交互更新记忆

### 场景3: 设置重复提醒
发现用户的定期模式和流程

### 场景4: 批量创建一周日程
AI主动应用所有记忆，个性化推荐日程安排

## 记忆演进

每个场景后，查看 `~/.universal-memory/` 目录下的记忆文件变化：

```
场景1后: 基础偏好建立
场景2后: 待办偏好添加
场景3后: 定期模式发现
场景4后: 完整工作模式形成
```

## 预期效果

✅ AI记住用户使用Google日历
✅ AI记住提醒偏好
✅ AI记住工作时间偏好
✅ AI能主动推荐日程安排
✅ 记忆跨会话保持
✅ 记忆自动优化（不超限制）
```

**Step 2: 创建运行脚本**

文件: `demos/calendar-todo/run_demo.sh`

```bash
#!/bin/bash

echo "============================================="
echo "Universal Memory Skill - 日历待办Demo"
echo "============================================="

# 运行Demo
python demos/calendar-todo/demo_runner.py

# 运行测试
echo ""
echo "运行测试验证..."
pytest demos/calendar-todo/test_demo.py -v
```

**Step 3: 添加执行权限**

```bash
chmod +x demos/calendar-todo/run_demo.sh
```

**Step 4: Commit**

```bash
git add demos/calendar-todo/README.md demos/calendar-todo/run_demo.sh
git commit -m "docs: add demo documentation and run script"
```

---

## 运行方式

### 快速体验

```bash
# 运行完整Demo
./demos/calendar-todo/run_demo.sh
```

### 分步验证

```bash
# 运行测试
pytest demos/calendar-todo/test_demo.py -v

# 查看记忆文件
cat ~/.universal-memory/MEMORY.md
cat ~/.universal-memory/USER.md
```

### 对比效果

Demo会输出：
1. 每个场景提取的记忆条目
2. 记忆文件的完整内容
3. 最终的统计报告

---

## 关键验证点

- [ ] 场景1后：记忆包含Google日历偏好
- [ ] 场景2后：AI展示已记住的偏好
- [ ] 场景3后：定期模式被记录
- [ ] 场景4后：AI能主动推荐日程
- [ ] 所有场景后：记忆文件在字符限制内
- [ ] 所有测试通过
