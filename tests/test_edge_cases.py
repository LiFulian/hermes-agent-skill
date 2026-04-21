"""Tests for edge cases in memory system."""

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


class TestEdgeCases:
    def test_extract_very_long_conversation(self, extractor):
        long_conversation = "Python " * 1000
        entries = extractor.extract_from_conversation(long_conversation)
        assert len(entries) > 0
    
    def test_memory_file_exactly_at_limit(self, extractor):
        max_chars = extractor.MEMORY_MD_MAX_CHARS
        long_entry = "x" * (max_chars - 50)  # Leave space for markdown formatting
        entry = MemoryEntry(long_entry, MemoryType.PROJECT_CONTEXT)
        extractor.merge_into_memory([entry])
        content = extractor.memory_file.read_text()
        assert len(content) <= max_chars
    
    def test_user_file_exactly_at_limit(self, extractor):
        max_chars = extractor.USER_MD_MAX_CHARS
        long_entry = "x" * (max_chars - 50)  # Leave space for markdown formatting
        entry = MemoryEntry(long_entry, MemoryType.USER_PREFERENCE)
        extractor.merge_into_memory([entry])
        content = extractor.user_file.read_text()
        assert len(content) <= max_chars
    
    def test_memory_file_over_limit(self, extractor):
        max_chars = extractor.MEMORY_MD_MAX_CHARS
        very_long_entry = "x" * (max_chars * 2)
        entry = MemoryEntry(very_long_entry, MemoryType.PROJECT_CONTEXT)
        extractor.merge_into_memory([entry])
        content = extractor.memory_file.read_text()
        assert len(content) <= max_chars
    
    def test_user_file_over_limit(self, extractor):
        max_chars = extractor.USER_MD_MAX_CHARS
        very_long_entry = "x" * (max_chars * 2)
        entry = MemoryEntry(very_long_entry, MemoryType.USER_PREFERENCE)
        extractor.merge_into_memory([entry])
        content = extractor.user_file.read_text()
        assert len(content) <= max_chars
    
    def test_empty_memory_files(self, temp_memory_dir):
        memory_file = temp_memory_dir / "MEMORY.md"
        user_file = temp_memory_dir / "USER.md"
        memory_file.write_text("")
        user_file.write_text("")
        
        extractor = MemoryExtractor(temp_memory_dir)
        assert extractor.memory_file.exists()
        assert extractor.user_file.exists()
    
    def test_corrupted_memory_files(self, temp_memory_dir):
        memory_file = temp_memory_dir / "MEMORY.md"
        user_file = temp_memory_dir / "USER.md"
        memory_file.write_text("corrupted content")
        user_file.write_text("corrupted content")
        
        extractor = MemoryExtractor(temp_memory_dir)
        entries = [MemoryEntry("Test", MemoryType.USER_PREFERENCE)]
        extractor.merge_into_memory(entries)
        assert extractor.memory_file.exists()
        assert extractor.user_file.exists()
    
    def test_extract_no_keywords(self, extractor):
        conversation = "Hello, how are you?"
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) == 0
    
    def test_extract_only_stopwords(self, extractor):
        conversation = "the and or but if when"
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) == 0
    
    def test_merge_empty_entries(self, extractor):
        stats = extractor.merge_into_memory([])
        assert stats["memory_entries_added"] == 0
        assert stats["user_entries_added"] == 0
    
    def test_memory_directory_not_writable(self, temp_memory_dir):
        temp_memory_dir.chmod(0o444)  # Read-only
        try:
            extractor = MemoryExtractor(temp_memory_dir)
            entries = [MemoryEntry("Test", MemoryType.USER_PREFERENCE)]
            stats = extractor.merge_into_memory(entries)
            # If it doesn't raise, check that no entries were added
            assert stats["memory_entries_added"] == 0
            assert stats["user_entries_added"] == 0
        except PermissionError:
            # Expected behavior - directory is read-only
            pass
    
    def test_extract_special_characters(self, extractor):
        conversation = "I use C++ & Java for $1000 projects"
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
    
    def test_extract_multiple_languages(self, extractor):
        conversation = "I use Python (Python) para desarrollo web (for web development)"
        entries = extractor.extract_from_conversation(conversation)
        assert len(entries) > 0
