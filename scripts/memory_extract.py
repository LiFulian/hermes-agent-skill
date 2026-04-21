"""
Memory extraction module - Extracts important information from conversations
and converts it to structured memory entries.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class MemoryType(Enum):
    USER_PREFERENCE = "user_preference"
    PROJECT_CONTEXT = "project_context"
    LEARNED_PATTERN = "learned_pattern"
    IMPORTANT_FACT = "important_fact"
    CODING_STYLE = "coding_style"
    ACTIVE_TASK = "active_task"


@dataclass
class MemoryEntry:
    content: str
    memory_type: MemoryType
    importance: float = 0.5
    timestamp: Optional[str] = None
    
    def to_markdown(self) -> str:
        return f"- {self.content}"


class MemoryExtractor:
    MEMORY_MD_MAX_CHARS = 2200
    USER_MD_MAX_CHARS = 1500
    
    def __init__(self, memory_dir: Optional[Path] = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".universal-memory"
        self.memory_dir = memory_dir
        self.memory_file = memory_dir / "MEMORY.md"
        self.user_file = memory_dir / "USER.md"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        if not self.memory_file.exists():
            self._create_default_memory()
        if not self.user_file.exists():
            self._create_default_user()
    
    def _create_default_memory(self):
        default = """# Agent Memory

## Project Context

## Learned Patterns

## Key Facts

## Active Tasks
"""
        self.memory_file.write_text(default)
    
    def _create_default_user(self):
        default = """# User Profile

## Preferences

## Projects

## Coding Style

## Important Notes
"""
        self.user_file.write_text(default)
    
    def extract_from_conversation(self, conversation: str) -> List[MemoryEntry]:
        entries = []
        entries.extend(self._extract_preferences(conversation))
        entries.extend(self._extract_project_context(conversation))
        entries.extend(self._extract_learned_patterns(conversation))
        entries.extend(self._extract_important_facts(conversation))
        entries.extend(self._extract_coding_style(conversation))
        entries = self._deduplicate_entries(entries)
        return entries
    
    def _extract_preferences(self, text: str) -> List[MemoryEntry]:
        entries = []
        patterns = [
            r'(?:I|I\s+prefer|prefer)\s+(?:to\s+)?(?:use\s+)?(.{10,100})(?:for|when|instead|rather)',
            r'(?:my\s+)?(?:preferred|favorite)\s+(\w+)\s+(?:is|are)\s+(.{10,100})',
            r'(?:I|I\s+always|I\s+usually)\s+(.{20,100})(?:when|if|for)',
            r'(?:用|使用|喜欢|偏好|通常)\s*\S+',
            r'(?:Python|FastAPI|React|JavaScript|TypeScript|Rust|Go|pytest)',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                entry_text = match.group(0).strip()
                if len(entry_text) > 3:
                    entries.append(MemoryEntry(
                        content=entry_text,
                        memory_type=MemoryType.USER_PREFERENCE,
                        importance=0.7
                    ))
        return entries

    def _extract_project_context(self, text: str) -> List[MemoryEntry]:
        entries = []
        patterns = [
            r'(?:building|working on|creating|developing|开发|创建|构建|工作).{5,150}',
            r'(?:project|app|tool|项目|产品).{5,150}',
            r'(?:using|built with|tech stack|使用|技术栈).{5,150}(?:Python|React|JavaScript|TypeScript|Rust|Go|Python|React|JavaScript|TypeScript|Rust|Go)',
            r'(?:项目|产品|团队|会议).{5,100}',
            r'(?:创建|设置|添加|安排).{5,80}(?:会议|待办|日程|提醒)',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                entry_text = match.group(0).strip()
                if len(entry_text) > 3:
                    entries.append(MemoryEntry(
                        content=entry_text,
                        memory_type=MemoryType.PROJECT_CONTEXT,
                        importance=0.6
                    ))
        return entries
    
    def _extract_learned_patterns(self, text: str) -> List[MemoryEntry]:
        entries = []
        patterns = [
            r'(?:solution|approach|method)\s+(?:that\s+)?(?:worked|successful).{20,150}',
            r'(?:avoid|don.t|never|shouldn.t).{10,100}(?:because|since|as)',
            r'(?:流程|习惯|模式).{10,80}',
            r'(?:通常|习惯).{10,60}(?:下午|上午|周)',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                entry_text = match.group(0).strip()
                if len(entry_text) > 5:
                    entries.append(MemoryEntry(
                        content=entry_text,
                        memory_type=MemoryType.LEARNED_PATTERN,
                        importance=0.5
                    ))
        return entries
    
    def _extract_important_facts(self, text: str) -> List[MemoryEntry]:
        entries = []
        patterns = [
            r'(?:remember|note|important|重要).{20,150}',
            r'(?:deploy|server|environment|config).{20,100}',
            r'(?:Google|日历|提醒|周报|例会).{5,80}',
            r'(?:每[周月天]|周五|周一|周三|周四|周二).{5,60}',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                entry_text = match.group(0).strip()
                if len(entry_text) > 5:
                    entries.append(MemoryEntry(
                        content=entry_text,
                        memory_type=MemoryType.IMPORTANT_FACT,
                        importance=0.4
                    ))
        return entries
    
    def _extract_coding_style(self, text: str) -> List[MemoryEntry]:
        entries = []
        patterns = [
            r'(?:prefer|like|want).{10,100}(?:type hint|typing|annotation)',
            r'(?:prefer|like|want).{10,100}(?:async|await|asyncio)',
            r'(?:style|convention|format).{20,100}',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entry_text = match.group(0).strip()
                if len(entry_text) > 15:
                    entries.append(MemoryEntry(
                        content=entry_text,
                        memory_type=MemoryType.CODING_STYLE,
                        importance=0.6
                    ))
        return entries
    
    def _deduplicate_entries(self, entries: List[MemoryEntry]) -> List[MemoryEntry]:
        seen = set()
        unique = []
        for entry in entries:
            key = entry.content.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(entry)
        return unique
    
    def merge_into_memory(self, new_entries: List[MemoryEntry]) -> Dict[str, int]:
        existing_memory = self.memory_file.read_text()
        existing_user = self.user_file.read_text()
        
        memory_entries = []
        user_entries = []
        
        for entry in new_entries:
            if entry.memory_type in [MemoryType.USER_PREFERENCE, MemoryType.CODING_STYLE]:
                user_entries.append(entry)
            else:
                memory_entries.append(entry)
        
        memory_updated = self._update_file(
            existing_memory, memory_entries, self.MEMORY_MD_MAX_CHARS
        )
        user_updated = self._update_file(
            existing_user, user_entries, self.USER_MD_MAX_CHARS
        )
        
        self.memory_file.write_text(memory_updated)
        self.user_file.write_text(user_updated)
        
        return {
            "memory_entries_added": len(memory_entries),
            "user_entries_added": len(user_entries),
            "memory_length": len(memory_updated),
            "user_length": len(user_updated),
        }
    
    def _update_file(self, existing: str, new_entries: List[MemoryEntry], max_chars: int) -> str:
        lines = existing.split("\n")
        current_section = "## Other"
        sections = {}
        
        for line in lines:
            if line.startswith("## "):
                current_section = line.strip()
                if current_section not in sections:
                    sections[current_section] = []
            else:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line)
        
        type_to_section = {
            MemoryType.PROJECT_CONTEXT: "## Project Context",
            MemoryType.LEARNED_PATTERN: "## Learned Patterns",
            MemoryType.IMPORTANT_FACT: "## Key Facts",
            MemoryType.ACTIVE_TASK: "## Active Tasks",
            MemoryType.USER_PREFERENCE: "## Preferences",
            MemoryType.CODING_STYLE: "## Coding Style",
        }
        
        for entry in new_entries:
            section = type_to_section.get(entry.memory_type, "## Other")
            entry_text = entry.to_markdown()
            if entry_text not in sections.get(section, []):
                if section not in sections:
                    sections[section] = []
                sections[section].append(entry_text)
        
        result_lines = []
        for line in lines:
            if line.startswith("# "):
                result_lines.append(line)
            elif line.startswith("## "):
                section = line.strip()
                result_lines.append(section)
                if section in sections:
                    entries = sections[section]
                    while entries and entries[0].strip() == "":
                        entries.pop(0)
                    for entry_line in entries:
                        result_lines.append(entry_line)
                    del sections[section]
        
        # Check length and trim if needed
        result_text = "\n".join(result_lines)
        if len(result_text) > max_chars:
            result_text = self._trim_to_limit_text(result_text, max_chars)
        
        return result_text
    
    def _trim_to_limit_text(self, text: str, max_chars: int) -> str:
        """Trim text to stay within character limit."""
        if len(text) <= max_chars:
            return text
        
        # First try to trim by lines
        lines = text.split("\n")
        result_lines = []
        current_length = 0
        
        for line in lines:
            line_length = len(line) + 1  # +1 for newline
            if current_length + line_length <= max_chars:
                result_lines.append(line)
                current_length += line_length
            else:
                # If this line would exceed, truncate it
                remaining = max_chars - current_length
                if remaining > 0:
                    truncated_line = line[:remaining]
                    result_lines.append(truncated_line)
                break
        
        # Ensure we have at least the basic structure
        if len(result_lines) < 10:
            result_lines = lines[:10]
        
        result = "\n".join(result_lines)
        
        # Final check - if still over, truncate the entire text
        if len(result) > max_chars:
            result = result[:max_chars]
        
        return result
    
    def _trim_to_limit(self, lines: List[str], max_chars: int) -> List[str]:
        """Trim lines to stay within character limit."""
        result = []
        current_length = 0
        
        for line in lines:
            line_length = len(line) + 1  # +1 for newline
            if current_length + line_length <= max_chars:
                result.append(line)
                current_length += line_length
            else:
                # If adding this line would exceed the limit, break
                break
        
        # Ensure we have at least the basic structure
        if len(result) < 10:
            result = lines[:10]
            
        return result
