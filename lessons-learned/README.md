# Lessons Learned Skill - Quick Start Guide

## What This Skill Does

The **lessons-learned** skill captures standards and guidance from your conversations with coding agents and documents them in a machine + human readable `LESSONS_LEARNED.md` file. This file can then be loaded by other agents (GitHub Copilot, CLI tools, frameworks) to automatically enforce project standards.

**Auto-initialization:** The file is automatically created on first use — no manual setup required.

---

## When to Use This Skill

**Trigger phrases from the user:**
- ✓ "Always check X before Y"
- ✓ "Make sure to test first"
- ✓ "Never overwrite files without asking"
- ✓ Course corrections: "Actually, do it this way instead"
- ✓ Emphasis: "This is critical/non-negotiable"
- ✓ Process patterns: "Verify prerequisites before saying task is ready"

---

## How It Works

### 1. Conversation Context
As you work with the user, you notice when they:
- Provide explicit instructions
- Correct your approach
- Establish quality criteria
- Emphasize a practice pattern

### 2. Auto-Initialize (First Time)
When you identify the first standard to capture:
- Check if `LESSONS_LEARNED.md` exists
- If NOT found: automatically create from template (happens automatically)
- File is ready to use
- If found: skip to step 3

**What user sees:**
```
📝 Initializing LESSONS_LEARNED.md (first time)...
✅ File created: LESSONS_LEARNED.md
   Ready to capture your first lesson.
```

### 3. Extract & Capture
When identified, you extract:
- **Standard**: What should be done
- **Context**: Why it matters
- **Action**: How to implement it (concrete steps)
- **Priority**: HIGH / MEDIUM / LOW
- **Enforced**: Manual / Automated / Recommended

### 4. Update LESSONS_LEARNED.md
- Append to relevant category section
- Preserve all existing standards (never delete)
- Update YAML metadata (version + timestamp)
- Confirm with the user what was added

### 5. Agents Read & Enforce
Other agents automatically:
- Load the file on startup (auto-initializes if missing)
- Parse standards by category
- Apply HIGH-priority standards first
- Report compliance in their summary

---

## File Structure

```
your-project/
├── LESSONS_LEARNED.md          # Main standards file (embedded config + docs)
├── .lessons-learned/           # Optional: metadata and history
│   └── metadata.json
└── .copilot-config.json        # Optional: project-wide agent config
```

### LESSONS_LEARNED.md Format

```markdown
---
version: "1.0"
last_updated: "2026-04-22T14:30:00Z"
categories: [prerequisites, process, quality-gates, coding-standards]
---

# Lessons Learned

## Category Name

### Standard Title
- **Standard**: What to do
- **Context**: Why it matters
- **Action**: How to do it
- **Priority**: HIGH/MEDIUM/LOW
- **Enforced**: Manual/Automated/Recommended
```

---

## Example: Playwright Prerequisites

**User says:**
```
"Ok, make sure the playwright/chrome is installed and works. Test it on a sample 
website of your choice, you need to record on the lessons learned that the user 
expects that the pre-requisites are installed, and confirm by testing them 
before saying the task is ready."
```

**Captured as:**
```markdown
## Prerequisites & Validation

### Installation & Testing Requirements
- **Standard**: Verify all prerequisites are installed before claiming task readiness
- **Context**: User expects pre-requisites (Playwright/Chrome) to be installed and working
- **Action**: Test prerequisites on a sample website before confirming task is ready
- **Priority**: HIGH
- **Enforced**: Manual verification required

### How to Check Prerequisites
1. List all required tools/libraries for the task
2. Verify each one is installed and accessible
3. Run a quick test on sample data (website, file, etc.)
4. Only then confirm readiness and proceed
```

---

## Integration with Agents

### For GitHub Copilot Users
Add to your system prompt or context:
```
Before starting work, load LESSONS_LEARNED.md and report which standards apply.
Follow all HIGH-priority standards. Report compliance in your summary.
```

### For Project Config
Create `.copilot-config.json`:
```json
{
  "project_standards": {
    "file": "LESSONS_LEARNED.md",
    "auto_load": true,
    "enforce_on_startup": true
  }
}
```

### For Bash/CLI
```bash
if [ -f "LESSONS_LEARNED.md" ]; then
  echo "Loading project standards..."
  grep "Priority.*HIGH" LESSONS_LEARNED.md
fi
```

---

## Workflow Summary

| Step | Action | Output |
|------|--------|--------|
| 1 | User provides direction during conversation | Observation noted |
| 2 | Identify standard/pattern/correction | Extracted intent |
| 3 | Auto-initialize file if needed | File created (first time only) |
| 4 | Add to LESSONS_LEARNED.md under category | File updated |
| 5 | Update YAML (version + timestamp) | Metadata current |
| 6 | Confirm with user | User sees what was captured |
| 7 | Agent loads on next task | Standards enforced |

---

## Manual Initialization (Optional)

If you want to initialize the file manually before capturing standards:

```bash
# Initialize in current directory
python scripts/init_lessons.py

# Initialize in specific project
python scripts/init_lessons.py /path/to/project

# Preview without creating
python scripts/init_lessons.py --dry-run

# Force re-initialize (overwrite existing)
python scripts/init_lessons.py --force
```

**Note:** This is optional — agents will auto-initialize automatically when needed.

---

## Key Benefits

✅ **Machine-readable** — Agents can parse and enforce automatically  
✅ **Human-friendly** — Clear Markdown format for quick scanning  
✅ **Continuous** — Updates as project evolves without losing history  
✅ **Config-embedded** — Can be part of project configuration  
✅ **Priority-aware** — Agents focus on HIGH-priority standards first  
✅ **Multi-category** — Organize standards by process type  
✅ **Traceable** — Version + timestamp show evolution  

---

## Common Patterns

### Pattern 1: Prerequisites Verification
```markdown
### Installation Check
- **Standard**: Verify all prerequisites before claiming readiness
- **Context**: Missing tools cause task failure
- **Action**: (1) List tools, (2) Check each installed, (3) Test on sample
- **Priority**: HIGH
- **Enforced**: Manual verification required
```

### Pattern 2: File Safety
```markdown
### Check Before Overwriting
- **Standard**: Never overwrite files without confirmation
- **Context**: Prevent loss of existing work
- **Action**: Search for file first; ask before overwriting
- **Priority**: HIGH
- **Enforced**: Manual check required
```

### Pattern 3: Quality Gate
```markdown
### Validation Before Completion
- **Standard**: Never mark task complete without testing
- **Context**: Quality assurance is non-negotiable
- **Action**: Run all verification steps before sign-off
- **Priority**: HIGH
- **Enforced**: Manual verification required
```

---

## Tips for Success

1. **Be specific** — "Always check X" beats "Be careful"
2. **Link to context** — Include the "why"
3. **Actionable steps** — List concrete how-tos
4. **Prioritize ruthlessly** — Only truly critical items get HIGH
5. **Review regularly** — Consolidate and remove outdated standards
6. **Evolve** — Standards should improve over time, not accumulate

---

## File Locations in Workspace

```
c:\Users\wandent\.my-skills\lessons-learned\
├── SKILL.md                           # Main skill definition
├── LESSONS_LEARNED.md.template        # Template for new projects
├── LICENSE.txt                        # Licensing terms
├── references/
│   └── agent-integration.md           # How agents load/parse the file
└── evals/
    └── evals.json                     # Test cases for validation
```

Use `LESSONS_LEARNED.md.template` as a starting point for new projects. Copy it to your project root as `LESSONS_LEARNED.md` and update standards as the project evolves.

