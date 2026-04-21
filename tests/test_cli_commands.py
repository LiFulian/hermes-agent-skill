"""Tests for CLI commands."""

import pytest
import tempfile
from pathlib import Path

from cli.memory_cli.commands.view import view_memory
from cli.memory_cli.commands.search import search_memory
from cli.memory_cli.commands.stats import show_stats


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        memory_file = Path(tmpdir) / "MEMORY.md"
        user_file = Path(tmpdir) / "USER.md"
        
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Building a web scraper\n- Using Python")
        user_file.write_text("# User Profile\n\n## Preferences\n- Python\n- IDE: Cursor")
        
        yield Path(tmpdir)


class TestViewCommand:
    def test_view_memory_both_files(self, temp_memory_dir, capsys):
        view_memory(temp_memory_dir)
        captured = capsys.readouterr()
        assert "MEMORY.md" in captured.out
        assert "USER.md" in captured.out
        assert "web scraper" in captured.out
        assert "Cursor" in captured.out
    
    def test_view_memory_only(self, temp_memory_dir, capsys):
        view_memory(temp_memory_dir, memory_only=True)
        captured = capsys.readouterr()
        assert "MEMORY.md" in captured.out
        assert "web scraper" in captured.out
    
    def test_view_user_only(self, temp_memory_dir, capsys):
        view_memory(temp_memory_dir, user_only=True)
        captured = capsys.readouterr()
        assert "USER.md" in captured.out
        assert "Cursor" in captured.out
    
    def test_view_missing_directory(self, capsys):
        view_memory(Path("/nonexistent"))
        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestSearchCommand:
    def test_search_found(self, temp_memory_dir, capsys):
        search_memory(temp_memory_dir, "Python")
        captured = capsys.readouterr()
        assert "Python" in captured.out
        assert "Search results" in captured.out
    
    def test_search_not_found(self, temp_memory_dir, capsys):
        search_memory(temp_memory_dir, "nonexistent_term_xyz")
        captured = capsys.readouterr()
        assert "No results" in captured.out
    
    def test_search_missing_directory(self, capsys):
        search_memory(Path("/nonexistent"), "test")
        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestStatsCommand:
    def test_show_stats(self, temp_memory_dir, capsys):
        show_stats(temp_memory_dir)
        captured = capsys.readouterr()
        assert "Memory Statistics" in captured.out
        assert "MEMORY.md" in captured.out
        assert "USER.md" in captured.out
        assert "characters" in captured.out
        assert "Entries" in captured.out
    
    def test_show_stats_missing(self, capsys):
        show_stats(Path("/nonexistent"))
        captured = capsys.readouterr()
        assert "not found" in captured.out
