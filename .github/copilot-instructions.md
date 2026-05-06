# Copilot Instructions for my-skills Repository

This repository contains **reusable skills** — specialized tools that help LLMs (like Claude) accomplish specific tasks more effectively.

## Repository Structure

```
my-skills/
├── README.md                     # Skill catalog and overview
├── {skill-name}/
│   ├── SKILL.md                  # Main skill definition (required)
│   ├── scripts/                  # Optional: Python utilities
│   ├── agents/                   # Optional: Specific agent implementations
│   ├── references/               # Optional: Reference docs
│   ├── evals/                    # Optional: Test cases (evals.json format)
│   ├── assets/                   # Optional: Supporting files
│   └── LICENSE.txt               # Optional: License terms
└── .github/                      # Repository metadata
```

## High-Level Architecture

**Core Concept:** Each skill is a standalone, self-contained agent tool that solves a specific problem. Skills are designed to:

- Trigger on specific user phrases or contexts
- Provide step-by-step guidance for a task workflow
- Include helper scripts where needed (Python-based)
- Measure effectiveness through evaluation tests

**Skill Discovery:** Users and agents discover skills through:
1. The main README.md (catalog of all skills with descriptions)
2. Skill descriptions in SKILL.md frontmatter (used for triggering)
3. SKILL.md instructions that guide the agent through the workflow

## Key Conventions

### SKILL.md Format

Every skill has a `SKILL.md` file with required YAML frontmatter:

```markdown
---
name: skill-name
description: "Short description of what the skill does and WHEN to use it. Include specific trigger phrases and contexts. Make it 'pushy' — explain when this skill SHOULD be invoked, not just that it CAN be. For example: 'Use this skill ANY TIME the user mentions X, even if they don't explicitly ask for Y.'"
license: Optional - add if using non-standard license
compatibility: Optional - list required tools/dependencies
---

# Skill Name (title)

Rest of markdown with workflow, examples, etc.
```

**Important:** The `description` field is the primary triggering mechanism. It must include:
- What the skill does
- Specific phrases that should trigger it (e.g., "when the user mentions X, Y, or Z")
- Contexts where it applies
- Enough detail that agents understand when to invoke it

### Skill Description Strategy

Skill descriptions intentionally use inclusive language to reduce "undertriggering":
- ✅ "Use this skill **whenever** the user mentions..."
- ✅ "Use this skill **ANY TIME** the user mentions..."
- ✅ "Use this skill **even if** they don't explicitly ask for..."
- ❌ Avoid: "This skill can be used to..." (passive, doesn't trigger well)

### Script Organization

When a skill includes Python scripts, they're organized in `scripts/`:

```
skill-name/scripts/
├── __init__.py                      # Package marker
├── main_script.py                   # Primary functionality
├── utils.py                         # Shared utilities (if needed)
├── requirements.txt                 # Dependencies (if needed)
└── README.md                        # Usage docs (if complex)
```

Common patterns:
- Scripts use `scripts/utils.py` for shared parsing/validation
- Entry points are typically simple CLI interfaces
- Dependencies listed in `requirements.txt` (Python ecosystem)

### Evaluation Tests

Skills with objective, measurable outcomes include evals:

```
skill-name/evals/
└── evals.json                       # Array of test cases
```

Format:
```json
[
  {
    "name": "test_case_name",
    "input": { /* test input */ },
    "expected": { /* expected output */ },
    "description": "What this tests"
  }
]
```

**Running evals:**
```bash
# From a skill directory with evals
python ../skill-creator/scripts/run_eval.py --skill-path .
```

### Common Scripts

- `run_eval.py` — Test skill triggering and outputs against evals
- `init_lessons.py` — Initialize LESSONS_LEARNED.md template
- `validate.py` — Validate SKILL.md structure or file formats
- `package_skill.py` — Package skill for distribution

## Build, Test, and Lint

### Running Skill Evaluations

```bash
# Test a specific skill's evals
python skill-creator/scripts/run_eval.py --skill-path {skill-name}

# Run all evals
for skill in */; do
  python skill-creator/scripts/run_eval.py --skill-path "$skill"
done
```

### Validate SKILL.md Structure

```bash
# Check if SKILL.md has required fields
python skill-creator/scripts/quick_validate.py {skill-name}/SKILL.md
```

### Install Dependencies

```bash
# For MCP builder skill dependencies
pip install -r mcp-builder/scripts/requirements.txt
```

## Important Patterns

### 1. Skill Triggering Language

Skills must use explicit, inclusive trigger phrases in descriptions. Examples:

```markdown
# GOOD ✅
"Use this skill whenever the user mentions 'Connect', 'Connect review', 'performance review', or 'self-assessment'."

# GOOD ✅
"Use this skill ANY TIME a .xlsx file is involved — even if the extracted content will be used elsewhere."

# AVOID ❌
"This skill can help users work with Excel files."
```

### 2. Workflow Structure in SKILL.md

Most skills follow this pattern:

1. **Overview** — High-level purpose
2. **When to Use** — Trigger phrases and contexts
3. **Process/Workflow** — Step-by-step guidance
4. **Examples** — Concrete examples with before/after
5. **Integration** — How to use with other tools/agents
6. **Tips** — Best practices and edge cases

### 3. Multi-Phase Skills

Complex skills (like `skill-creator`, `mcp-builder`) break workflows into phases:

```markdown
## Phase 1: Planning
...
## Phase 2: Implementation
...
## Phase 3: Evaluation
...
```

This makes it easier for agents to track progress and resume mid-workflow.

### 4. Documentation in Skills

- **SKILL.md** — Skill definition and workflow (primary)
- **README.md** (in skill folder) — Quick-start guide, common questions
- **references/** — Detailed reference docs or API specs
- **AGENTS.md** or similar — Agent-specific implementations (if applicable)

### 5. Nested Workflows

Some skills invoke other skills. For example, `skill-creator` may use `lessons-learned` to capture standards. When nesting:

- Clearly document the dependency
- Assume the invoked skill is available
- Pass context so the invoked skill understands its role

## When Working on This Repository

1. **Adding a new skill:**
   - Create `{skill-name}/` folder
   - Write `SKILL.md` with required YAML frontmatter
   - If including tests, create `evals/evals.json`
   - If including scripts, add to `scripts/` with `__init__.py`

2. **Modifying a skill:**
   - Update `SKILL.md` — frontmatter triggers description changes
   - Test trigger phrases by running evals
   - Keep backward compatibility if the skill is public-facing

3. **Testing trigger accuracy:**
   - Use `skill-creator/scripts/run_eval.py` to test if descriptions trigger appropriately
   - Iterate on description language until triggering is consistent

4. **Packaging/Distribution:**
   - Use `skill-creator/scripts/package_skill.py` if the skill is meant for external distribution
   - Include LICENSE.txt for non-standard licenses

## File Conventions

- **Python** — All scripts use Python 3.8+, type hints where helpful, standard library first
- **Names** — Skill folder names are kebab-case (e.g., `mcp-builder`, `skill-creator`)
- **YAML** — Use simple, flat structure in SKILL.md frontmatter (no nested complexity)
- **Markdown** — Follow standard conventions; use headers to structure SKILL.md logically

## Common Questions

**Q: How do I know if a skill should have evals?**
A: If the skill has objectively measurable outcomes (file transformations, data extraction, code generation), include evals. If it's subjective (writing style, creative output), evals are optional.

**Q: Where should I put helper utilities?**
A: In `scripts/utils.py`. Import with `from scripts.utils import ...` (Python path relative to skill root).

**Q: Should I put everything in SKILL.md?**
A: Keep SKILL.md focused on workflow and triggering. Move detailed reference docs to `references/` and quick-start guides to README.md.

**Q: How do I handle dependencies?**
A: List them in `scripts/requirements.txt`. Document installation instructions in the skill's workflow section if needed.
