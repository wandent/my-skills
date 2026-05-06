---
name: query-markdown-notes
description: Query and retrieve information from a markdown knowledge base stored in C:\Users\wandent\OneDrive - Microsoft\Documents\_CST\CST_FY26. Use this skill whenever you need to search, retrieve, filter, or summarize notes from the user's personal knowledge base by project, topic, keyword, or full-text search. The skill searches markdown files efficiently, returns relevant sections with context, filters by folder/project, and can generate summary notes. Use this skill when the user asks about their projects, notes, documentation, or knowledge base, or when you need context from their stored information. Always use this skill for any query that might be answered in their knowledge base.
compatibility: "Requires: Python 3.8+, pathlib, re modules"
---

# Query Markdown Notes

A skill to efficiently search, retrieve, and summarize information from your markdown knowledge base.

## Knowledge Base Location

- **Base Path**: `C:\Users\wandent\OneDrive - Microsoft\Documents\_CST\CST_FY26`
- **Supported Formats**: `.md` (markdown)
- **Pre-processed Files**: Stored in `.knowledge_base_preprocessed/` folder (created in current working directory)
- **Output**: Summary notes saved to current working directory, full context loaded internally for reasoning

## How to Use This Skill

The skill provides multiple ways to query your knowledge base:

### 1. Full-Text Search
Search for specific content across all markdown files:
```
Search for "B3 DataLake" to find all notes mentioning this project
```

### 2. Keyword & Project Filtering
Combine keyword search with folder/project filtering:
```
Find all notes in the "B3 - DataLake Migration" project mentioning "AWS"
```

### 3. Browse by Structure
List available projects and folders to explore what exists:
```
Show me what's in the Projects folder
```

### 4. Generate Summary Notes
Create a summary document from query results:
```
Search for "authentication" and create a summary note with findings
```

### 5. Multi-Format Input Processing
The skill can pre-process Word, PowerPoint, and Excel files:
- Convert `.docx` to markdown in `.knowledge_base_preprocessed/`
- Extract text from `.pptx` and save as markdown
- Convert `.xlsx` to markdown tables

## Query Operations

### Search Operation
Performs full-text search across markdown files with optional filtering.

**Parameters:**
- `query` (required): Search term or keywords
- `project_filter` (optional): Narrow search to specific project/folder (e.g., "B3 - DataLake Migration", "Projects/Analog Devices")
- `max_results` (optional, default=10): Limit number of results to return
- `include_context_lines` (optional, default=3): Lines of context around match

**Output Format:**
```
[File Match 1]
Path: <relative path from knowledge base>
Project: <project name if identifiable>
Relevance: <match type - direct keyword hit, section header, etc.>

Context:
<snippet with match highlighted, including surrounding lines>

---
[File Match 2]
...
```

### Filter by Project
List and filter notes by project or folder:

**Parameters:**
- `project_path` (required): Path relative to knowledge base (e.g., "Projects", "Archive/FY25")
- `recursive` (optional, default=true): Include subfolders

**Output:** Folder structure with file counts and descriptions

### Generate Summary
Create a summary note from search results with internal full-context loading:

**Parameters:**
- `query`: Original search query
- `max_file_count` (optional, default=5): Number of top files to summarize

**Output Format:**

The skill generates a markdown file with:
- **Title**: Based on search query
- **Summary**: Synthesized findings from all matched files
- **Key Findings**: Bullet points extracted from relevant sections
- **Sources**: List of files consulted (internal full context loaded, summary shown)
- **Related Topics**: Suggested related queries

This file is saved to the current working directory as `summary_<query>_<timestamp>.md`

## Multi-Format Support

When files are encountered in the knowledge base:

### Word Documents (.docx)
- Extracted to markdown format
- Saved to `.knowledge_base_preprocessed/<filename>.md`
- Indexed for future searches
- Tables preserved as markdown tables

### PowerPoint Files (.pptx)
- Slide content extracted as markdown
- Slide numbers preserved
- Saved to `.knowledge_base_preprocessed/<filename>.md`
- Slide notes included

### Excel Files (.xlsx)
- Converted to markdown tables
- Sheet names become section headers
- Saved to `.knowledge_base_preprocessed/<filename>.md`
- Cell data preserved with alignment

## Important Behavior

### File Persistence
- **Reads**: All markdown files from the knowledge base folder
- **Preprocesses**: Converts Word/PowerPoint/Excel to markdown in `.knowledge_base_preprocessed/`
- **Outputs**: Only summary notes saved to current working directory
- **Context**: Full file contents loaded internally (not summarized) for reasoning

### Search Strategy
1. First searches existing markdown files
2. Identifies non-markdown files (Word, PowerPoint, Excel)
3. Pre-processes them on first encounter
4. Re-runs search including converted files
5. Returns ranked results by relevance

### Folder Structure Navigation
The knowledge base is organized hierarchically:
- `Projects/` - Active project work
- `Archive/` - Historical projects and materials
- `Archive/FY25/` - Previous fiscal year
- `Archive/Brazil Sub/` - Regional subcategories

## Output Examples

### Search Result Example
```
[File Match 1]
Path: Projects/B3 - DataLake Migration/pdd-analyse-aws-azure.md
Project: B3 - DataLake Migration
Relevance: AWS mentioned in architecture decisions section

Context:
...current architecture uses on-premises data warehouse.
The proposal compares AWS Redshift vs Azure Synapse for the migration.
Key considerations include cost, integration with existing SQL Server...
```

### Summary Note Example
```
# Summary: B3 AWS Migration Analysis

## Summary
The B3 DataLake migration project is evaluating cloud data warehouse solutions
for replacing their on-premises infrastructure...

## Key Findings
- AWS Redshift and Azure Synapse are primary candidates
- Cost analysis favors Azure Synapse in hybrid scenarios
- Migration timeline: 18 months
- Phase 1: POC with sample data (Q2 FY26)

## Sources
- Projects/B3 - DataLake Migration/pdd-analyse-aws-azure.md
- Projects/B3 - DataLake Migration/Notes.md
- [Internal full context loaded for reasoning]

## Related Topics
- Cloud migration strategy
- Data warehouse optimization
- AWS vs Azure comparison
```

## Implementation Details

### Internal Processing
1. **Indexing**: Creates an internal index on first run for fast searching
2. **Caching**: Maintains cache of file contents in memory during session
3. **Preprocessing**: Auto-converts non-markdown files on first discovery
4. **Ranking**: Results ranked by relevance score (keyword position, frequency, section type)

### Error Handling
- Missing files gracefully skip without stopping search
- Invalid markdown skips to next file
- Non-readable files logged but don't interrupt operation
- Large files processed in chunks to avoid memory issues

## Workflow

1. **User asks a question** that might be answered in their knowledge base
2. **Skill searches** the knowledge base using keywords and project filters
3. **Skill identifies** relevant markdown files and pre-processes any non-markdown files
4. **Skill returns** relevant sections with context and file references
5. **Skill creates summary** if requested (optional)
6. **Full content loaded internally** for reasoning and context during the session
7. **Summary saved** to current working directory with timestamp

## Example Queries

- "What notes do I have about AWS migration?"
- "Show me everything in the B3 project about architecture"
- "Summarize my authentication implementation notes"
- "What's in the Brazil Sub folder?"
- "Find all mentions of 'GenAI' across my projects"
- "Create a summary of the Analog Devices project"
