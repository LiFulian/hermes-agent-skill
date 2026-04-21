# Memory Manager Skill

## Overview
This skill provides advanced memory management operations for maintaining and optimizing your persistent memory system. Use this skill when you need to perform maintenance, search, reorganize, or clean up memory files.

## When to Use This Skill

Use this skill when:
- Memory files are approaching character limits
- You need to search for specific information in memory
- Memory contains outdated or duplicate entries
- You want to reorganize memory structure
- The user asks to view or manage memory
- Periodic memory maintenance is needed

## Memory Operations

### 1. Memory Search
To find specific information in memory:

1. Read MEMORY.md and USER.md
2. Search for relevant keywords or concepts
3. Return matching entries with context

Example search queries:
- "What projects is the user working on?"
- "What testing framework does the user prefer?"
- "What are the deployment constraints?"

### 2. Memory Cleanup
When memory is getting cluttered:

1. Read current memory files
2. Identify and remove:
   - Outdated information (projects no longer active)
   - Duplicate entries
   - Vague or low-value information
   - Information older than 30 days (unless still relevant)
3. Reorganize remaining information by importance
4. Ensure character limits are respected
5. Write cleaned memory files

### 3. Memory Reorganization
To improve memory structure:

1. Read current memory files
2. Categorize information into appropriate sections:
   - **Project Context**: Active projects, tech stacks, architecture
   - **Learned Patterns**: Successful approaches, user preferences
   - **Key Facts**: Environment facts, conventions, configs
   - **Active Tasks**: Current work, recent changes, next steps
3. Prioritize entries by importance and recency
4. Trim to fit character limits if needed
5. Write reorganized memory files

### 4. Memory Merge
When you have multiple sources of information:

1. Read all relevant memory files
2. Combine information, removing duplicates
3. Prioritize newer information over older
4. Keep most specific version of duplicate entries
5. Write merged memory files

## Cleanup Priority Algorithm

When memory exceeds character limits, remove information in this order:

1. **Remove first**: Information older than 60 days with no recent references
2. **Remove second**: Vague or generic statements
3. **Remove third**: Duplicate or near-duplicate entries
4. **Remove fourth**: Low-specificity information
5. **Keep always**: User preferences, active project context, critical conventions

## Memory Quality Checks

After any memory update, verify:

1. **Character count**: Within limits (MEMORY.md: 2200, USER.md: 1500)
2. **No duplicates**: Each piece of information appears only once
3. **Specific**: Entries contain concrete details, not vague statements
4. **Current**: Information is still relevant and accurate
5. **Structured**: Proper markdown format with clear sections
6. **Complete**: No truncated sentences or incomplete thoughts

## Example Cleanup Operation

**Before cleanup** (MEMORY.md approaching limit):
```markdown
# Agent Memory

## Project Context
- User is building a Python web scraper
- User was considering using requests library
- User decided to use asyncio and aiohttp instead
- Project involves scraping e-commerce sites
- User mentioned possibly adding ML features
- Tech stack: Python 3.11, asyncio, aiohttp, BeautifulSoup
- Deployment target: AWS Lambda
- User is also working on a React dashboard
- User might switch to FastAPI later

## Learned Patterns
- Prefers asyncio over threading
- User likes comprehensive error handling
- User prefers explicit type hints
- Memory from last session: asyncio is better
- Use connection pooling for HTTP requests

## Key Facts
- Uses Cursor IDE
- Prefers pytest
- AWS Lambda has 15min timeout
- User has AWS account
- Memory: always use async/await
```

**After cleanup**:
```markdown
# Agent Memory

## Project Context
- Python web scraper for e-commerce sites
- Tech stack: Python 3.11, asyncio, aiohttp, BeautifulSoup
- Deployment: AWS Lambda (15min timeout)

## Learned Patterns
- Prefers asyncio over threading for I/O
- Comprehensive error handling required
- Explicit type hints in all code
- Use connection pooling for HTTP requests

## Key Facts
- IDE: Cursor
- Testing: pytest
- Cloud: AWS (account configured)
```

## Automated Maintenance

Perform these checks periodically (every 5-10 sessions):

1. **Size check**: Are memory files within limits?
2. **Relevance check**: Is all information still current?
3. **Structure check**: Is information well-organized?
4. **Value check**: Does each entry provide useful context?

If any check fails, perform appropriate maintenance operation.

## User-Requested Memory Operations

When user asks to manage memory:

- "Show me my memory" → Read and display both memory files
- "Clear my memory" → Ask for confirmation, then reset files to empty templates
- "Remember that [X]" → Add specific information to appropriate memory file
- "Forget about [X]" → Remove specific information from memory
- "What do you know about me?" → Summarize key points from memory files
- "Update memory" → Perform full cleanup and reorganization

Always confirm destructive operations (clear, delete) before executing.
