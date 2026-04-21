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
