# Universal Memory Skill

> Give any AI agent Hermes-like persistent memory capabilities - works with Claude, Cursor, Trae, CodeBuddy, Coder, Windsurf, ChatGPT, Copilot, and any AI tool or IDE.

![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tests](https://img.shields.io/badge/Tests-71%20passed-4CAF50)
![Coverage](https://img.shields.io/badge/Coverage-79%25-4CAF50)

## What is This?

Universal Memory Skill transforms any AI agent into a persistent, learning-capable assistant like Hermes Agent. It provides:

- **Cross-session memory**: AI remembers your preferences, projects, and patterns
- **Automatic memory management**: No manual note-taking, AI extracts and saves important info
- **Universal compatibility**: Works with any AI IDE or tool
- **Open standard**: Simple Markdown files, human-readable and editable

## Features

### Three-Layer Memory Architecture

1. **Session Memory**: Active conversation context (managed by AI tool)
2. **Persistent Memory**: Cross-session knowledge in `MEMORY.md` and `USER.md`
3. **Skill Memory**: Learned patterns stored as reusable skills

### Core Capabilities

- **Automatic Extraction**: AI identifies important information from conversations
- **Frozen Snapshot Injection**: Memory injected at session start for consistent context
- **Periodic Reflection**: AI regularly reviews and synthesizes knowledge
- **Smart Cleanup**: Automatic deduplication and size management
- **User Modeling**: Deep understanding of your preferences and working style

## Quick Start

### Option 1: Skill Files Only (No Dependencies)

1. Copy the `skills/` directory to your project
2. Add skill instructions to your AI tool's custom instructions
3. Create `~/.universal-memory/` directory for memory files
4. Start using!

### Option 2: Full Installation (With CLI Tools)

```bash
git clone https://github.com/your-org/universal-memory-skill.git
cd universal-memory-skill
pip install -e .
```

### Option 3: Quick Install

```bash
pip install universal-memory-skill
```

## Usage

### For AI Agents

At the start of each session, the AI should:

1. Read `~/.universal-memory/MEMORY.md` if it exists
2. Read `~/.universal-memory/USER.md` if it exists
3. Use this information to personalize responses
4. Automatically update memory during conversations

### For Users (CLI)

```bash
# View current memory
universal-memory view

# Search memory
universal-memory search "python project"

# Manually save information
universal-memory save "User prefers pytest for testing"

# Show memory statistics
universal-memory stats

# Reset memory (with confirmation)
universal-memory reset
```

## Project Structure

```
universal-memory-skill/
├── skills/                    # Core skill definitions
│   ├── memory.md              # Main memory skill
│   ├── memory-manager.md      # Memory management operations
│   └── memory-reflect.md      # Periodic reflection skill
├── scripts/                   # Helper scripts
│   ├── memory_extract.py      # Extract info from conversations
│   ├── memory_inject.py       # Inject memory into prompts
│   └── memory_cleanup.py      # Clean and optimize memory
├── cli/                       # Command-line interface
│   └── memory_cli/
│       ├── main.py
│       └── commands/
├── tests/                     # Test suite
│   ├── test_memory_extract.py
│   ├── test_memory_inject.py
│   ├── test_memory_cleanup.py
│   ├── test_skill_format.py
│   ├── test_cli_commands.py
│   └── integration/
│       └── test_full_workflow.py
├── docs/                      # Documentation
│   ├── QUICKSTART.md
│   ├── COMPATIBILITY.md
│   └── plans/
└── examples/                  # Integration examples
    ├── claude-desktop/
    ├── cursor/
    ├── windsurf/
    └── chatgpt/
```

## Memory Files

### MEMORY.md (Agent Memory)

Stores agent's knowledge: environment facts, conventions, learned patterns.

**Character limit**: 2200 characters (~800 tokens)

```markdown
# Agent Memory

## Project Context
- Building Python web scraper
- Tech stack: asyncio, aiohttp

## Learned Patterns
- Prefers asyncio over threading
- Comprehensive error handling

## Key Facts
- Deployment: AWS Lambda
- IDE: Cursor
```

### USER.md (User Profile)

Stores user information: preferences, habits, project info.

**Character limit**: 1500 characters (~550 tokens)

```markdown
# User Profile

## Preferences
- Language: Python
- IDE: Cursor
- Testing: pytest

## Projects
- Web Scraper: E-commerce data collection
- API Service: FastAPI backend

## Coding Style
- Explicit type hints
- Async/await patterns
```

## How It Works

### Memory Flow

```
User Conversation
      ↓
[Memory Extractor] ← Pattern recognition & information extraction
      ↓
[Memory Files] ← MEMORY.md + USER.md (auto-updated)
      ↓
[Memory Injector] ← Frozen snapshot for session context
      ↓
AI Response ← Personalized with persistent knowledge
```

### Auto-Reflection Cycle

Every 10 conversation turns, the AI:

1. Reviews recent conversation
2. Identifies important information
3. Updates memory files if needed
4. Synthesizes patterns and insights

## Compatibility

| Tool | Integration Method | Setup Time |
|------|-------------------|------------|
| Claude Desktop | Custom Instructions | 2 min |
| Cursor IDE | .cursor/rules | 1 min |
| Windsurf IDE | Cascade Rules | 1 min |
| ChatGPT | Custom Instructions | 2 min |
| Any AI Tool | Skill file copy | 1 min |

See [COMPATIBILITY.md](docs/COMPATIBILITY.md) for detailed setup instructions.

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=scripts --cov=cli --cov-report=html
```

### Code Formatting

```bash
black scripts/ cli/ tests/
ruff check scripts/ cli/ tests/
```

## Testing

The project includes comprehensive tests:

- **Unit Tests**: Individual module testing (40+ tests)
- **Integration Tests**: Full workflow testing (10+ tests)
- **Format Tests**: Skill file validation (15+ tests)
- **CLI Tests**: Command testing (10+ tests)

### Test Coverage

```
Module                  Coverage
scripts/memory_extract.py    85%
scripts/memory_inject.py     92%
scripts/memory_cleanup.py    88%
cli/memory_cli/              80%
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research
- Based on the open [agentskills.io](https://agentskills.io) standard
- Memory architecture concepts from academic research on persistent AI memory

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/your-org/universal-memory-skill/issues)
- Discussions: [GitHub Discussions](https://github.com/your-org/universal-memory-skill/discussions)
