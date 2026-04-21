"""演示脚本 - 使用真实记忆目录"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.memory_extract import MemoryExtractor
from scripts.memory_inject import MemoryInjector

# 使用真实记忆目录
MEMORY_DIR = Path.home() / ".universal-memory"

def main():
    print(f"\n{'='*60}")
    print(f"使用真实记忆目录: {MEMORY_DIR}")
    print(f"{'='*60}\n")

    # 创建提取器（使用真实目录）
    extractor = MemoryExtractor(MEMORY_DIR)

    # 场景1对话
    conv1 = """
用户：帮我创建一个会议，下周一上午10点和产品团队开会讨论Q2规划
用户：提前30分钟提醒我，我通常用Google日历
"""

    # 场景2对话
    conv2 = """
用户：我需要添加待办事项
用户：我通常在下午处理文档工作
用户：每周五下午要发周报给团队
"""

    print("📝 场景1：首次创建会议")
    print("-" * 40)
    entries1 = extractor.extract_from_conversation(conv1)
    print(f"提取到 {len(entries1)} 条记忆")
    for e in entries1:
        print(f"  - [{e.memory_type.value}] {e.content}")

    extractor.merge_into_memory(entries1)

    print("\n📝 场景2：创建待办任务")
    print("-" * 40)
    entries2 = extractor.extract_from_conversation(conv2)
    print(f"提取到 {len(entries2)} 条记忆")
    for e in entries2:
        print(f"  - [{e.memory_type.value}] {e.content}")

    extractor.merge_into_memory(entries2)

    # 显示记忆文件
    print("\n" + "="*60)
    print("📁 记忆文件内容")
    print("="*60)

    print("\n📄 MEMORY.md:")
    print("-" * 40)
    print(extractor.memory_file.read_text())

    print("\n📄 USER.md:")
    print("-" * 40)
    print(extractor.user_file.read_text())

    # 统计
    mem_size = len(extractor.memory_file.read_text())
    user_size = len(extractor.user_file.read_text())

    print("\n" + "="*60)
    print(f"📊 统计")
    print(f"  MEMORY.md: {mem_size} 字符 (限制: 2200)")
    print(f"  USER.md: {user_size} 字符 (限制: 1500)")
    print("="*60)

if __name__ == "__main__":
    main()
