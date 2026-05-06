# Search Session History Skill - README

This skill searches through your chat session history to find documents, artifacts, responses, and generated content.

## Features

- **Keyword search**: Find files by searching both filename and content
- **Temporal filtering**: Use relative dates (last week, last month) or specific date ranges (May 1-15)
- **Multi-format support**: Searches .md, .txt, and .json files
- **Relevance ranking**: Results sorted by match quality and recency
- **Conversation context**: Each result includes context about what you were working on
- **Markdown output**: Results saved as a readable summary in your current directory

## Quick Usage

### Basic search
```
Search my sessions for "Docker" from the last month
```

### Complex search with date range
```
Find files about "API design" between May 1 and May 20
```

### Specific file type search
```
Show me markdown notes about "Machine Learning" from the past 2 weeks
```

## How Results Are Presented

The skill generates a markdown summary file with:
1. **Results table** - File path, type, modification date, relevance score
2. **Details section** - For each match:
   - Session ID and file path
   - Creation and modification dates
   - Relevance score (0-100)
   - Conversation context (what you were working on)
   - Excerpt with line number

## Installation

Copy this skill folder to `~/.my-skills/search-session-history/`

## Dependencies

- Python 3.8+
- Standard library only (no external packages required)

## Notes

- Only searches text-readable files (.md, .txt, .json)
- Binary files and images are skipped
- Session folders must be readable by your current process
- Very large files (>1MB) are sampled
