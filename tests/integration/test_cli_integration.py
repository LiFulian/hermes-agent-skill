"""Integration tests for CLI commands."""

import pytest
import tempfile
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def temp_memory_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def cli_path():
    """Get path to universal-memory CLI."""
    return Path(__file__).parent.parent.parent / "cli" / "memory_cli" / "main.py"


class TestCLIIntegration:
    def test_cli_view_command(self, temp_memory_dir, cli_path):
        """Test view command."""
        # Create test memory files
        memory_file = temp_memory_dir / "MEMORY.md"
        user_file = temp_memory_dir / "USER.md"
        
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Test project\n")
        user_file.write_text("# User Profile\n\n## Preferences\n- Test preference\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "view"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "MEMORY.md" in result.stdout
        assert "USER.md" in result.stdout
        assert "Test project" in result.stdout
        assert "Test preference" in result.stdout
    
    def test_cli_view_memory_only(self, temp_memory_dir, cli_path):
        """Test view memory only."""
        memory_file = temp_memory_dir / "MEMORY.md"
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Test project\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "view", "--memory"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "MEMORY.md" in result.stdout
        assert "Test project" in result.stdout
    
    def test_cli_view_user_only(self, temp_memory_dir, cli_path):
        """Test view user only."""
        user_file = temp_memory_dir / "USER.md"
        user_file.write_text("# User Profile\n\n## Preferences\n- Test preference\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "view", "--user"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "USER.md" in result.stdout
        assert "Test preference" in result.stdout
    
    def test_cli_search_command(self, temp_memory_dir, cli_path):
        """Test search command."""
        memory_file = temp_memory_dir / "MEMORY.md"
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Python project\n- Web scraper\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "search", "Python"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Python" in result.stdout
        assert "Search results" in result.stdout
    
    def test_cli_search_not_found(self, temp_memory_dir, cli_path):
        """Test search command with no results."""
        memory_file = temp_memory_dir / "MEMORY.md"
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Python project\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "search", "Java"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "No results" in result.stdout
    
    def test_cli_stats_command(self, temp_memory_dir, cli_path):
        """Test stats command."""
        memory_file = temp_memory_dir / "MEMORY.md"
        user_file = temp_memory_dir / "USER.md"
        
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- Test project\n")
        user_file.write_text("# User Profile\n\n## Preferences\n- Test preference\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "stats"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Memory Statistics" in result.stdout
        assert "MEMORY.md" in result.stdout
        assert "USER.md" in result.stdout
        assert "characters" in result.stdout
    
    def test_cli_save_command(self, temp_memory_dir, cli_path):
        """Test save command."""
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "save", "Test memory entry"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Saved" in result.stdout
        
        memory_file = temp_memory_dir / "MEMORY.md"
        assert memory_file.exists()
        content = memory_file.read_text()
        assert "Test memory entry" in content
    
    def test_cli_missing_directory(self, cli_path):
        """Test CLI with missing directory."""
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", "/nonexistent/directory", "view"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "not found" in result.stdout
    
    def test_cli_chinese_support(self, temp_memory_dir, cli_path):
        """Test CLI with Chinese content."""
        memory_file = temp_memory_dir / "MEMORY.md"
        memory_file.write_text("# Agent Memory\n\n## Project Context\n- 网页爬虫项目\n")
        
        result = subprocess.run(
            [sys.executable, str(cli_path), "--memory-dir", str(temp_memory_dir), "search", "爬虫"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "爬虫" in result.stdout
    
    def test_cli_help_command(self, cli_path):
        """Test help command."""
        result = subprocess.run(
            [sys.executable, str(cli_path), "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "usage" in result.stdout
        assert "Available commands" in result.stdout
        assert "options" in result.stdout
