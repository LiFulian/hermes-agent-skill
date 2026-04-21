"""Show memory statistics command."""

from pathlib import Path


def show_stats(memory_dir: Path):
    if not memory_dir.exists():
        print(f"Memory directory not found: {memory_dir}")
        return
    
    memory_file = memory_dir / "MEMORY.md"
    user_file = memory_dir / "USER.md"
    
    print("Memory Statistics")
    print("=" * 60)
    
    if memory_file.exists():
        content = memory_file.read_text()
        lines = content.split("\n")
        entries = [l for l in lines if l.strip().startswith("-")]
        sections = [l for l in lines if l.startswith("##")]
        
        print(f"MEMORY.md:")
        print(f"  Size: {len(content)} / 2200 characters")
        print(f"  Sections: {len(sections)}")
        print(f"  Entries: {len(entries)}")
        print(f"  Usage: {len(content) / 2200 * 100:.1f}%")
        print()
    else:
        print("MEMORY.md: Not found")
        print()
    
    if user_file.exists():
        content = user_file.read_text()
        lines = content.split("\n")
        entries = [l for l in lines if l.strip().startswith("-")]
        sections = [l for l in lines if l.startswith("##")]
        
        print(f"USER.md:")
        print(f"  Size: {len(content)} / 1500 characters")
        print(f"  Sections: {len(sections)}")
        print(f"  Entries: {len(entries)}")
        print(f"  Usage: {len(content) / 1500 * 100:.1f}%")
        print()
    else:
        print("USER.md: Not found")
        print()
