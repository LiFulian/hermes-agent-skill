# Quick Start Guide

Get Universal Memory Skill running in under 5 minutes with any AI tool.

## Option 1: Claude Desktop

### Step 1: Create Memory Directory
```bash
mkdir -p ~/.universal-memory
```

### Step 2: Create Memory Templates
```bash
cat > ~/.universal-memory/MEMORY.md << 'EOF'
# Agent Memory

## Project Context

## Learned Patterns

## Key Facts

## Active Tasks
EOF

cat > ~/.universal-memory/USER.md << 'EOF'
# User Profile

## Preferences

## Projects

## Coding Style

## Important Notes
EOF
```

### Step 3: Add Custom Instructions
1. Open Claude Desktop Settings
2. Go to "Custom Instructions"
3. Add the following:

```
You have persistent memory stored at ~/.universal-memory/

At session start:
1. Read ~/.universal-memory/MEMORY.md
2. Read ~/.universal-memory/USER.md
3. Use this information to personalize responses

During conversation:
- Extract important information (preferences, project context, patterns)
- Update memory files when valuable information is discovered
- Keep memory files within character limits (MEMORY.md: 2200, USER.md: 1500)

Memory format: See ~/.universal-memory/ for examples
```

### Step 4: Done!
Start using Claude - it will now remember context across sessions.

## Option 2: Cursor IDE

### Step 1: Create Memory Directory
```bash
mkdir -p ~/.universal-memory
```

### Step 2: Create Memory Files
(Same templates as Claude Desktop)

### Step 3: Create Cursor Rules
```bash
mkdir -p .cursor
cat > .cursor/rules/memory.mdc << 'EOF'
---
description: Enable persistent memory for AI assistant
---

AI assistant has persistent memory at ~/.universal-memory/

Read MEMORY.md and USER.md at session start.
Update memory files with important information.
Keep memory within character limits.
EOF
```

### Step 4: Done!
Cursor will now use memory across sessions.

## Option 3: Windsurf IDE

### Step 1: Create Memory Directory and Files
(Same as above)

### Step 2: Configure Cascade Rules
Add to your `.windsurfrules` or Cascade settings:

```
Memory system enabled at ~/.universal-memory/
Read and update MEMORY.md and USER.md automatically.
```

### Step 3: Done!

## Option 4: ChatGPT

### Step 1: Create Memory Files
(Same as above, you'll need to manage manually)

### Step 2: Add to Custom Instructions
Go to Settings → Custom Instructions and add:

```
I use a memory system. Check the files at ~/.universal-memory/ if you have file access.
Remember to ask me what to remember after important conversations.
```

### Step 3: Manual Updates
Since ChatGPT can't read files, you'll need to:
1. Copy memory content into conversation when needed
2. Ask ChatGPT to summarize what to remember
3. Manually update MEMORY.md and USER.md

## Using the CLI Tool

Install the package:
```bash
pip install universal-memory-skill
```

View your memory:
```bash
universal-memory view
```

Search memory:
```bash
universal-memory search "python"
```

Save information:
```bash
universal-memory save "User prefers Python 3.11"
```

## Next Steps

- Read [COMPATIBILITY.md](COMPATIBILITY.md) for more tools
- Learn about memory format in the `skills/memory.md` file
- Customize memory templates for your needs
- Explore automatic memory management features

## Troubleshooting

**Memory not being read?**
- Check file path is correct: `~/.universal-memory/`
- Ensure files are readable
- Check file format is valid Markdown

**Memory getting too large?**
- Run cleanup: `universal-memory stats` to check size
- Manually trim old entries
- AI should auto-cleanup when approaching limits

**CLI not working?**
- Ensure Python 3.8+ is installed
- Run `pip install -e .` in project directory
- Check `universal-memory --help` for command list
