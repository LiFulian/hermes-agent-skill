"""Integration tests for Chinese language support."""

import pytest
import tempfile
from pathlib import Path

from scripts.memory_extract import MemoryExtractor, MemoryEntry, MemoryType
from scripts.memory_inject import MemoryInjector
from scripts.memory_cleanup import MemoryCleaner


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestChineseWorkflow:
    def test_chinese_extract_and_merge_workflow(self, temp_memory_dir):
        """Test full workflow with Chinese language."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = """
        用户：我正在开发一个网页爬虫，使用Python和asyncio。
        我喜欢用pytest做测试，Cursor是我的IDE。
        我总是在代码中使用类型提示。
        
        助手：好的，我会帮你。
        
        用户：部署目标是AWS Lambda。
        """
        
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
        
        stats = extractor.merge_into_memory(entries)
        assert stats["memory_entries_added"] > 0 or stats["user_entries_added"] > 0
        
        assert temp_memory_dir.joinpath("MEMORY.md").exists()
        assert temp_memory_dir.joinpath("USER.md").exists()
    
    def test_chinese_inject_workflow(self, temp_memory_dir):
        """Test memory injection with Chinese content."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = "我喜欢用Python开发所有项目，正在做一个网页应用"
        entries = extractor.extract_from_conversation(conversation)
        extractor.merge_into_memory(entries)
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        
        assert "Persistent Memory Context" in injected
        assert "Python" in injected or "网页" in injected
    
    def test_mixed_language_workflow(self, temp_memory_dir):
        """Test workflow with mixed Chinese and English."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = """
        User: I'm building a 网页爬虫 using Python.
        我需要使用 asyncio 和 aiohttp。
        Assistant: Great! I'll help you with that.
        User: The 部署 target is AWS Lambda.
        """
        
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
        
        stats = extractor.merge_into_memory(entries)
        assert stats["memory_entries_added"] > 0 or stats["user_entries_added"] > 0
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        assert "Persistent Memory Context" in injected
    
    def test_chinese_multi_session_workflow(self, temp_memory_dir):
        """Test multiple Chinese sessions."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        session_1 = "我喜欢用Python开发网页爬虫"
        entries_1 = extractor.extract_from_conversation(session_1)
        extractor.merge_into_memory(entries_1)
        
        session_2 = "我决定使用asyncio和aiohttp来做爬虫"
        entries_2 = extractor.extract_from_conversation(session_2)
        extractor.merge_into_memory(entries_2)
        
        session_3 = "我喜欢用pytest做测试，想部署到AWS Lambda"
        entries_3 = extractor.extract_from_conversation(session_3)
        extractor.merge_into_memory(entries_3)
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        combined = memory_content + user_content
        assert "Python" in combined or "asyncio" in combined or "pytest" in combined
    
    def test_chinese_important_facts(self, temp_memory_dir):
        """Test extraction of important facts in Chinese."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = """
        重要：部署目标是AWS Lambda，超时时间是15分钟。
        记住：数据库连接需要使用连接池。
        注意：API密钥保存在环境变量中。
        """
        
        entries = extractor.extract_from_conversation(conversation)
        fact_entries = [e for e in entries if e.memory_type == MemoryType.IMPORTANT_FACT]
        assert len(fact_entries) > 0
        
        extractor.merge_into_memory(entries)
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        assert "重要" in memory_content or "记住" in memory_content or "注意" in memory_content
    
    def test_chinese_patterns(self, temp_memory_dir):
        """Test extraction of patterns in Chinese."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = """
        我通常在下午处理文档工作。
        每周一上午有团队会议。
        周五下午需要发送周报。
        """
        
        entries = extractor.extract_from_conversation(conversation)
        pattern_entries = [e for e in entries if e.memory_type == MemoryType.LEARNED_PATTERN]
        assert len(pattern_entries) > 0
        
        extractor.merge_into_memory(entries)
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        assert "下午" in memory_content or "周一" in memory_content or "周五" in memory_content
    
    def test_chinese_cleanup_workflow(self, temp_memory_dir):
        """Test cleanup with Chinese content."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        for i in range(10):
            conversation = f"条目{i}：关于主题{i}的一些信息"
            entries = extractor.extract_from_conversation(conversation)
            extractor.merge_into_memory(entries)
        
        cleaner = MemoryCleaner(temp_memory_dir)
        stats = cleaner.cleanup()
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        assert "Persistent Memory Context" in injected
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        assert len(memory_content) <= extractor.MEMORY_MD_MAX_CHARS
    
    def test_chinese_character_limits(self, temp_memory_dir):
        """Test character limits with Chinese content."""
        extractor = MemoryExtractor(temp_memory_dir)
        
        # Create very long Chinese content
        long_chinese = "我" * 1000
        conversation = f"重要信息：{long_chinese}"
        
        entries = extractor.extract_from_conversation(conversation)
        extractor.merge_into_memory(entries)
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        
        assert len(memory_content) <= extractor.MEMORY_MD_MAX_CHARS
        assert len(user_content) <= extractor.USER_MD_MAX_CHARS
