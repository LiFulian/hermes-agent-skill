"""
Memory cleanup module - Cleans, deduplicates, and optimizes memory files.
"""

import re
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime


class MemoryCleaner:
    MEMORY_MD_MAX_CHARS = 2200
    USER_MD_MAX_CHARS = 1500
    
    def __init__(self, memory_dir: Optional[Path] = None):
        if memory_dir is None:
            memory_dir = Path.home() / ".universal-memory"
        self.memory_dir = memory_dir
        self.memory_file = memory_dir / "MEMORY.md"
        self.user_file = memory_dir / "USER.md"
    
    def cleanup(self) -> Dict[str, int]:
        memory_stats = self._cleanup_file(self.memory_file, self.MEMORY_MD_MAX_CHARS)
        user_stats = self._cleanup_file(self.user_file, self.USER_MD_MAX_CHARS)
        
        return {
            "memory_before": memory_stats["before"],
            "memory_after": memory_stats["after"],
            "memory_removed": memory_stats["removed"],
            "user_before": user_stats["before"],
            "user_after": user_stats["after"],
            "user_removed": user_stats["removed"],
        }
    
    def _cleanup_file(self, file_path: Path, max_chars: int) -> Dict[str, int]:
        if not file_path.exists():
            return {"before": 0, "after": 0, "removed": 0}
        
        content = file_path.read_text()
        before_length = len(content)
        
        lines = content.split("\n")
        
        cleaned_lines = self._remove_empty_lines(lines)
        cleaned_lines = self._remove_duplicates(cleaned_lines)
        cleaned_lines = self._normalize_whitespace(cleaned_lines)
        cleaned_lines = self._truncate_long_lines(cleaned_lines, max_chars)
        
        total_length = len("\n".join(cleaned_lines))
        if total_length > max_chars:
            cleaned_lines = self._trim_to_limit(cleaned_lines, max_chars)
        
        cleaned_content = "\n".join(cleaned_lines)
        file_path.write_text(cleaned_content)
        
        return {
            "before": before_length,
            "after": len(cleaned_content),
            "removed": before_length - len(cleaned_content),
        }
    
    def _truncate_long_lines(self, lines: List[str], max_chars: int) -> List[str]:
        max_line_length = max_chars // 10
        return [line[:max_line_length] if len(line) > max_line_length else line for line in lines]
    
    def _remove_empty_lines(self, lines: List[str]) -> List[str]:
        cleaned = []
        prev_empty = False
        
        for line in lines:
            is_empty = line.strip() == ""
            if is_empty and prev_empty:
                continue
            cleaned.append(line)
            prev_empty = is_empty
        
        while cleaned and cleaned[-1].strip() == "":
            cleaned.pop()
        
        return cleaned
    
    def _remove_duplicates(self, lines: List[str]) -> List[str]:
        seen = set()
        result = []
        
        for line in lines:
            stripped = line.strip().lower()
            if stripped and stripped in seen:
                continue
            if stripped:
                seen.add(stripped)
            result.append(line)
        
        return result
    
    def _normalize_whitespace(self, lines: List[str]) -> List[str]:
        return [line.rstrip() for line in lines]
    
    def _trim_to_limit(self, lines: List[str], max_chars: int) -> List[str]:
        headers_to_keep = set()
        for line in lines:
            if line.startswith("## "):
                headers_to_keep.add(line.strip())
        
        content_lines = []
        current_header = None
        
        for line in lines:
            if line.startswith("## "):
                current_header = line.strip()
            elif line.startswith("# "):
                pass
            elif line.strip() and current_header:
                content_lines.append({
                    "header": current_header,
                    "line": line,
                    "importance": self._score_line(line),
                })
        
        content_lines.sort(key=lambda x: x["importance"], reverse=True)
        
        selected = []
        header_lines: Dict[str, List[str]] = {}
        for item in content_lines:
            if item["header"] not in header_lines:
                header_lines[item["header"]] = []
            header_lines[item["header"]].append(item["line"])
        
        for header in [l.strip() for l in lines if l.startswith("## ")]:
            if header in header_lines:
                selected.append(header)
                for line in header_lines[header]:
                    selected.append(line)
                selected.append("")
        
        result_lines = [lines[0]] if lines and lines[0].startswith("#") else []
        result_lines.extend(selected)
        
        while len("\n".join(result_lines)) > max_chars and len(result_lines) > 3:
            result_lines.pop()
        
        return result_lines
    
    def _score_line(self, line: str) -> float:
        score = 0.0
        if line.startswith("-"):
            score += 0.1
        length = len(line.strip())
        if 20 <= length <= 100:
            score += 0.3
        elif length > 100:
            score += 0.2
        keywords = [
            "prefer", "always", "never", "use", "build", "project",
            "deploy", "config", "important", "note",
        ]
        line_lower = line.lower()
        for keyword in keywords:
            if keyword in line_lower:
                score += 0.1
                break
        return score
