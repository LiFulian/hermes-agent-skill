"""Tests for memory extraction module."""

import pytest
import tempfile
from pathlib import Path

from scripts.memory_extract import MemoryExtractor, MemoryEntry, MemoryType


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def extractor(temp_memory_dir):
    return MemoryExtractor(temp_memory_dir)


class TestMemoryExtractor:
    def test_init_creates_directory(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        assert extractor.memory_dir.exists()
    
    def test_init_creates_default_memory_file(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        assert extractor.memory_file.exists()
        assert extractor.user_file.exists()
    
    def test_default_memory_has_correct_format(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        content = extractor.memory_file.read_text()
        assert "# Agent Memory" in content
        assert "## Project Context" in content
        assert "## Learned Patterns" in content
        assert "## Key Facts" in content
        assert "## Active Tasks" in content
    
    def test_default_user_has_correct_format(self, temp_memory_dir):
        extractor = MemoryExtractor(temp_memory_dir)
        content = extractor.user_file.read_text()
        assert "# User Profile" in content
        assert "## Preferences" in content
        assert "## Projects" in content
        assert "## Coding Style" in content
        assert "## Important Notes" in content
    
    def test_extract_preferences_simple(self, extractor):
        conversation = "I prefer to use Python for all my projects when building web apps"
        entries = extractor.extract_from_conversation(conversation)
        preference_entries = [e for e in entries if e.memory_type == MemoryType.USER_PREFERENCE]
        assert len(preference_entries) > 0
    
    def test_extract_project_context(self, extractor):
        conversation = "I'm building a Python web scraper using asyncio and aiohttp for data collection"
        entries = extractor.extract_from_conversation(conversation)
        project_entries = [e for e in entries if e.memory_type == MemoryType.PROJECT_CONTEXT]
        assert len(project_entries) > 0
    
    def test_extract_learned_patterns(self, extractor):
        conversation = "The solution that worked well was using connection pooling for better performance"
        entries = extractor.extract_from_conversation(conversation)
        pattern_entries = [e for e in entries if e.memory_type == MemoryType.LEARNED_PATTERN]
        assert len(pattern_entries) > 0
    
    def test_extract_important_facts(self, extractor):
        conversation = "Important: the deployment target is AWS Lambda with a 15 minute timeout"
        entries = extractor.extract_from_conversation(conversation)
        fact_entries = [e for e in entries if e.memory_type == MemoryType.IMPORTANT_FACT]
        assert len(fact_entries) > 0
    
    def test_extract_coding_style(self, extractor):
        conversation = "I prefer to use type hints and async/await patterns in all Python code"
        entries = extractor.extract_from_conversation(conversation)
        style_entries = [e for e in entries if e.memory_type == MemoryType.CODING_STYLE]
        assert len(style_entries) > 0
    
    def test_deduplicate_entries(self, extractor):
        conversation = "I prefer Python. I prefer Python for development."
        entries = extractor.extract_from_conversation(conversation)
        unique_entries = extractor._deduplicate_entries(entries)
        contents = [e.content.lower() for e in unique_entries]
        assert len(contents) == len(set(contents))
    
    def test_extract_empty_conversation(self, extractor):
        entries = extractor.extract_from_conversation("")
        assert entries == []
    
    def test_extract_chinese_preferences(self, extractor):
        conversation = "我喜欢用Python开发后端，偏好使用FastAPI框架"
        entries = extractor.extract_from_conversation(conversation)
        preference_entries = [e for e in entries if e.memory_type == MemoryType.USER_PREFERENCE]
        assert len(preference_entries) > 0
        assert any("Python" in e.content for e in preference_entries)
        assert any("FastAPI" in e.content for e in preference_entries)
    
    def test_extract_chinese_project_context(self, extractor):
        conversation = "我正在开发一个网页爬虫，使用Python和asyncio"
        entries = extractor.extract_from_conversation(conversation)
        project_entries = [e for e in entries if e.memory_type == MemoryType.PROJECT_CONTEXT]
        assert len(project_entries) > 0
    
    def test_extract_chinese_important_facts(self, extractor):
        conversation = "重要：部署目标是AWS Lambda，超时时间是15分钟"
        entries = extractor.extract_from_conversation(conversation)
        fact_entries = [e for e in entries if e.memory_type == MemoryType.IMPORTANT_FACT]
        assert len(fact_entries) > 0
    
    def test_extract_mixed_language(self, extractor):
        conversation = "I use Python for 网页爬虫 development，需要使用asyncio"
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
    
    def test_merge_into_memory(self, extractor):
        entries = [
            MemoryEntry("Prefers Python", MemoryType.USER_PREFERENCE),
            MemoryEntry("Building web scraper", MemoryType.PROJECT_CONTEXT),
        ]
        stats = extractor.merge_into_memory(entries)
        assert stats["memory_entries_added"] == 1
        assert stats["user_entries_added"] == 1
        assert stats["memory_length"] > 0
        assert stats["user_length"] > 0
    
    def test_memory_file_respects_char_limit(self, extractor):
        many_entries = [
            MemoryEntry(f"Entry {i}: " + "x" * 100, MemoryType.PROJECT_CONTEXT)
            for i in range(30)
        ]
        extractor.merge_into_memory(many_entries)
        content = extractor.memory_file.read_text()
        assert len(content) <= extractor.MEMORY_MD_MAX_CHARS
    
    def test_user_file_respects_char_limit(self, extractor):
        many_entries = [
            MemoryEntry(f"Pref {i}: " + "x" * 100, MemoryType.USER_PREFERENCE)
            for i in range(20)
        ]
        extractor.merge_into_memory(many_entries)
        content = extractor.user_file.read_text()
        assert len(content) <= extractor.USER_MD_MAX_CHARS


class TestMemoryEntry:
    def test_to_markdown(self):
        entry = MemoryEntry("Test content", MemoryType.USER_PREFERENCE)
        assert entry.to_markdown() == "- Test content"
    
    def test_entry_with_importance(self):
        entry = MemoryEntry("Important", MemoryType.IMPORTANT_FACT, importance=0.9)
        assert entry.importance == 0.9
        assert entry.memory_type == MemoryType.IMPORTANT_FACT


class TestMemoryType:
    def test_all_types_exist(self):
        assert MemoryType.USER_PREFERENCE.value == "user_preference"
        assert MemoryType.PROJECT_CONTEXT.value == "project_context"
        assert MemoryType.LEARNED_PATTERN.value == "learned_pattern"
        assert MemoryType.IMPORTANT_FACT.value == "important_fact"
        assert MemoryType.CODING_STYLE.value == "coding_style"
        assert MemoryType.ACTIVE_TASK.value == "active_task"
