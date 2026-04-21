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
    """测试场景1：首次创建会议"""
    
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
    """测试场景2：跨会话记忆保持"""
    
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
    """测试完整工作流"""
    
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
    
    def test_demo_runner_works(self):
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
        
        assert len(results) == 4
        for result in results:
            assert result["entries_extracted"] >= 0
