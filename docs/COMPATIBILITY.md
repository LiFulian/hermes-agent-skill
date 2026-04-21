# Compatibility Guide

Universal Memory Skill works with any AI tool. Here's how to set it up with popular platforms.

## Supported Tools

### 1. Claude Desktop

**Integration Type**: Custom Instructions
**Setup Difficulty**: Easy
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory
2. Create `MEMORY.md` and `USER.md` templates
3. Add memory instructions to Custom Instructions
4. Claude will automatically read/write memory files

#### Features Supported
- ✅ Read memory at session start
- ✅ Automatic memory updates
- ✅ Memory reflection
- ✅ Cross-session persistence

#### Limitations
- Memory size depends on Claude's context window
- No built-in memory search (use CLI tool)

### 2. Cursor IDE

**Integration Type**: .cursor/rules
**Setup Difficulty**: Easy
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory
2. Create `.cursor/rules/memory.mdc` file
3. Add memory instructions to rules file

#### Example .cursor/rules/memory.mdc
```markdown
---
description: Persistent memory system
globs: **/*
---

## Memory System

Memory files are at `~/.universal-memory/`

At session start:
- Read `~/.universal-memory/MEMORY.md`
- Read `~/.universal-memory/USER.md`

During conversations:
- Update memory with important information
- Respect character limits (MEMORY.md: 2200, USER.md: 1500)
- Auto-reflect every 10 turns
```

#### Features Supported
- ✅ Full memory support
- ✅ Project-specific rules
- ✅ Automatic memory management

### 3. Trae IDE

**Integration Type**: Built-in Skills / Custom Instructions
**Setup Difficulty**: Easy
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory
2. Create `MEMORY.md` and `USER.md` templates
3. Copy `skills/memory.md` content to Trae's skill configuration
4. Configure memory path in Trae settings

#### Features Supported
- ✅ Full memory support
- ✅ Built-in skills system
- ✅ Automatic memory management
- ✅ Cross-session persistence

#### Configuration Example
Add to Trae's custom instructions or skill configuration:
```
You have persistent memory at ~/.universal-memory/
Read MEMORY.md and USER.md at session start.
Update memory with important information during conversations.
```

### 4. CodeBuddy (by Cocop)

**Integration Type**: Plugin / Extension
**Setup Difficulty**: Easy
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory
2. Install CodeBuddy plugin/extension
3. Configure memory path in CodeBuddy settings
4. Copy `skills/memory.md` to CodeBuddy's skill directory

#### Features Supported
- ✅ Full memory support
- ✅ Plugin ecosystem integration
- ✅ Automatic memory management

### 5. Coder

**Integration Type**: Remote Development / Workspace Configuration
**Setup Difficulty**: Medium
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory (works with remote workspaces)
2. Configure memory path in Coder workspace template
3. Copy `skills/memory.md` to workspace configuration
4. Set up file sync for memory files across workspaces

#### Features Supported
- ✅ Full memory support for remote development
- ✅ Workspace-level memory persistence
- ✅ Multi-machine sync (with cloud storage)

### 6. Windsurf IDE (Cascade)

**Integration Type**: Cascade Rules
**Setup Difficulty**: Easy
**Auto-Update**: Yes

#### Setup Instructions
1. Create `~/.universal-memory/` directory
2. Add memory instructions to `.windsurfrules` or Cascade settings

#### Features Supported
- ✅ Full memory support
- ✅ Cascade integration

### 7. ChatGPT

**Integration Type**: Custom Instructions (Manual)
**Setup Difficulty**: Medium
**Auto-Update**: Manual

#### Setup Instructions
1. Create memory files manually
2. Add memory awareness to Custom Instructions
3. Manually update memory files

#### Manual Workflow
1. At start of important conversation, paste memory content
2. Ask ChatGPT: "What should I remember from this conversation?"
3. Manually update MEMORY.md/USER.md

#### Features Supported
- ✅ Memory format compatibility
- ⚠️ Manual updates required
- ❌ No automatic file access

### 8. GitHub Copilot (VS Code)

**Integration Type**: Workspace Settings
**Setup Difficulty**: Medium
**Auto-Update**: Yes (with extensions)

#### Setup Instructions
1. Create `.github/copilot-instructions.md` in workspace
2. Add memory instructions
3. Use with VS Code file system access

### 9. Ollama / Local LLMs

**Integration Type**: System Prompt
**Setup Difficulty**: Easy
**Auto-Update**: Yes (with tool calls)

#### Setup Instructions
1. Add memory instructions to system prompt
2. Configure file read/write tool calls
3. Point to `~/.universal-memory/` directory

#### Example System Prompt Addition
```
You have access to persistent memory at /home/user/.universal-memory/
Use file read/write tools to access MEMORY.md and USER.md.
```

### 10. Any AI Tool

**Integration Type**: Skill File Copy
**Setup Difficulty**: Easy
**Auto-Update**: Depends on tool

#### Universal Setup
1. Copy `skills/memory.md` to your AI tool's skill/instruction location
2. Create `~/.universal-memory/` directory
3. Create memory template files
4. Configure your AI tool to load the skill

#### Requirements
Your AI tool must support:
- Reading files from disk (or pasting content)
- Following instructions from skill files
- Writing files (for automatic updates) OR manual update workflow

## Feature Comparison

| Feature | Claude | Cursor | Trae | CodeBuddy | Coder | Windsurf | ChatGPT | Any Tool |
|---------|--------|--------|------|-----------|-------|----------|---------|----------|
| Read Memory | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ⚠️ Manual | ⚠️ Depends |
| Write Memory | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ⚠️ Manual | ⚠️ Depends |
| Auto Reflection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⚠️ Depends |
| Memory Search | CLI | CLI | CLI | CLI | CLI | CLI | CLI | Use CLI |

## Advanced Configuration

### Custom Memory Directory

Set custom memory directory:
```bash
export UNIVERSAL_MEMORY_DIR=/path/to/memory
```

Or use CLI flag:
```bash
universal-memory view --memory-dir /path/to/memory
```

### Project-Specific Memory

For project-specific memory:
```bash
# Create project memory directory
mkdir -p .memory

# Copy skill files
cp -r /path/to/universal-memory-skill/skills/ .

# Configure AI tool to use .memory/ directory
```

### Memory Backup

Backup your memory:
```bash
tar -czf memory-backup-$(date +%Y%m%d).tar.gz ~/.universal-memory/
```

### Memory Sync Across Devices

Use git or cloud sync:
```bash
# Git approach
cd ~/.universal-memory
git init
git add .
git commit -m "Memory backup"
git push

# Cloud sync (e.g., Dropbox, iCloud)
# Move memory dir to synced location
mv ~/.universal-memory ~/Dropbox/universal-memory
ln -s ~/Dropbox/universal-memory ~/.universal-memory
```

## Troubleshooting by Tool

### Claude Desktop
- **Issue**: Not reading memory
  - **Solution**: Verify file paths in Custom Instructions
- **Issue**: Memory not updating
  - **Solution**: Ensure Claude has file write permissions

### Cursor
- **Issue**: Rules not applying
  - **Solution**: Check `.cursor/rules/` file format and globs
- **Issue**: Memory path wrong
  - **Solution**: Use absolute path `~/.universal-memory/`

### ChatGPT
- **Issue**: Can't access files
  - **Solution**: Use manual workflow with copy/paste
- **Issue**: Memory gets lost
  - **Solution**: Always paste memory at conversation start

## Request New Tool Support

If your AI tool isn't listed, open an issue on GitHub with:
- Tool name and version
- How the tool handles custom instructions
- Whether it supports file system access
- Any specific integration requirements
