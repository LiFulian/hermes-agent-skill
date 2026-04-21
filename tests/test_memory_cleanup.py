"""Tests for memory cleanup module."""

import pytest
import tempfile
from pathlib import Path

from scripts.memory_cleanup import MemoryCleaner


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def cleaner(temp_memory_dir):
    return MemoryCleaner(temp_memory_dir)


@pytest.fixture
def sample_memory_file(temp_memory_dir):
    content = """# Agent Memory

## Project Context
- Building a web scraper
- Using Python and asyncio
- Deployment on AWS Lambda

## Learned Patterns
- Prefers asyncio over threading
- Prefers asyncio over threading
- Uses connection pooling

## Key Facts
- IDE: Cursor
- Testing: pytest


"""
    file_path = temp_memory_dir / "MEMORY.md"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def sample_user_file(temp_memory_dir):
    content = """# User Profile

## Preferences
- Language: Python
- IDE: Cursor

## Coding Style
- Type hints required
- Type hints required

"""
    file_path = temp_memory_dir / "USER.md"
    file_path.write_text(content)
    return file_path


class TestMemoryCleaner:
    def test_init(self, temp_memory_dir):
        cleaner = MemoryCleaner(temp_memory_dir)
        assert cleaner.memory_dir == temp_memory_dir
    
    def test_cleanup_removes_duplicates(self, temp_memory_dir, sample_memory_file, sample_user_file):
        cleaner = MemoryCleaner(temp_memory_dir)
        stats = cleaner.cleanup()
        assert stats["memory_removed"] > 0
        assert stats["user_removed"] > 0
    
    def test_cleanup_with_missing_files(self, temp_memory_dir):
        cleaner = MemoryCleaner(temp_memory_dir)
        stats = cleaner.cleanup()
        assert stats["memory_before"] == 0
        assert stats["user_before"] == 0
    
    def test_remove_empty_lines(self, cleaner):
        lines = ["line1", "", "", "line2", "", "line3"]
        result = cleaner._remove_empty_lines(lines)
        assert result == ["line1", "", "line2", "", "line3"]
    
    def test_remove_empty_lines_trailing(self, cleaner):
        lines = ["line1", "", ""]
        result = cleaner._remove_empty_lines(lines)
        assert result == ["line1"]
    
    def test_remove_duplicates(self, cleaner):
        lines = ["- Item 1", "- Item 2", "- Item 1", "- Item 3"]
        result = cleaner._remove_duplicates(lines)
        assert result.count("- Item 1") == 1
        assert len(result) == 3
    
    def test_normalize_whitespace(self, cleaner):
        lines = ["line1   ", "line2  ", "line3"]
        result = cleaner._normalize_whitespace(lines)
        assert all(line == line.rstrip() for line in result)
    
    def test_trim_to_limit(self, cleaner):
        lines = ["# Header"] + [f"- Item {i}" for i in range(100)]
        result = cleaner._trim_to_limit(lines, 200)
        assert len("\n".join(result)) <= 200
    
    def test_score_line_keywords(self, cleaner):
        line = "- User prefers Python for projects"
        score = cleaner._score_line(line)
        assert score > 0
    
    def test_score_line_length(self, cleaner):
        short_line = "- X"
        normal_line = "- This is a normal length line with good content"
        assert cleaner._score_line(normal_line) > cleaner._score_line(short_line)
    
    def test_cleanup_respects_memory_limit(self, temp_memory_dir):
        huge_content = "# Agent Memory\n\n## Project Context\n"
        huge_content += "- " + "x" * 3000 + "\n"
        
        memory_file = temp_memory_dir / "MEMORY.md"
        memory_file.write_text(huge_content)
        
        cleaner = MemoryCleaner(temp_memory_dir)
        cleaner.cleanup()
        
        content = memory_file.read_text()
        assert len(content) <= cleaner.MEMORY_MD_MAX_CHARS
    
    def test_cleanup_respects_user_limit(self, temp_memory_dir):
        huge_content = "# User Profile\n\n## Preferences\n"
        huge_content += "- " + "x" * 2000 + "\n"
        
        user_file = temp_memory_dir / "USER.md"
        user_file.write_text(huge_content)
        
        cleaner = MemoryCleaner(temp_memory_dir)
        cleaner.cleanup()
        
        content = user_file.read_text()
        assert len(content) <= cleaner.USER_MD_MAX_CHARS
