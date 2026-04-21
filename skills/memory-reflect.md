# Memory Reflection Skill

## Overview
This skill enables periodic self-reflection and knowledge synthesis - a key feature that allows AI agents to continuously improve their memory by reviewing past conversations and identifying valuable insights worth preserving.

## When to Use This Skill

Use this skill:
- Every 10 conversation turns (count messages in current session)
- After completing a significant task or solving a complex problem
- When the user explicitly asks you to reflect
- At natural conversation breaks or session endings
- When you notice patterns that should be remembered

## Reflection Process

### Step 1: Review Recent Conversation

Look back at the last 10 messages (or recent significant interactions) and identify:

1. **New Information Learned**
   - Facts about the user (preferences, constraints, context)
   - Project details revealed
   - Technical decisions made
   - Problems encountered and solutions found

2. **Patterns Discovered**
   - Recurring themes in user requests
   - Common approaches the user prefers
   - Types of problems the user frequently solves
   - Communication style preferences

3. **Lessons Learned**
   - Mistakes made and corrections learned
   - Better approaches discovered
   - Inefficiencies to avoid
   - Successful strategies to repeat

4. **User Profile Updates**
   - New projects mentioned
   - Changed preferences
   - New tools or technologies being used
   - Updated constraints or requirements

### Step 2: Synthesize Insights

Transform raw observations into concise, actionable memory entries:

**Bad (too verbose):**
"During this conversation, the user mentioned that they're working on a web scraping project and they said they prefer to use Python because they're more familiar with it, and they also mentioned that they've been using the requests library but now want to switch to asyncio for better performance with concurrent requests."

**Good (concise and structured):**
- Project: Web scraper (Python)
- Migration: requests → asyncio for concurrency
- User strength: Python

### Step 3: Update Memory Files

Based on synthesized insights:

1. **Update USER.md** if you learned about:
   - User preferences (language, tools, style)
   - New projects or goals
   - Coding style details
   - Communication preferences

2. **Update MEMORY.md** if you learned about:
   - Project context and decisions
   - Technical solutions that worked
   - Environment facts
   - Patterns to remember

3. **Skip update** if:
   - Nothing new or important was revealed
   - Information is already in memory
   - Information is transient or low-value

### Step 4: Memory Synthesis

Every 50 conversation turns (or weekly if tracking time), perform deeper synthesis:

1. Read both memory files
2. Look for connections between entries
3. Identify higher-level patterns
4. Create summary entries that capture trends
5. Remove outdated individual entries that are now captured in summaries

**Example synthesis:**

**Individual entries (before):**
```
- User prefers asyncio for web scraping
- User uses aiohttp for HTTP requests
- User likes connection pooling
- User wants timeout handling in all requests
```

**Synthesized entry (after):**
```
- HTTP approach: asyncio + aiohttp with connection pooling and explicit timeouts
```

## Reflection Questions

During reflection, ask yourself these questions:

1. **User Understanding**
   - What did I learn about the user's preferences?
   - What projects are they focused on?
   - What challenges are they facing?
   - How do they like to work?

2. **Knowledge Retention**
   - What technical solutions should I remember?
   - What approaches worked well?
   - What mistakes should I avoid next time?
   - What patterns are emerging?

3. **Memory Quality**
   - Is my memory current and accurate?
   - Are there outdated entries to remove?
   - Is memory well-organized?
   - Am I respecting character limits?

## Reflection Output Format

When reflection is complete, document what you did (internally):

```
Reflection completed:
- Reviewed last N messages
- Identified X new insights
- Updated USER.md: [list changes]
- Updated MEMORY.md: [list changes]
- Performed synthesis: [yes/no]
```

## Example Reflection

**Recent conversation summary:**
- User asked to refactor a Python function
- User preferred list comprehension over map/filter
- User mentioned they're migrating to Python 3.12
- User rejected the first approach, wanted simpler code
- Final solution used walrus operator for cleaner code

**Memory updates:**

USER.md additions:
```markdown
## Coding Style
- Prefers list comprehensions over map/filter
- Values simplicity over cleverness
- Likes modern Python features (walrus operator, etc.)
- Using Python 3.12
```

MEMORY.md additions:
```markdown
## Learned Patterns
- Python refactoring: prefer simple, readable solutions
- User may reject overly clever code
```

## Important Guidelines

1. **Be Selective**: Not everything is worth remembering
2. **Stay Objective**: Record facts and observed preferences, not assumptions
3. **Respect Privacy**: Don't store personal or sensitive information
4. **Keep Current**: Remove outdated information during reflection
5. **Be Specific**: Vague memories are not useful
6. **Synthesize Regularly**: Combine related memories to save space and improve clarity

## User Interaction

When reflecting, you can optionally ask the user:

"I've noticed we've been working on [X] - is there anything specific about this project you'd like me to remember for future sessions?"

This helps ensure you're remembering what the user considers important.
