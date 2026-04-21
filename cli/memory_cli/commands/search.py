"""Search memory command."""

from pathlib import Path


def _search_file(file_path: Path, query: str, file_name: str):
    results = []
    content = file_path.read_text()
    for line_num, line in enumerate(content.split("\n"), 1):
        if query in line.lower():
            results.append((file_name, line_num, line))
    return results


def search_memory(memory_dir: Path, query: str):
    if not memory_dir.exists():
        print(f"Memory directory not found: {memory_dir}")
        return
    
    query_lower = query.lower()
    results = []
    
    memory_file = memory_dir / "MEMORY.md"
    if memory_file.exists():
        results.extend(_search_file(memory_file, query_lower, "MEMORY.md"))
    
    user_file = memory_dir / "USER.md"
    if user_file.exists():
        results.extend(_search_file(user_file, query_lower, "USER.md"))
    
    if not results:
        print(f"No results found for: {query}")
        return
    
    print(f"Search results for: {query}")
    print("=" * 60)
    for file_name, line_num, line in results:
        print(f"[{file_name}:{line_num}] {line.strip()}")
