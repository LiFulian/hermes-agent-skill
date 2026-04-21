"""Integration tests for full memory workflow."""

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


class TestFullWorkflow:
    def test_extract_and_merge_workflow(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = """
        User: I'm building a Python web scraper using asyncio.
        I prefer pytest for testing and Cursor as my IDE.
        I always use type hints in my code.
        
        Assistant: Great! I'll help you with that.
        
        User: The deployment target is AWS Lambda.
        """
        
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
        
        stats = extractor.merge_into_memory(entries)
        assert stats["memory_entries_added"] > 0 or stats["user_entries_added"] > 0
        
        assert temp_memory_dir.joinpath("MEMORY.md").exists()
        assert temp_memory_dir.joinpath("USER.md").exists()
    
    def test_extract_inject_workflow(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        conversation = "I prefer Python for all projects and I'm building a web app"
        entries = extractor.extract_from_conversation(conversation)
        extractor.merge_into_memory(entries)
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        
        assert "Persistent Memory Context" in injected
        assert "Python" in injected or "web app" in injected
    
    def test_extract_cleanup_inject_workflow(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        for i in range(5):
            conversation = f"Entry {i}: I prefer tool {i} for project {i}"
            entries = extractor.extract_from_conversation(conversation)
            extractor.merge_into_memory(entries)
        
        cleaner = MemoryCleaner(temp_memory_dir)
        stats = cleaner.cleanup()
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        
        assert "Persistent Memory Context" in injected
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        assert len(memory_content) <= extractor.MEMORY_MD_MAX_CHARS
        
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        assert len(user_content) <= extractor.USER_MD_MAX_CHARS
    
    def test_multiple_sessions_simulation(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        session_1 = "I prefer to use Python when building web scraping projects"
        entries_1 = extractor.extract_from_conversation(session_1)
        extractor.merge_into_memory(entries_1)
        
        session_2 = "I decided to use asyncio and aiohttp for the scraper"
        entries_2 = extractor.extract_from_conversation(session_2)
        extractor.merge_into_memory(entries_2)
        
        session_3 = "I prefer pytest for testing and want to deploy to AWS Lambda"
        entries_3 = extractor.extract_from_conversation(session_3)
        extractor.merge_into_memory(entries_3)
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        combined = memory_content + user_content
        assert "Python" in combined or "asyncio" in combined or "pytest" in combined
        
        summary = injector.get_memory_summary()
        assert "Memory:" in summary
        assert "User:" in summary
    
    def test_memory_respects_limits_after_multiple_updates(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        for i in range(20):
            conversation = f"""
            I prefer technique {i} for optimization.
            I'm working on project {i} which involves {i} components.
            Important fact {i}: the system handles {i} requests per second.
            """
            entries = extractor.extract_from_conversation(conversation)
            extractor.merge_into_memory(entries)
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        
        assert len(memory_content) <= extractor.MEMORY_MD_MAX_CHARS
        assert len(user_content) <= extractor.USER_MD_MAX_CHARS
    
    def test_cleanup_then_extract_workflow(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        for i in range(10):
            conversation = f"Entry {i}: some information about topic {i}"
            entries = extractor.extract_from_conversation(conversation)
            extractor.merge_into_memory(entries)
        
        cleaner = MemoryCleaner(temp_memory_dir)
        cleaner.cleanup()
        
        new_conversation = "I now prefer Rust for system programming"
        new_entries = extractor.extract_from_conversation(new_conversation)
        extractor.merge_into_memory(new_entries)
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        assert "Persistent Memory Context" in injected
    
    def test_empty_memory_workflow(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        injector = MemoryInjector(temp_memory_dir)
        
        entries = extractor.extract_from_conversation("")
        assert entries == []
        
        injector = MemoryInjector(temp_memory_dir)
        injected = injector.inject_memory()
        assert "Persistent Memory Context" in injected
    
    def test_deduplication_across_sessions(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        
        session_1 = "I prefer Python for web development"
        entries_1 = extractor.extract_from_conversation(session_1)
        extractor.merge_into_memory(entries_1)
        
        session_2 = "I prefer Python for web development and I like async programming"
        entries_2 = extractor.extract_from_conversation(session_2)
        extractor.merge_into_memory(entries_2)
        
        memory_content = temp_memory_dir.joinpath("MEMORY.md").read_text()
        user_content = temp_memory_dir.joinpath("USER.md").read_text()
        
        combined = memory_content + user_content
        count = combined.lower().count("prefer")
        assert count <= 3
