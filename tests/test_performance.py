"""Performance tests for memory system."""

import pytest
import tempfile
import time
from pathlib import Path

from scripts.memory_extract import MemoryExtractor, MemoryEntry, MemoryType


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def extractor(temp_memory_dir):
    return MemoryExtractor(temp_memory_dir)


class TestPerformance:
    def test_extract_speed(self, extractor):
        """Test that extraction is fast enough for real-time use."""
        conversation = "I use Python for web development with FastAPI and pytest. " * 10
        start_time = time.time()
        entries = extractor.extract_from_conversation(conversation)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 1.0, f"Extraction took {duration:.2f}s, should be < 1s"
        assert len(entries) > 0
    
    def test_merge_speed(self, extractor):
        """Test that memory merging is fast enough."""
        entries = [
            MemoryEntry(f"Entry {i}", MemoryType.PROJECT_CONTEXT)
            for i in range(50)
        ]
        start_time = time.time()
        stats = extractor.merge_into_memory(entries)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 1.0, f"Merging took {duration:.2f}s, should be < 1s"
        assert stats["memory_entries_added"] == 50
        assert stats["user_entries_added"] == 0
    
    def test_extract_large_conversation(self, extractor):
        """Test extraction with large conversation."""
        large_conversation = "I use Python. " * 1000
        start_time = time.time()
        entries = extractor.extract_from_conversation(large_conversation)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 2.0, f"Extraction took {duration:.2f}s, should be < 2s"
        assert len(entries) > 0
    
    def test_merge_large_entries(self, extractor):
        """Test merging with large number of entries."""
        entries = [
            MemoryEntry(f"Entry {i}: " + "x" * 100, MemoryType.PROJECT_CONTEXT)
            for i in range(100)
        ]
        start_time = time.time()
        stats = extractor.merge_into_memory(entries)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 2.0, f"Merging took {duration:.2f}s, should be < 2s"
        assert stats["memory_entries_added"] == 100
        assert stats["user_entries_added"] == 0
    
    def test_memory_file_read_write_speed(self, extractor):
        """Test memory file read/write speed."""
        # Write test
        entries = [MemoryEntry("Test content" * 10, MemoryType.USER_PREFERENCE)]
        start_time = time.time()
        extractor.merge_into_memory(entries)
        end_time = time.time()
        write_duration = end_time - start_time
        assert write_duration < 0.5, f"Write took {write_duration:.2f}s, should be < 0.5s"
        
        # Read test
        start_time = time.time()
        content = extractor.memory_file.read_text()
        end_time = time.time()
        read_duration = end_time - start_time
        assert read_duration < 0.1, f"Read took {read_duration:.2f}s, should be < 0.1s"
        assert len(content) > 0
    
    def test_deduplication_performance(self, extractor):
        """Test deduplication performance."""
        # Create duplicate entries
        entries = []
        for i in range(100):
            entries.append(MemoryEntry("Python", MemoryType.USER_PREFERENCE))
            entries.append(MemoryEntry("FastAPI", MemoryType.USER_PREFERENCE))
        
        start_time = time.time()
        unique_entries = extractor._deduplicate_entries(entries)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 0.5, f"Deduplication took {duration:.2f}s, should be < 0.5s"
        assert len(unique_entries) == 2  # Only 2 unique entries
