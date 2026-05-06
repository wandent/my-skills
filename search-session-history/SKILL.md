---
name: search-session-history
description: Search chat session history and artifacts stored locally for content, responses, and generated documents. This skill searches through your past chat sessions (text, JSON, markdown files) across session folders, filters by file creation/modification dates using both relative (last month, last week) and specific date ranges, ranks results by relevance and date, includes conversation context for each result, and generates a summary markdown file. Use this skill whenever you need to find something you've worked on before—whether it's code snippets, analysis, documents, research notes, or design artifacts from past sessions. Searches are sorted by date, include the original user request that prompted the result, and only save output to your current directory.
compatibility: Python 3.8+, requires read access to session-state directory
---

# Search Session History Skill

This skill helps you find documents, responses, and artifacts generated in past chat sessions. It's designed to work with your local session storage and supports rich temporal filtering and context extraction.

## Quick Start

### Basic keyword search
```
Search my chat sessions for "Terraform" documents created in the last month
```

### Temporal filtering examples
```
Find all markdown files I worked on last week about "Azure"
Search for "Docker" in session files between May 1 and May 15
Show me analysis documents from the past 2 weeks
```

### Content + filename search
```
Find responses or documents mentioning "API design" from the last month
Search for files with "migration" in the name or content, from March
```

## How It Works

**Search Scope**
- Searches `.md`, `.txt`, `.json` files in session folders
- Looks in both file names and file content
- Respects file creation/modification timestamps

**Temporal Filtering Options**

*Relative dates (from today):*
- "last X days" (e.g., last 3 days)
- "last week", "last 2 weeks"
- "last month", "last 3 months"
- "past X hours" (for recent work)

*Specific date ranges:*
- "between May 1 and May 15"
- "after April 20"
- "before June 1"

**Results Include**

For each match:
1. **File path** and session folder name
2. **File type** (.md, .txt, .json)
3. **Dates** (created, modified)
4. **Relevant excerpts** from the content
5. **Conversation summary** - Context about what the user was trying to accomplish when this content was generated
6. **Match score** - Based on relevance and recency

**Output Format**

Results are saved as a markdown summary file to your current working directory with:
- Search query and filters applied
- Execution timestamp
- Sorted results (by date, descending)
- File content previews
- Conversation context for each result

## Search Examples

### Example 1: Find recent research
**Query:** "Find markdown files about cloud architecture from the last 2 weeks"
**Result:** 
- Identifies session folders created/modified in the past 2 weeks
- Searches for "cloud" + "architecture" in filenames and content
- Returns matching .md files with context about what projects you were working on

### Example 2: Temporal + keyword search
**Query:** "Search for 'database design' documentation from March"
**Result:**
- Filters to files created/modified in March
- Searches for phrase "database design"
- Returns matches with surrounding context and conversation summaries

### Example 3: Find code snippets
**Query:** "Show me code examples mentioning 'FastAPI' from the last month"
**Result:**
- Searches .txt, .md, .json files (skips binary)
- Finds FastAPI references
- Shows code blocks with context about what you were building

## Limitations

- Only searches text-based files (.md, .txt, .json)
- Binary files (images, PDFs, Office docs) are skipped
- Session folders must be readable by your current process
- Very large files (>1MB) are sampled
- Conversation context is best-effort based on available metadata

## Tips for Better Results

1. **Be specific with keywords** - "Flask routing" finds more than just "Flask"
2. **Combine date + keyword** - Much faster than searching all history
3. **Check file extensions** - Know what type of files you're looking for (.md for notes, .json for configs, .txt for logs)
4. **Use relative dates** - "last month" is easier than calculating specific dates
5. **Look at the summary file** - The output markdown includes search metadata showing what was filtered

## Understanding the Output

The generated markdown summary includes:
- **Search Metadata**: Query, filters, execution time, number of matches
- **Results Table**: File path, type, dates, relevance score
- **Content Previews**: Excerpts from matches with line context
- **Conversation Context**: Summary of what you were working on when this was created
- **Date Sorting**: Results ordered newest first (or by your preference)
