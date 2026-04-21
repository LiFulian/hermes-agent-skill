"""Tests for memory injection module."""

import pytest
import tempfile
from pathlib import Path

from scripts.memory_inject import MemoryInjector


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def injector(temp_memory_dir):
    inj = MemoryInjector(temp_memory_dir)
    inj.memory_file.write_text("# Agent Memory\n\n## Project Context\n- Test project")
    inj.user_file.write_text("# User Profile\n\n## Preferences\n- Python")
    return inj


class TestMemoryInjector:
    def test_init_with_custom_dir(self, temp_memory_dir):
        injector = MemoryInjector(temp_memory_dir)
        assert injector.memory_dir == temp_memory_dir
    
    def test_inject_memory_with_existing_files(self, injector):
        result = injector.inject_memory()
        assert "## Persistent Memory Context" in result
        assert "Test project" in result
        assert "Python" in result
        assert "Memory Context End" in result
    
    def test_inject_memory_with_missing_files(self, temp_memory_dir):
        injector = MemoryInjector(temp_memory_dir / "nonexistent")
        result = injector.inject_memory()
        assert "not found" in result
    
    def test_inject_custom_template(self, injector):
        template = "Memory: {memory_content}\nUser: {user_content}"
        result = injector.inject_custom(template)
        assert "Memory:" in result
        assert "User:" in result
        assert "Test project" in result
    
    def test_get_memory_summary(self, injector):
        summary = injector.get_memory_summary()
        assert "Memory:" in summary
        assert "User:" in summary
        assert "entries" in summary
    
    def test_read_file_safe_existing_file(self, injector):
        content = injector._read_file_safe(injector.memory_file)
        assert "Agent Memory" in content
    
    def test_read_file_safe_missing_file(self, injector):
        content = injector._read_file_safe(Path("/nonexistent/file.md"))
        assert "not found" in content
    
    def test_inject_template_format(self, injector):
        result = injector.inject_memory()
        assert result.count("{") == 0
        assert result.count("}") == 0
    
    def test_inject_includes_both_files(self, injector):
        result = injector.inject_memory()
        assert "Agent Memory (MEMORY.md)" in result
        assert "User Profile (USER.md)" in result
