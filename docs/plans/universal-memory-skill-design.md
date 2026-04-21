# Universal Memory Skill - Architecture Design

## Project Goal

Create a universal, open-source memory skill that enables any AI agent (Claude, Cursor, Windsurf, ChatGPT, or any IDE/tool) to have Hermes Agent-like persistent memory capabilities.

## Core Architecture

### 1. File Structure

```
universal-memory-skill/
├── skills/
│   ├── memory.md                    # Core skill definition
│   ├── memory-manager.md            # Memory management operations
│   └── memory-reflect.md            # Periodic reflection skill
├── scripts/
│   ├── memory_extract.py            # Auto-extract important info from conversations
│   ├── memory_inject.py             # Inject memory into system prompt
│   └── memory_cleanup.py            # Clean and deduplicate memory
├── cli/
│   └── memory-cli/                  # Command-line interface
│       ├── __init__.py
│       ├── main.py
│       ├── commands/
│       │   ├── view.py              # View current memory
│       │   ├── search.py            # Search memory
│       │   └── stats.py             # Memory statistics
├── memory/
│   ├── MEMORY.md                    # Agent memory (auto-managed)
│   └── USER.md                      # User profile memory (auto-managed)
├── tests/
│   ├── test_memory_extract.py
│   ├── test_memory_inject.py
│   ├── test_memory_cleanup.py
│   ├── test_skill_format.py
│   └── integration/
│       └── test_full_workflow.py
├── docs/
│   ├── README.md                    # Main documentation
│   ├── ARCHITECTURE.md              # This file
│   ├── QUICKSTART.md                # Quick start guide
│   └── COMPATIBILITY.md             # Compatible tools list
├── examples/
│   ├── claude-desktop/
│   ├── cursor/
│   ├── windsurf/
│   └── chatgpt/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── setup.py
```

### 2. Memory Architecture (Three-Layer Design)

#### Layer 1: Session Memory
- Stored in conversation context
- Temporary, cleared when session ends
- Managed automatically by the AI agent

#### Layer 2: Persistent Memory (Core)
- **MEMORY.md** (2200 chars limit)
  - Agent's notes about environment, facts, conventions, learned knowledge
  - Format: Markdown with section headers
  - Auto-updated by AI agent during conversations
  
- **USER.md** (1500 chars limit)
  - User profile: preferences, habits, project info, coding style
  - Format: Markdown with structured fields
  - Auto-extracted from user interactions

#### Layer 3: Skill Memory
- Learned patterns stored as reusable skills
- Created from successful task completions
- Stored in `~/.universal-memory/skills/`

### 3. Core Skill Design (memory.md)

```markdown
# Memory Skill

## Overview
You have access to a persistent memory system. Use this skill to remember important
information across sessions and provide better assistance.

## Memory Location
Memory files are stored in: `~/.universal-memory/`
- MEMORY.md: Your persistent memory
- USER.md: User profile and preferences

## How to Use Memory

### Reading Memory
At the start of each session:
1. Check if `~/.universal-memory/MEMORY.md` exists
2. Check if `~/.universal-memory/USER.md` exists
3. Read both files if they exist
4. Use this information to personalize your responses

### Writing Memory
During conversations, identify important information worth remembering:
- User preferences (language, tools, coding style)
- Project context (tech stack, architecture decisions)
- Learned patterns (solutions that worked well)
- Important facts mentioned by user

### Memory Format
```
# MEMORY.md

## Project Context
- User is building a Python web scraper

## Learned Patterns  
- Prefers asyncio over threading for I/O

## Key Facts
- Deployment target: AWS Lambda

---

# USER.md

## Preferences
- Language: Python
- IDE: Cursor
- Response style: Concise, code-first

## Projects
- Web scraper for e-commerce sites
- ML model for price prediction
```

### Memory Rules
1. Keep memory concise - respect character limits
2. Only store truly important information
3. Update outdated info instead of adding duplicates
4. Remove information that's no longer relevant
5. Prioritize recent and frequently-used information

## Auto-Reflection
Every 10 conversation turns, ask yourself:
"Is there important information from this conversation that should be saved to memory?"
If yes, update MEMORY.md or USER.md accordingly.
```

### 4. Helper Scripts Design

#### memory_extract.py
- Input: Conversation transcript or summary
- Output: Structured memory updates
- Logic:
  1. Parse conversation for key information
  2. Classify into: user_preference, project_context, learned_pattern, important_fact
  3. Generate memory update in proper format
  4. Merge with existing memory (deduplication)
  5. Enforce character limits

#### memory_inject.py
- Input: Memory files
- Output: Formatted text for system prompt injection
- Logic:
  1. Read MEMORY.md and USER.md
  2. Format as frozen snapshot
  3. Insert into system prompt template

#### memory_cleanup.py
- Remove outdated information
- Deduplicate entries
- Compress to fit character limits
- Priority scoring for information retention

### 5. CLI Tool Design

```bash
# View current memory
universal-memory view

# Search memory
universal-memory search "python project"

# Force save current context
universal-memory save "User prefers pytest for testing"

# Show memory statistics
universal-memory stats

# Reset memory
universal-memory reset
```

### 6. Compatibility Layer

Provide integration guides for:
- **Claude Desktop**: Custom instructions + memory files
- **Cursor**: .cursor/rules + memory files
- **Windsurf**: Cascade rules + memory files
- **ChatGPT**: Custom instructions (manual copy)
- **Any AI Tool**: Generic skill format

### 7. Testing Strategy

#### Unit Tests
- Test memory extraction logic
- Test memory injection formatting
- Test cleanup and deduplication
- Test character limit enforcement
- Test skill format validation

#### Integration Tests
- Full workflow: extract → save → inject → use
- Multi-session simulation
- Compatibility with different AI tools
- Performance under character limits

#### Test Fixtures
- Sample conversations
- Expected memory outputs
- Edge cases (empty memory, full memory, corrupted files)

## Implementation Phases

### Phase 1: Core Skill Files
- Write memory.md, memory-manager.md, memory-reflect.md
- Create example memory templates
- Basic documentation

### Phase 2: Helper Scripts
- Implement memory_extract.py
- Implement memory_inject.py  
- Implement memory_cleanup.py
- Unit tests for all scripts

### Phase 3: CLI Tool
- Build memory-cli package
- Implement view, search, save, stats commands
- Integration tests

### Phase 4: Documentation & Examples
- Complete README
- Compatibility guide
- Examples for each supported tool
- Quick start tutorial

### Phase 5: Testing & Polish
- Full test suite
- Code quality checks
- Performance optimization
- Final review

## Technical Decisions

1. **Python for scripts**: Wide compatibility, easy to understand
2. **Markdown for memory files**: Human-readable, editable by any tool
3. **No database dependencies**: Simple file-based approach
4. **Character limits**: Ensure memory fits in context window
5. **Open standard format**: Any AI agent can read/write the same files
