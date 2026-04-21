# Claude Desktop Example - Universal Memory Integration

## Setup Instructions

### 1. Create Memory Directory

Open Terminal and run:
```bash
mkdir -p ~/.universal-memory
```

### 2. Create Memory Template Files

```bash
cat > ~/.universal-memory/MEMORY.md << 'EOF'
# Agent Memory

## Project Context
- [Your projects will be listed here]

## Learned Patterns
- [AI's learned patterns will be listed here]

## Key Facts
- [Important facts will be listed here]

## Active Tasks
- [Current tasks will be listed here]
EOF

cat > ~/.universal-memory/USER.md << 'EOF'
# User Profile

## Preferences
- [Your preferences will be learned]

## Projects
- [Your projects will be tracked]

## Coding Style
- [Your coding style will be remembered]

## Important Notes
- [Important notes about you]
EOF
```

### 3. Configure Claude Desktop

1. Open Claude Desktop
2. Click Settings (gear icon)
3. Find "Custom Instructions" or "Memory" section
4. Add the following instructions:

```
You have access to a persistent memory system at ~/.universal-memory/

## At Session Start
1. Read the file: ~/.universal-memory/MEMORY.md
2. Read the file: ~/.universal-memory/USER.md
3. Use this information to personalize your responses

## During Conversation
- Identify important information worth remembering:
  * User preferences (tools, languages, styles)
  * Project context (tech stack, architecture)
  * Learned patterns (what works, what doesn't)
  * Important facts (environment, constraints)
  
- Update memory files when you discover new information
- Keep MEMORY.md under 2200 characters
- Keep USER.md under 1500 characters
- Update existing entries instead of adding duplicates
- Remove outdated information

## Auto-Reflection
Every 10 conversation turns, ask yourself:
"Is there important information from this conversation that should be saved to memory?"
If yes, update the appropriate memory file.
```

### 4. Verify Setup

1. Start a new conversation with Claude
2. Ask Claude: "What do you know about me?"
3. Claude should read your memory files and respond

## Example Memory Updates

### After First Conversation

**You say**: "I'm building a Python web scraper using asyncio"

**Claude updates USER.md**:
```markdown
# User Profile

## Preferences
- Language: Python
- Async patterns: asyncio

## Projects
- Web Scraper: Asyncio-based web scraper

## Coding Style

## Important Notes
```

### After Multiple Sessions

**MEMORY.md**:
```markdown
# Agent Memory

## Project Context
- Python web scraper for e-commerce
- Tech stack: Python 3.11, asyncio, aiohttp

## Learned Patterns
- Prefers asyncio over threading
- Comprehensive error handling required

## Key Facts
- Deployment target: AWS Lambda
- IDE: Cursor

## Active Tasks
- Optimizing scraper performance
```

## Troubleshooting

**Claude not reading memory?**
- Check Custom Instructions contain the correct path
- Verify files exist at ~/.universal-memory/
- Ensure Claude has file access permissions

**Memory not updating?**
- Claude needs to be instructed to write files
- Check if Claude has write permissions
- Review memory character limits

## Advanced: Using Memory Manager Skill

For advanced memory operations, also add the contents of:
- `skills/memory-manager.md` to Custom Instructions
- `skills/memory-reflect.md` to Custom Instructions

This gives Claude full memory management capabilities.
