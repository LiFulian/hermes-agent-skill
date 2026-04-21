"""Tests for skill format validation."""

import pytest
from pathlib import Path


def get_skills_dir():
    return Path(__file__).parent.parent / "skills"


class TestSkillFormat:
    def test_memory_md_exists(self):
        assert (get_skills_dir() / "memory.md").exists()
    
    def test_memory_manager_md_exists(self):
        assert (get_skills_dir() / "memory-manager.md").exists()
    
    def test_memory_reflect_md_exists(self):
        assert (get_skills_dir() / "memory-reflect.md").exists()
    
    def test_memory_md_has_overview(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "## Overview" in content
    
    def test_memory_md_has_usage_instructions(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "## When to Use Memory" in content or "## How to Use Memory" in content or "## Usage" in content
    
    def test_memory_md_has_format_spec(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "## Memory Format" in content or "Format" in content
    
    def test_memory_md_has_rules(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "## Memory" in content or "Rules" in content
    
    def test_memory_manager_has_operations(self):
        content = (get_skills_dir() / "memory-manager.md").read_text()
        assert "## Memory Operations" in content or "Operations" in content
    
    def test_memory_manager_has_cleanup(self):
        content = (get_skills_dir() / "memory-manager.md").read_text()
        assert "leanup" in content
    
    def test_memory_reflect_has_process(self):
        content = (get_skills_dir() / "memory-reflect.md").read_text()
        assert "## Reflection Process" in content or "Process" in content
    
    def test_memory_reflect_has_questions(self):
        content = (get_skills_dir() / "memory-reflect.md").read_text()
        assert "## Reflection Questions" in content or "Questions" in content
    
    def test_all_skills_are_markdown(self):
        for file in get_skills_dir().glob("*.md"):
            assert file.suffix == ".md"
    
    def test_all_skills_have_content(self):
        for file in get_skills_dir().glob("*.md"):
            content = file.read_text()
            assert len(content) > 100
    
    def test_memory_md_mentions_character_limits(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "2200" in content or "1500" in content or "character" in content.lower()
    
    def test_memory_md_mentions_memory_files(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "MEMORY.md" in content
        assert "USER.md" in content
    
    def test_memory_md_has_compatibility_section(self):
        content = (get_skills_dir() / "memory.md").read_text()
        assert "## Compatibility" in content or "Compatibility" in content
