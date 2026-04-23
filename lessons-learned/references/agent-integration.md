# Agent Integration Guide

## Overview

This guide shows coding agents and developers how to integrate LESSONS_LEARNED.md into their workflows.

---

## Python Integration

### Load and Parse

```python
import yaml
from pathlib import Path

def load_lessons_learned(project_path="."):
    """Load and parse LESSONS_LEARNED.md"""
    file_path = Path(project_path) / "LESSONS_LEARNED.md"
    
    if not file_path.exists():
        return None, {}
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Extract YAML front matter
    parts = content.split("---")
    if len(parts) >= 3:
        yaml_content = parts[1]
        markdown_content = "---".join(parts[2:])
        
        metadata = yaml.safe_load(yaml_content)
        return metadata, markdown_content
    
    return {}, content

def get_standards_by_category(project_path, category):
    """Get all standards for a specific category"""
    metadata, _ = load_lessons_learned(project_path)
    
    if not metadata or category not in metadata.get("categories", []):
        return []
    
    # Parse markdown to extract standards for category
    # (implementation depends on markdown parsing library)
    return []
```

### Auto-Initialize & Check Prerequisites

```python
from lessons_learned_helper import LessonsHelper, ensure_initialized

# Ensure file exists (auto-creates if missing)
if not ensure_initialized("."):
    print("⚠️  Could not initialize LESSONS_LEARNED.md")
    exit(1)

# Now safe to read standards
helper = LessonsHelper(".")
version = helper.get_version()
print(f"✅ Project standards v{version} loaded")

# Add a new standard
helper.add_standard(
    category="process",
    title="Code Review Checklist",
    standard="All code changes must be peer reviewed",
    context="Catch issues early and spread knowledge",
    action="1) Create PR, 2) Add reviewer, 3) Wait for approval, 4) Merge",
    priority="HIGH",
    enforced="Manual"
)
```

### Check Before Proceeding

```python
def verify_prerequisites(lessons_path="."):
    """Check if prerequisites have been verified"""
    from lessons_learned_helper import LessonsHelper
    
    helper = LessonsHelper(lessons_path)
    if not helper.exists():
        helper.ensure_initialized()
    
    # Get HIGH-priority standards
    content = helper.read()
    
    # Check for prerequisites section
    if "Installation & Testing Requirements" in content:
        print("⚠️  Prerequisites verification required before task completion")
        return False
    
    return True
```

---

## Using the Helper Module (Recommended)

The easiest way for agents to work with LESSONS_LEARNED.md is via the helper module:

```python
from lessons_learned_helper import LessonsHelper, ensure_initialized, capture_standard

# Ensure file exists (auto-creates from template if missing)
ensure_initialized(".")

# Create helper instance
helper = LessonsHelper(".")

# Capture a new standard
helper.add_standard(
    category="process",
    title="My New Standard",
    standard="Always verify X before Y",
    context="Prevents issues with Z",
    action="1. Check X\n2. Log result\n3. Proceed if OK",
    priority="HIGH",
    enforced="Manual"
)

# Query standards
version = helper.get_version()  # Get current version
high_priority = helper.get_high_priority_standards()  # Find critical items
content = helper.read()  # Get full content

# Update metadata
helper.increment_version()  # Auto-increment: 1.0 → 1.1
```

**No file I/O needed** — the helper handles all initialization, parsing, and writing.

---

## GitHub Copilot Integration

### System Prompt Enhancement (Auto-Init Version)

```markdown
Before starting work on this project:

1. Check if LESSONS_LEARNED.md exists
   - If NOT found, auto-initialize: python scripts/init_lessons.py
   - If found, load it and read HIGH-priority standards
   
2. Report which standards apply to the current task

3. Follow all HIGH-priority standards before proceeding

4. When capturing new standards from user feedback, use:
   from lessons_learned_helper import LessonsHelper
   helper = LessonsHelper(".")
   helper.add_standard(...)

Example compliance report:
"Following project standards from LESSONS_LEARNED.md (v1.2):
✓ Initialized file from template
✓ Checked prerequisites (Playwright installed)
✓ Tested on sample website
✓ Verified file safety before creation
Ready to proceed."
```

### Auto-Initialization Config

Add to `.copilot-chat` or workspace context:

```json
{
  "project_standards": {
    "auto_init": true,
    "init_script": "python scripts/init_lessons.py",
    "helper_module": "scripts/lessons_learned_helper.py",
    "enforce_high_priority": true,
    "report_compliance": true
  }
}
```

Copilot will automatically:
1. Run init_lessons.py if LESSONS_LEARNED.md doesn't exist
2. Import helper module for standard capture operations
3. Report compliance in task completion summary

---

## Bash/CLI Integration

### Pre-flight Check with Auto-Initialization

```bash
#!/bin/bash

# Auto-initialize if needed
if [ ! -f "LESSONS_LEARNED.md" ]; then
    echo "📝 Initializing LESSONS_LEARNED.md (first time)..."
    python scripts/init_lessons.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize standards file"
        exit 1
    fi
fi

# Extract and display categories
CATEGORIES=$(grep "categories:" LESSONS_LEARNED.md | sed 's/.*\[//; s/\].*//')
echo "✅ Project standards loaded. Categories: $CATEGORIES"

# Check for HIGH priority items
HIGH_PRIORITY=$(grep -A2 "Priority.*HIGH" LESSONS_LEARNED.md | grep "Standard" | wc -l)
if [ $HIGH_PRIORITY -gt 0 ]; then
    echo "🔴 $HIGH_PRIORITY high-priority standards must be followed"
    echo ""
    grep -B1 "Priority.*HIGH" LESSONS_LEARNED.md | grep "Standard"
fi
```

### Verify Before Completing Task

```bash
#!/bin/bash
# Run before marking task complete

if [ ! -f "LESSONS_LEARNED.md" ]; then
    echo "⚠️  No standards file found"
    exit 1
fi

# Verify version is current
CURRENT_VERSION=$(grep "version:" LESSONS_LEARNED.md | head -1 | sed 's/.*"\([^"]*\)".*/\1/')
echo "📋 Standards version: $CURRENT_VERSION"

# Check all HIGH-priority standards
echo "🔍 Verifying HIGH-priority standards..."
if grep -q "Priority.*HIGH" LESSONS_LEARNED.md; then
    echo "✅ Standards are in place and ready to enforce"
else
    echo "⚠️  No HIGH-priority standards defined"
fi
```

---

## TypeScript/Node Integration

### Load and Validate

```typescript
import * as fs from "fs";
import * as yaml from "js-yaml";

interface LessonMetadata {
  version: string;
  last_updated: string;
  categories: string[];
}

interface Standard {
  name: string;
  standard: string;
  context: string;
  action: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
  enforced: "Manual" | "Automated" | "Recommended";
}

class ProjectStandards {
  private metadata: LessonMetadata;
  private standards: Standard[] = [];

  load(projectPath: string = "."): boolean {
    const filePath = `${projectPath}/LESSONS_LEARNED.md`;
    
    if (!fs.existsSync(filePath)) {
      return false;
    }

    const content = fs.readFileSync(filePath, "utf-8");
    const parts = content.split("---");
    
    if (parts.length >= 3) {
      this.metadata = yaml.load(parts[1]) as LessonMetadata;
      this.parseMarkdown(parts.slice(2).join("---"));
      return true;
    }

    return false;
  }

  private parseMarkdown(content: string): void {
    // Parse markdown sections to extract standards
    const standardRegex = /###\s+(.+?)\n([\s\S]*?)(?=###\s|$)/g;
    let match;

    while ((match = standardRegex.exec(content)) !== null) {
      const section = match[1];
      const text = match[2];
      
      // Extract standard fields (simplified)
      const standard = this.extractStandard(section, text);
      if (standard) this.standards.push(standard);
    }
  }

  private extractStandard(name: string, text: string): Standard | null {
    const standardMatch = text.match(/\*\*Standard\*\*:\s*(.+)/);
    const contextMatch = text.match(/\*\*Context\*\*:\s*(.+)/);
    const actionMatch = text.match(/\*\*Action\*\*:\s*(.+)/);
    const priorityMatch = text.match(/\*\*Priority\*\*:\s*(.+)/);

    if (!standardMatch) return null;

    return {
      name,
      standard: standardMatch[1],
      context: contextMatch?.[1] || "",
      action: actionMatch?.[1] || "",
      priority: (priorityMatch?.[1]?.toUpperCase() as any) || "MEDIUM",
      enforced: "Manual",
    };
  }

  getByCategory(category: string): Standard[] {
    // Filter standards by category (simplified)
    return this.standards;
  }

  getHighPriority(): Standard[] {
    return this.standards.filter((s) => s.priority === "HIGH");
  }

  printReport(): void {
    console.log(`📋 Project Standards (v${this.metadata.version})`);
    console.log(
      `ℹ️  Last updated: ${this.metadata.last_updated}\n`
    );

    const highPriority = this.getHighPriority();
    if (highPriority.length > 0) {
      console.log(`🔴 HIGH Priority (${highPriority.length}):`);
      highPriority.forEach((s) => console.log(`  - ${s.standard}`));
    }
  }
}

// Usage
const standards = new ProjectStandards();
if (standards.load(".")) {
  standards.printReport();
}
```

---

## Configuration File Integration

### Example: .copilot-config.json

```json
{
  "project_name": "my-project",
  "project_standards": {
    "enabled": true,
    "file": "LESSONS_LEARNED.md",
    "auto_load": true,
    "enforce_on_startup": true,
    "categories": [
      "prerequisites",
      "process",
      "quality-gates",
      "coding-standards"
    ]
  },
  "agent_instructions": {
    "before_task": "Load project standards from LESSONS_LEARNED.md and report which apply",
    "before_completion": "Verify all relevant standards were followed",
    "on_standards_conflict": "Ask user for clarification; do not override standards"
  }
}
```

### Example: package.json Scripts

```json
{
  "scripts": {
    "check-standards": "node scripts/check-standards.js",
    "lint-standards": "node scripts/lint-standards.js",
    "update-standards": "node scripts/update-standards.js"
  }
}
```

---

### Pre-commit Hook (Auto-Initialize)

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Auto-initialize if needed
if [ ! -f LESSONS_LEARNED.md ]; then
    python scripts/init_lessons.py
    git add LESSONS_LEARNED.md
fi

echo "Checking project standards..."
if grep -q "Priority.*HIGH" LESSONS_LEARNED.md; then
    echo "✓ High-priority standards exist"
fi

# Prevent commits that violate standards
if grep -q "DO NOT" LESSONS_LEARNED.md; then
    echo "⚠️  Review DON'Ts in LESSONS_LEARNED.md before committing"
fi
```

### CI/CD Integration

```yaml
# .github/workflows/validate-standards.yml
name: Validate Standards
on: [push, pull_request]

jobs:
  check-standards:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Initialize LESSONS_LEARNED.md if needed
        run: |
          if [ ! -f LESSONS_LEARNED.md ]; then
            echo "📝 Initializing standards file..."
            python scripts/init_lessons.py
            git add LESSONS_LEARNED.md
          fi
      
      - name: Validate standards file exists
        run: |
          if [ ! -f LESSONS_LEARNED.md ]; then
            echo "❌ LESSONS_LEARNED.md not found after initialization"
            exit 1
          fi
          echo "✓ Standards file found"
      
      - name: Check for HIGH-priority standards
        run: |
          if grep -q "Priority.*HIGH" LESSONS_LEARNED.md; then
            echo "✓ HIGH-priority standards defined"
            grep -c "Priority.*HIGH" LESSONS_LEARNED.md
          fi
      
      - name: Validate file syntax
        run: python scripts/validate.py LESSONS_LEARNED.md
      
      - name: Commit auto-initialized file (if needed)
        if: github.ref == 'refs/heads/main'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git diff --quiet && git diff --staged --quiet || \
            (git add LESSONS_LEARNED.md && \
             git commit -m "chore: initialize LESSONS_LEARNED.md" && \
             git push)
```

---

## Best Practices

1. **Load early** — Parse LESSONS_LEARNED.md at agent startup
2. **Report compliance** — Always show which standards were checked
3. **Don't ignore HIGH** — Never skip high-priority standards
4. **Ask on conflict** — If standards conflict with task requirements, ask the user
5. **Version awareness** — Check the version field; alert if it differs from expected
6. **Timestamp checks** — Warn if standards are stale (not updated recently)

