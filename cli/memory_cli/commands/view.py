"""View memory command."""

from pathlib import Path


def view_memory(memory_dir: Path, user_only: bool = False, memory_only: bool = False):
    if not memory_dir.exists():
        print(f"Memory directory not found: {memory_dir}")
        print("Run 'universal-memory save \"some info\"' to create memory files.")
        return
    
    if memory_only or not user_only:
        memory_file = memory_dir / "MEMORY.md"
        if memory_file.exists():
            print("=" * 60)
            print("MEMORY.md (Agent Memory)")
            print("=" * 60)
            print(memory_file.read_text())
            print()
        else:
            print("MEMORY.md not found")
            print()
    
    if user_only or not memory_only:
        user_file = memory_dir / "USER.md"
        if user_file.exists():
            print("=" * 60)
            print("USER.md (User Profile)")
            print("=" * 60)
            print(user_file.read_text())
            print()
        else:
            print("USER.md not found")
            print()
