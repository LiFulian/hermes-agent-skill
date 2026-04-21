"""
Memory injection module - Formats memory files for system prompt injection.
"""

from typing import Optional
from pathlib import Path


class MemoryInjector:
    INJECT_TEMPLATE = """
## Persistent Memory Context (Frozen Snapshot)

### Agent Memory (MEMORY.md)
{memory_content}

### User Profile (USER.md)
{user_content}

---
Memory Context End - Above information is frozen for this session.
"""
    
    def __init__(self, memory_dir: Optional[Path] = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".universal-memory"
        self.memory_dir = memory_dir
        self.memory_file = memory_dir / "MEMORY.md"
        self.user_file = memory_dir / "USER.md"
    
    def inject_memory(self) -> str:
        memory_content = self._read_file_safe(self.memory_file)
        user_content = self._read_file_safe(self.user_file)
        
        return self.INJECT_TEMPLATE.format(
            memory_content=memory_content,
            user_content=user_content
        )
    
    def inject_custom(self, template: Optional[str] = None) -> str:
        memory_content = self._read_file_safe(self.memory_file)
        user_content = self._read_file_safe(self.user_file)
        
        if template:
            return template.format(
                memory_content=memory_content,
                user_content=user_content
            )
        return self.inject_memory()
    
    def get_memory_summary(self) -> str:
        memory_content = self._read_file_safe(self.memory_file)
        user_content = self._read_file_safe(self.user_file)
        
        memory_lines = [l for l in memory_content.split("\n") if l.strip().startswith("-")]
        user_lines = [l for l in user_content.split("\n") if l.strip().startswith("-")]
        
        return f"Memory: {len(memory_lines)} entries, User: {len(user_lines)} entries"
    
    def _read_file_safe(self, file_path: Path) -> str:
        if file_path.exists():
            return file_path.read_text()
        return f"[Memory file not found: {file_path.name}]"
