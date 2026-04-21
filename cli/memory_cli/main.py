"""Memory CLI - Command line interface for universal memory skill."""

import argparse
import sys
from pathlib import Path

from cli.memory_cli.commands.view import view_memory
from cli.memory_cli.commands.search import search_memory
from cli.memory_cli.commands.stats import show_stats


def main():
    parser = argparse.ArgumentParser(
        description="Universal Memory CLI - Manage persistent memory for AI agents"
    )
    parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path.home() / ".universal-memory",
        help="Directory for memory files (default: ~/.universal-memory)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    view_parser = subparsers.add_parser("view", help="View current memory files")
    view_parser.add_argument("--user", action="store_true", help="Show only USER.md")
    view_parser.add_argument("--memory", action="store_true", help="Show only MEMORY.md")
    
    search_parser = subparsers.add_parser("search", help="Search memory files")
    search_parser.add_argument("query", help="Search query")
    
    stats_parser = subparsers.add_parser("stats", help="Show memory statistics")
    
    save_parser = subparsers.add_parser("save", help="Save information to memory")
    save_parser.add_argument("info", help="Information to save")
    save_parser.add_argument("--type", choices=["memory", "user"], default="memory",
                            help="Which file to save to")
    
    reset_parser = subparsers.add_parser("reset", help="Reset memory files")
    reset_parser.add_argument("--confirm", action="store_true", help="Skip confirmation")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    memory_dir = args.memory_dir
    
    if args.command == "view":
        view_memory(memory_dir, user_only=args.user, memory_only=args.memory)
    elif args.command == "search":
        search_memory(memory_dir, args.query)
    elif args.command == "stats":
        show_stats(memory_dir)
    elif args.command == "save":
        save_to_memory(memory_dir, args.info, args.type)
    elif args.command == "reset":
        reset_memory(memory_dir, args.confirm)


def save_to_memory(memory_dir: Path, info: str, target: str):
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    if target == "memory":
        file_path = memory_dir / "MEMORY.md"
        if not file_path.exists():
            file_path.write_text("# Agent Memory\n\n## Added Entries\n")
        with open(file_path, "a") as f:
            f.write(f"- {info}\n")
        print(f"Saved to MEMORY.md")
    else:
        file_path = memory_dir / "USER.md"
        if not file_path.exists():
            file_path.write_text("# User Profile\n\n## Added Entries\n")
        with open(file_path, "a") as f:
            f.write(f"- {info}\n")
        print(f"Saved to USER.md")


def reset_memory(memory_dir: Path, confirmed: bool):
    if not confirmed:
        response = input("This will delete all memory files. Are you sure? (y/N): ")
        if response.lower() != "y":
            print("Cancelled.")
            return
    
    memory_file = memory_dir / "MEMORY.md"
    user_file = memory_dir / "USER.md"
    
    if memory_file.exists():
        memory_file.unlink()
        print("Deleted MEMORY.md")
    
    if user_file.exists():
        user_file.unlink()
        print("Deleted USER.md")
    
    print("Memory reset complete.")


if __name__ == "__main__":
    main()
