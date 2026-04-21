# Architecture Documentation

Detailed technical architecture of Universal Memory Skill.

## Design Philosophy

Universal Memory Skill is designed with three core principles:

1. **Universality**: Works with any AI tool, no vendor lock-in
2. **Simplicity**: Plain text files, no databases or complex dependencies
3. **Transparency**: Human-readable and editable memory files

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                      AI Agent                           │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Skill Files │  │ Session      │  │ Reflection   │  │
│  │  (memory.md) │  │ Context      │  │ Engine       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                   │                  │        │
│         └───────────────────┼──────────────────┘        │
│                             │                           │
└─────────────────────────────┼───────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Memory Files     │
                    │                   │
                    │  MEMORY.md (2200) │
                    │  USER.md (1500)   │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │ Extractor  │ │ Injector   │ │ Cleaner    │
        └────────────┘ └────────────┘ └────────────┘
```

### Component Breakdown

#### 1. Skill Layer (`skills/`)

**Purpose**: Define behavior instructions for AI agents

**Files**:
- `memory.md`: Core memory usage instructions
- `memory-manager.md`: Memory maintenance operations
- `memory-reflect.md`: Self-reflection and knowledge synthesis

**Format**: Markdown files that AI agents read and follow as instructions

#### 2. Memory Storage Layer (`~/.universal-memory/`)

**Purpose**: Persistent cross-session memory storage

**Files**:
- `MEMORY.md`: Agent's learned knowledge (2200 char limit)
- `USER.md`: User profile and preferences (1500 char limit)

**Why Markdown?**
- Human-readable
- Editable by any tool
- Structured yet flexible
- Easy to parse and update

**Character Limits Rationale**:
- Fits within AI context window
- Forces prioritization of important information
- Prevents memory bloat
- Ensures fast loading

#### 3. Helper Scripts (`scripts/`)

**Memory Extractor** (`memory_extract.py`):
- **Input**: Conversation text
- **Output**: Structured memory entries
- **Logic**: Pattern matching to identify important information
- **Classification**: Categorizes into preference, context, pattern, fact, style

**Memory Injector** (`memory_inject.py`):
- **Input**: Memory files
- **Output**: Formatted text for system prompt
- **Logic**: Reads files and formats as frozen snapshot
- **Template**: Configurable injection format

**Memory Cleaner** (`memory_cleanup.py`):
- **Input**: Existing memory files
- **Output**: Cleaned and optimized memory
- **Logic**: Deduplication, whitespace normalization, size management
- **Priority**: Importance scoring for information retention

#### 4. CLI Layer (`cli/`)

**Purpose**: User-facing command-line interface

**Commands**:
- `view`: Display current memory
- `search`: Search memory content
- `save`: Manually save information
- `stats`: Show memory statistics
- `reset`: Clear all memory

#### 5. Test Layer (`tests/`)

**Unit Tests**: Individual component testing
- `test_memory_extract.py`: Extraction logic
- `test_memory_inject.py`: Injection formatting
- `test_memory_cleanup.py`: Cleanup operations
- `test_skill_format.py`: Skill file validation
- `test_cli_commands.py`: CLI command testing

**Integration Tests**: Full workflow testing
- `test_full_workflow.py`: End-to-end scenarios

## Memory Flow

### Session Start Flow

```
1. AI Agent starts session
   ↓
2. Check for memory files at ~/.universal-memory/
   ↓
3. If exist, read MEMORY.md and USER.md
   ↓
4. Format as frozen snapshot
   ↓
5. Inject into system prompt
   ↓
6. AI uses memory to personalize responses
```

### During Session Flow

```
1. User and AI interact
   ↓
2. AI identifies important information:
   - User preferences revealed
   - Project context shared
   - Patterns discovered
   - Facts mentioned
   ↓
3. AI updates memory files (automatic)
   ↓
4. Check character limits
   ↓
5. If over limit, trim oldest/least important entries
```

### Reflection Flow

```
1. Every 10 conversation turns
   ↓
2. AI reviews recent conversation
   ↓
3. Identifies insights worth remembering:
   - New preferences
   - Project changes
   - Lessons learned
   - Patterns emerging
   ↓
4. Updates memory files
   ↓
5. Synthesizes related entries (every 50 turns)
```

## Data Structures

### Memory Entry

```python
@dataclass
class MemoryEntry:
    content: str              # The actual information
    memory_type: MemoryType   # Classification
    importance: float         # 0.0 to 1.0
    timestamp: Optional[str]  # When it was recorded
```

### Memory Types

```python
class MemoryType(Enum):
    USER_PREFERENCE = "user_preference"     # User's likes/dislikes
    PROJECT_CONTEXT = "project_context"     # Project info
    LEARNED_PATTERN = "learned_pattern"     # Successful approaches
    IMPORTANT_FACT = "important_fact"       # Key facts
    CODING_STYLE = "coding_style"           # Code conventions
    ACTIVE_TASK = "active_task"             # Current work
```

## Memory Management Algorithm

### Extraction Priority

1. **Explicit Statements**: "I prefer X", "Remember that Y"
2. **Repeated Information**: Mentioned multiple times
3. **Corrections**: User corrects AI's approach
4. **Project Decisions**: Architecture choices, tech stack
5. **Style Preferences**: Code format, naming conventions

### Cleanup Priority (when over limit)

1. Remove: Information older than 60 days with no recent use
2. Remove: Vague or generic statements
3. Remove: Duplicate or near-duplicate entries
4. Remove: Low-specificity information
5. Keep: User preferences (always relevant)
6. Keep: Active project context
7. Keep: Critical conventions and constraints

### Deduplication Strategy

- Normalize text to lowercase for comparison
- Use exact match for short entries
- Use fuzzy match for longer entries
- Keep most recent version of duplicates
- Keep most specific version

## Error Handling

### File System Errors
- Missing directory: Auto-create
- Missing files: Auto-create with templates
- Permission errors: Graceful fallback with warning
- Corrupted files: Reset to template

### Character Limit Errors
- Pre-emptive trimming before write
- Post-write validation
- Emergency cleanup if still over limit

### Memory Quality Errors
- Empty content: Skip update
- Invalid format: Log warning and skip
- Duplicate detection: Prevent redundant entries

## Performance Considerations

### File I/O
- Small files (< 3KB total) - fast reads/writes
- Minimal parsing - simple text operations
- No database overhead

### Memory Limits
- 2200 chars = ~800 tokens = minimal context usage
- 1500 chars = ~550 tokens = minimal context usage
- Total: ~1350 tokens = < 5% of typical context window

### Scalability
- Works with any number of sessions
- No state to manage beyond files
- Can sync across devices via file sync

## Security Considerations

### What NOT to Store
- Passwords or API keys
- Personal sensitive data
- Temporary session tokens
- Anything user asks to forget

### File Permissions
- Memory directory: User-only access (700)
- Memory files: User read/write (600)

### User Control
- User can view memory anytime
- User can edit memory files directly
- User can reset/clear memory
- User can disable memory system

## Extension Points

### Custom Extractors
Add domain-specific extraction patterns:
```python
class CustomExtractor(MemoryExtractor):
    def _extract_domain_specific(self, text):
        # Custom pattern matching
        pass
```

### Custom Injectors
Change injection format:
```python
class CustomInjector(MemoryInjector):
    INJECT_TEMPLATE = "Your custom template here"
```

### Custom Cleanup Rules
Adjust cleanup priorities:
```python
class CustomCleaner(MemoryCleaner):
    def _custom_scoring(self, line):
        # Custom importance scoring
        pass
```

## Testing Strategy

### Unit Tests
- Test each module in isolation
- Mock file system operations
- Test edge cases (empty, full, corrupted)

### Integration Tests
- Test complete workflows
- Multi-session simulations
- Character limit enforcement

### Format Tests
- Validate skill file structure
- Check required sections exist
- Verify character limits mentioned

## Future Enhancements

### Potential Features
1. **Vector Search**: Semantic search over memory
2. **Memory Graph**: Relationship mapping between entries
3. **Importance Decay**: Time-based relevance scoring
4. **Multi-User**: Support for multiple user profiles
5. **Memory Bulletin**: Periodic knowledge synthesis
6. **Skill Generation**: Auto-create skills from patterns

### Why Not Implemented Now?
- KISS principle (Keep It Simple, Stupid)
- Core functionality first
- Avoid over-engineering
- Prove concept before adding complexity
