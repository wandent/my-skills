# Query Markdown Notes Skill

A comprehensive skill for searching, retrieving, and summarizing your personal markdown knowledge base.

## Features

- **Full-text search** across markdown files
- **Project filtering** to narrow results by folder
- **Multi-format support** (converts .docx, .pptx, .xlsx to markdown)
- **Automatic preprocessing** stores converted files in `.knowledge_base_preprocessed/`
- **Summary generation** creates markdown summaries with key findings
- **Context-aware results** returns relevant sections with surrounding lines
- **Efficient caching** maintains performance on large knowledge bases

## Skill Location

`C:\Users\wandent\.my-skills\query-markdown-notes\`

## Knowledge Base

Reads from: `C:\Users\wandent\OneDrive - Microsoft\Documents\_CST\CST_FY26\`

## Installation

The skill is ready to use. When invoked, Claude will:
1. Search your markdown knowledge base
2. Pre-process any Word/PowerPoint/Excel files on first encounter
3. Return relevant sections with context
4. Generate summary notes to the current directory
5. Load full content internally for reasoning

## Usage Examples

### Search for a topic
"Find all my notes about AWS migration"

### Filter by project
"What do I have in the B3 project about DataLake?"

### Generate summary
"Create a summary of my authentication implementation notes"

### Browse structure
"Show me what's in the Projects folder"

### Multi-term search
"Find all mentions of both 'GenAI' and 'architecture'"

## Output Files

- **Summary notes**: Saved as `summary_<query>_<timestamp>.md` in current directory
- **Preprocessed files**: Cached in `.knowledge_base_preprocessed/` folder for reuse

## Scripts

- `scripts/query_notes.py` - Python implementation of the searcher (optional CLI usage)

## Requirements

- Python 3.8+
- Optional: `python-docx`, `python-pptx`, `openpyxl` for multi-format support

## Notes

- Full file contents are loaded internally for reasoning
- Summaries only show snippets with context
- Pre-processed files are reused to avoid re-conversion
- Large knowledge bases benefit from project filtering to narrow results
