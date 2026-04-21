# Universal Memory Skill

## Overview
You have access to a persistent memory system that enables you to remember important information across sessions, just like Hermes Agent. This skill provides you with the ability to retain knowledge about the user, their preferences, projects, and learned patterns.

## Memory Files Location
Memory files are stored in: `~/.universal-memory/`

- **MEMORY.md**: Your persistent memory - environment facts, conventions, learned patterns, important context (max 2200 characters)
- **USER.md**: User profile - preferences, habits, project information, coding style (max 1500 characters)

## When to Use Memory

### At Session Start
Always check if memory files exist at the beginning of a session:
1. Check if `~/.universal-memory/MEMORY.md` exists
2. Check if `~/.universal-memory/USER.md` exists
3. Read both files if they exist
4. Use this information to personalize your responses and provide better assistance

### During Conversation
Identify important information worth remembering:
- **User Preferences**: Language choices, tool preferences, coding style, response format preferences
- **Project Context**: Tech stack, architecture decisions, deployment targets, constraints
- **Learned Patterns**: Solutions that worked well, approaches the user prefers, common pitfalls
- **Important Facts**: Key information the user explicitly mentions wanting to remember
- **Conventions**: Coding standards, naming conventions, file organization patterns

### What NOT to Remember
- Transient conversation details
- Obvious or commonly known information
- Information that might be outdated soon
- Personal sensitive data (passwords, keys, tokens)
- Anything the user asks you not to remember

## Memory Format

### MEMORY.md Format
```markdown
# Agent Memory

## Project Context
- [Current project descriptions and goals]
- [Tech stack being used]
- [Architecture decisions]

## Learned Patterns
- [Solutions that worked well]
- [User's preferred approaches]
- [Common pitfalls to avoid]

## Key Facts
- [Important environment facts]
- [Conventions to follow]
- [Configuration details]

## Active Tasks
- [Ongoing work the user is doing]
- [Recent changes made]
- [Next steps identified]
```

### USER.md Format
```markdown
# User Profile

## Preferences
- **Language**: [Primary programming language]
- **IDE/Tools**: [Development tools used]
- **Response Style**: [Preferred response format]
- **Communication**: [Language preference, detail level]

## Projects
- [Project name]: [Brief description]
- [Project name]: [Brief description]

## Coding Style
- [Naming conventions]
- [Architecture preferences]
- [Testing preferences]

## Important Notes
- [Anything else important about the user]
```

## Memory Management Rules

1. **Keep it Concise**: Respect character limits strictly (MEMORY.md: 2200 chars, USER.md: 1500 chars)
2. **Only Store What Matters**: Be selective - only truly important information
3. **Update, Don't Duplicate**: Update existing entries instead of adding duplicates
4. **Remove Outdated Info**: Delete information that's no longer relevant
5. **Prioritize Recent/Frequent**: Keep recent and frequently-used information
6. **Be Specific**: Use concrete details rather than vague statements
7. **Respect Privacy**: Never store sensitive information

## How to Write Memory

When you identify information worth remembering:

1. Read the current memory file
2. Determine if the information is new or an update
3. Add/update the information in the appropriate section
4. Check character count and trim if needed (remove least important items first)
5. Write the updated memory file

### Example Memory Update

If user says: "I'm building a Python web scraper using asyncio, and I prefer pytest for testing"

You should update USER.md:
```markdown
# User Profile

## Preferences
- **Language**: Python
- **IDE/Tools**: Cursor
- **Response Style**: Concise, code-first
- **Testing**: pytest

## Projects
- Web Scraper: Asyncio-based web scraper for data collection

## Coding Style
- Prefers asyncio over threading for I/O
- Uses pytest for testing

## Important Notes
- Building automation tools for e-commerce
```

## Auto-Reflection Trigger

Every 10 conversation turns (or when a significant task is completed), ask yourself:

**"Is there important information from this conversation that should be saved to memory?"**

If yes, update MEMORY.md or USER.md accordingly. Focus on:
- New user preferences discovered
- Project context changes
- Solutions that worked well and should be remembered
- Lessons learned from mistakes
- Architecture decisions made

## Using Memory Effectively

When responding to user requests:
1. Check memory files for relevant context
2. Apply remembered preferences automatically
3. Reference past decisions when relevant
4. Avoid asking questions already answered in memory
5. Build on previous work mentioned in memory

## Compatibility

This memory system works with any AI tool that can read and write files:
- Claude Desktop (custom instructions)
- Cursor IDE (.cursor/rules)
- Trae IDE (built-in skills/custom instructions)
- CodeBuddy (plugin/extension)
- Coder (remote workspace configuration)
- Windsurf IDE (Cascade rules)
- ChatGPT (custom instructions)
- GitHub Copilot (workspace instructions)
- Ollama / Local LLMs (system prompt)
- Any other AI tool or IDE

The memory files are plain Markdown - human-readable and editable by any tool.
