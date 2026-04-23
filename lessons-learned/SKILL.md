---
name: lessons-learned
description: "Capture and document standards from conversation feedback into a machine-readable LESSONS_LEARNED.md file. USE THIS SKILL whenever the user is providing standards, correcting approach, steering analysis, or establishing quality criteria across ANY domain — coding conventions, testing, architecture, security, UX, deployment, debugging, data handling, communication style, team processes, or any other topic. Triggers include: 'make sure to', 'always check', 'never do X', 'I prefer', 'from now on', 'test first', 'verify before', 'that's not how we do it', 'I told you before', course corrections mid-workflow, repeated emphasis, contradiction of prior direction, or any instruction that establishes a pattern or gate. Also use when reading back over a long conversation to extract accumulated guidance. Runs continuously — every new lesson appends without overwriting prior ones."
---

# Lessons Learned Capture & Documentation

## Overview

This skill captures guidance, standards, and process patterns that emerge from conversation feedback and documents them in a format that both humans and coding agents can read and follow.

It works across **all domains** — there is no restriction on what kind of lesson can be captured. Whether the user is directing coding style, debugging approaches, security practices, UX patterns, data handling, deployment rules, communication preferences, or team processes — all of it is fair game.

**Key purposes:**

- Read conversation history and extract every lesson the user has taught or implied
- Extract and preserve user-directed standards from any domain
- Maintain a living document that updates as the project evolves
- Enable coding agents (Copilot, CLI, frameworks) to understand project-specific rules
- Serve as a config file embedded in the project structure

---

## Reading Conversation History

Before capturing a lesson, re-read the conversation from the beginning and identify **all** directional signals — not just the most recent one. Ask yourself: has the user, at any point:

| Signal type              | What it looks like                                                   |
| ------------------------ | -------------------------------------------------------------------- |
| **Explicit rule**        | "Always do X", "Never do Y", "Make sure to Z"                        |
| **Correction**           | "No, that's wrong — do it this way", "I said not to do that"         |
| **Preference statement** | "I prefer X over Y", "We use X here, not Y"                          |
| **Steering mid-task**    | "Wait, before you continue — also check X"                           |
| **Repeated instruction** | User says the same thing twice across different turns                |
| **Frustration signal**   | "I already told you", "Again, please don't do this"                  |
| **Approval of approach** | "Yes, exactly like that — remember this pattern"                     |
| **Named example**        | Describes a specific scenario and how they'd want it handled         |
| **Constraint**           | "We can't use X because of Y" — captures a constraint as a standard  |
| **Quality gate**         | "Don't call this done until you've verified X"                       |
| **Anti-pattern**         | "That's exactly what we don't want" — captures negative examples too |

When capturing, **don't only capture the last lesson** — scan the entire conversation history and extract all lessons found, organizing them by category.

---

## Recognizing Lesson Signals

### Phrase patterns to watch for

```
"always / never / don't / make sure / you must / be sure to / check first"
"I prefer / we prefer / we use / our standard is / our convention is"
"from now on / going forward / in this project"
"wait / hold on / before you continue / actually / no — "
"that's not right / that's wrong / I said not to"
"I already mentioned / I told you / as I said"
"yes, exactly like that / good, remember this"
"we can't use X because / X is not allowed / avoid X"
"don't call it done until / task is only complete when"
```

### Implied signals (no explicit phrase required)

Sometimes a lesson is implicit in the user's correction or action, not stated as a rule. Example:

> User uploads a `.env` file and says: "Use these values for config."

The lesson is: *"Project uses a `.env` file for config values — do not hardcode them."* Capture even when not explicitly stated as a rule.

---

## Categories

Categorize each lesson into the most appropriate section. If it spans two, pick the primary and add a cross-reference note.

| Category             | What goes here                                                               |
| -------------------- | ---------------------------------------------------------------------------- |
| **prerequisites**    | Tool installation, environment setup, dependencies, version requirements     |
| **process**          | Task ordering, workflow steps, how to approach problems, checklists          |
| **quality-gates**    | What "done" means, validation steps, review criteria, testing requirements   |
| **coding-standards** | Naming conventions, code style, patterns to use or avoid, language choices   |
| **architecture**     | System design choices, component boundaries, data flow, integration patterns |
| **security**         | Auth requirements, data handling, credential management, access controls     |
| **testing**          | Test structure, coverage requirements, what/how to test, tooling preferences |
| **data-handling**    | Schema conventions, transformation rules, validation, storage choices        |
| **deployment**       | Release process, environment rules, CI/CD gates, rollback procedures         |
| **communication**    | Output format, tone, report structure, how to present results                |
| **ux-design**        | UI patterns, accessibility, user flow priorities, design rules               |
| **debugging**        | How to diagnose issues, what to log, trace approaches, escalation rules      |

---

## Quick Reference

| When to Capture   | Domain  | Example                                                                    |
| ----------------- | ------- | -------------------------------------------------------------------------- |
| **Prerequisites** | Any     | "Make sure Playwright/Chrome is installed and tested before saying ready"  |
| **Coding style**  | Code    | "We use `async/await` only — no `.then()` chains"                          |
| **Architecture**  | Design  | "All API calls go through the service layer, not directly from components" |
| **Security**      | Auth    | "Never log tokens or PII — even in debug output"                           |
| **Testing**       | QA      | "Every new function needs a unit test before merging"                      |
| **Data handling** | DB      | "Dates must always be stored as UTC ISO 8601"                              |
| **Correction**    | Any     | "No — use the existing helper, don't write a new one"                      |
| **Quality gate**  | Process | "Don't mark complete until the user has seen the output"                   |
| **UX**            | Design  | "Always show a loading state — don't let the UI go blank"                  |
| **Deployment**    | DevOps  | "Never push directly to main — always use a feature branch"                |
| **Debugging**     | Dev     | "Always check logs in CloudWatch first, not local console"                 |
| **Communication** | Output  | "Keep summaries under 5 bullet points — don't over-explain"                |

---

## File Structure

### Location

```
your-project/
├── LESSONS_LEARNED.md (embedded config + documentation)
└── .lessons-learned/
    └── metadata.json (optional: tracks updates and history)
```

### Format

LESSONS_LEARNED.md uses a hybrid format: YAML front matter (for machine parsing) + Markdown body (for human reading).

```markdown
---
version: "1.0"
last_updated: "2026-04-22T14:30:00Z"
categories:
  - prerequisites
  - process
  - quality-gates
  - coding-standards
  - architecture
  - security
  - testing
  - data-handling
  - deployment
  - communication
  - ux-design
  - debugging
---

# Lessons Learned

## Prerequisites & Validation

### Tool Installation Requirements
- **Standard**: Verify all prerequisites are installed and working before claiming task readiness
- **Context**: User expects tools to be installed and tested before proceeding
- **Action**: 1) List required tools, 2) Verify each installed, 3) Test on sample, 4) Confirm readiness
- **Priority**: HIGH
- **Enforced**: Manual verification required

---

## Process Standards

### Validation Before Completion
- **Standard**: Never mark a task complete without testing it
- **Context**: Quality assurance is non-negotiable
- **Action**: Run all verifications before final sign-off
- **Priority**: HIGH

---

## Coding Standards

(Standards added here as they emerge)

---

## How Agents Should Use This File

1. **Read on startup** — Load this file when beginning work on the project
2. **Check relevant sections** — Find sections matching the current task type
3. **Follow listed actions** — Apply each standard before proceeding
4. **Report compliance** — Indicate in work summary which standards were checked
5. **Flag violations** — If unable to follow a standard, explain why and propose alternative

### Machine-Readable Parsing

Agents can parse the YAML front matter to categorize standards:
```yaml
categories: [prerequisites, process, quality-gates, coding-standards, architecture, security, ...]
```

Each section follows this structure for consistent parsing:

```markdown
### Section Title
- **Standard**: (What rule to follow)
- **Context**: (Why it matters)
- **Action**: (How to implement it)
- **Priority**: (HIGH/MEDIUM/LOW)
- **Enforced**: (Type of enforcement: Manual/Automated/Recommended)
```

---

## Workflow for Capturing Lessons

### Step 0: Auto-Initialize (First Time Only)

**Automatic on first use:**

1. Check if `LESSONS_LEARNED.md` exists in project root
2. If NOT found:
   - Create the file from built-in template
   - Initialize with metadata (version 1.0, current timestamp, categories)
   - Add placeholder sections (Prerequisites, Process, Quality Gates, Coding Standards)
   - Confirm file creation to user
3. If found:
   - Skip initialization, proceed to capture

**How it works:**

- Script `scripts/init_lessons.py` handles auto-creation
- Uses template from `LESSONS_LEARNED.md.template`
- Runs automatically before first lesson capture
- User never manually creates the file

**User sees:**

```
📝 Initializing LESSONS_LEARNED.md (first time)...
✅ File created: LESSONS_LEARNED.md
   Ready to capture your first lesson.
```

### Step 1: Identify During Conversation

Scan the **full conversation history** from the beginning — not just the most recent message. Look for any point where the user:

- **Corrects direction** — "No — do it this way", "That's not what I meant", "Actually, use X instead"
- **States a rule** — "Always/never/make sure/be sure to/don't..."
- **Establishes a preference** — "I prefer X", "We use X here", "Our standard is X"
- **Steers mid-task** — "Wait, before you continue — also check X"
- **Repeats an instruction** — Same guidance given across two or more turns (always HIGH priority)
- **Expresses frustration** — "I already told you", "Again, please don't" (signals a persistent gap)
- **Approves a pattern** — "Yes, exactly like that — remember this"
- **Names a constraint** — "We can't use X because of Y"
- **Sets a quality gate** — "Don't call this done until you've verified X"
- **Implies a standard via action** — Uploads a config file, pastes a template, references a pattern

If more than one lesson is found in the history, capture **all of them** in a single update, not just the one that triggered the current turn.

### Step 2: Extract & Categorize

When identified, extract:

1. **The standard** (what should be done)
2. **The context** (why or when)
3. **Specific actions** (how to implement)
4. **Priority** (how critical)
5. **Enforcement type** (manual check, automated test, or advisory)

### Step 3: Update LESSONS_LEARNED.md

- Auto-initialize if file doesn't exist (see Step 0)
- Append to relevant section
- Update timestamp and version
- Preserve all previous entries (never delete unless explicitly asked)
- Cross-reference related standards if applicable

### Step 4: Confirm with User

After capturing, summarize what you added:

```
✓ Added to LESSONS_LEARNED.md under [Category]:
  - [Standard description]
  - Action: [How it will be applied]
```

---

## Examples

The Playwright example is one of many. Below are diverse examples across different domains.

---

### Example 1: Prerequisites (Tool Setup)

**User says:** "Make sure the playwright/chrome is installed and works. Test it on a sample website before saying the task is ready."

**Category:** `prerequisites`

**Captured as:**

```markdown
## Prerequisites & Validation

### Tool Installation Requirements
- **Standard**: Verify all prerequisites are installed and working before claiming task readiness
- **Context**: User expects tools like Playwright/Chrome to be installed and tested
- **Action**: 1) List required tools, 2) Verify each is installed, 3) Test on sample input, 4) Only then confirm readiness
- **Priority**: HIGH
- **Enforced**: Manual verification required
```

---

### Example 2: File Safety (Coding)

**User says:** "Wait, before you create the file, check if there's already one. Don't overwrite existing work."

**Category:** `coding-standards`

**Captured as:**

```markdown
## Coding Standards

### File Safety
- **Standard**: Always check if a file exists before creating or overwriting
- **Context**: Prevent accidental loss of existing work
- **Action**: Before creating a file, search for it first; if it exists, ask before overwriting
- **Priority**: HIGH
- **Enforced**: Manual check required
```

---

### Example 3: Async Style Correction

**User says mid-conversation:** "No — we don't use `.then()` chains here. Switch to async/await throughout."

**Category:** `coding-standards`

**Captured as:**

```markdown
### Async Pattern
- **Standard**: Use `async/await` exclusively — never `.then()` or `.catch()` chains
- **Context**: Team convention; inconsistent async patterns cause review failures
- **Action**: Refactor any `.then()` chains to async/await before submitting code
- **Priority**: HIGH
- **Enforced**: Code review gate
```

---

### Example 4: Architecture Direction

**User says:** "API calls should never go directly from the component. Everything goes through the service layer."

**Category:** `architecture`

**Captured as:**

```markdown
## Architecture

### Service Layer Enforcement
- **Standard**: All API calls must go through the service layer, not directly from UI components
- **Context**: Separation of concerns; direct calls bypass logging, error handling, and auth
- **Action**: Move any fetch/axios/http call in a component to a service file
- **Priority**: HIGH
- **Enforced**: Manual code review
```

---

### Example 5: Security Constraint

**User says:** "Don't ever log the access tokens — even in debug mode. We had an incident because of that."

**Category:** `security`

**Captured as:**

```markdown
## Security

### No Token Logging
- **Standard**: Never log access tokens, refresh tokens, API keys, or any credentials — in any environment
- **Context**: Past security incident caused by tokens appearing in debug logs
- **Action**: Before any log statement, verify output contains no auth values; use `[REDACTED]` if needed
- **Priority**: HIGH
- **Enforced**: Automated lint rule + manual review
```

---

### Example 6: Data Handling

**User says:** "Dates need to be stored as UTC ISO 8601 strings — not Unix timestamps, not local time."

**Category:** `data-handling`

**Captured as:**

```markdown
## Data Handling

### Date Format Standard
- **Standard**: All dates must be stored and transmitted as UTC ISO 8601 strings (e.g. `2026-04-22T14:30:00Z`)
- **Context**: Prevents timezone bugs and inconsistency across services
- **Action**: Convert all date values to `.toISOString()` before storage or API response
- **Priority**: HIGH
- **Enforced**: Input validation + schema check
```

---

### Example 7: Testing Requirement

**User says:** "Every new function you add needs a unit test. Don't create untested code."

**Category:** `testing`

**Captured as:**

```markdown
## Testing

### Unit Test Coverage Requirement
- **Standard**: Every new function must have at least one unit test before it is considered complete
- **Context**: Untested code leads to silent regressions; user enforces test-first culture
- **Action**: After writing a function, immediately write a test covering the happy path and one edge case
- **Priority**: HIGH
- **Enforced**: PR review gate — no merge without tests
```

---

### Example 8: Deployment Gate

**User says:** "Never push directly to main. Feature branches only, always go through a PR."

**Category:** `deployment`

**Captured as:**

```markdown
## Deployment

### Branch Protection
- **Standard**: No direct pushes to `main`; all changes must go through a feature branch and PR
- **Context**: Protects production branch; enables review and CI checks
- **Action**: Create a branch (`feature/`, `fix/`, `chore/`), push changes, open a PR; never `git push origin main`
- **Priority**: HIGH
- **Enforced**: Repository branch protection rule + team convention
```

---

### Example 9: UX Pattern

**User corrects a UI implementation:** "Don't let the screen go blank while loading. Always show a spinner or skeleton."

**Category:** `ux-design`

**Captured as:**

```markdown
## UX Design

### Loading State Requirement
- **Standard**: All async data loads must show a loading indicator (spinner or skeleton screen)
- **Context**: Blank screens confuse users and appear broken
- **Action**: Wrap all async renders in a loading state; default to skeleton or spinner until data resolves
- **Priority**: MEDIUM
- **Enforced**: UI review
```

---

### Example 10: Debugging Approach

**User says:** "When something breaks in prod, check CloudWatch first — not local logs."

**Category:** `debugging`

**Captured as:**

```markdown
## Debugging

### Production Debugging Source
- **Standard**: For production issues, check AWS CloudWatch logs first — local logs do not mirror prod
- **Context**: Local setup differs from prod; misleading local logs have caused wasted debugging time
- **Action**: 1) Open CloudWatch, 2) Filter by service + time window, 3) Only replicate locally after identifying the issue
- **Priority**: MEDIUM
- **Enforced**: Team convention
```

---

### Example 11: Communication Style (Implicit Steering)

**Scenario:** User repeatedly cuts off long explanations and says "just give me the bullet points."

**Category:** `communication`

**Captured as:**

```markdown
## Communication

### Output Brevity
- **Standard**: Keep summaries concise — bullet points only; limit to 5 bullets maximum
- **Context**: User prefers brief, scannable output; long prose has been cut short multiple times
- **Action**: Convert any paragraph explanation to bullets; remove anything not actionable or essential
- **Priority**: MEDIUM
- **Enforced**: Conversational preference
```

---

### Example 12: Repeated Correction (History Scan)

**Scenario:** At turn 3, user said "don't use `var`." At turn 12, user said again "I see you're still using `var` — stop."

**Category:** `coding-standards`

**How to detect:** When scanning history, match similar corrections across turns. A repeated correction is always HIGH priority.

**Captured as:**

```markdown
### Variable Declaration
- **Standard**: Never use `var` — use `const` by default, `let` when reassignment is needed
- **Context**: User corrected this twice across the conversation; persistent pattern requiring explicit standard
- **Action**: Search for `var` in any generated code before submitting; replace with `const`/`let`
- **Priority**: HIGH
- **Enforced**: Linter rule + manual check
- **Note**: Repeated correction — flagged as high friction pattern
```

---

### Example 13: Implied Constraint (No Explicit Rule Stated)

**Scenario:** User uploads `.env` file and says "Use these values." — no explicit rule is stated.

**Category:** `coding-standards` / `security`

**How to detect:** Implied standard from user action + instruction. Even without "always/never" phrasing, the intent is clear.

**Captured as:**

```markdown
### Config Source
- **Standard**: Configuration values must come from the `.env` file — never hardcoded in source
- **Context**: User provided `.env` as the config source; hardcoded values would be inconsistent and insecure
- **Action**: Reference `process.env.VAR_NAME` (or equivalent); never paste values directly into code
- **Priority**: HIGH
- **Enforced**: Code review
```

---

## Maintenance

### Auto-Initialization Script

Run before first use in a project:

```bash
python scripts/init_lessons.py
```

Options:

```bash
# Initialize in current directory
python scripts/init_lessons.py

# Initialize in specific project directory
python scripts/init_lessons.py /path/to/project

# Force re-initialize (overwrites existing)
python scripts/init_lessons.py --force

# Show what would be created (dry-run)
python scripts/init_lessons.py --dry-run
```

### Version Updates

- Increment version number in YAML front matter when adding new standards
- Update `last_updated` timestamp
- Keep a change log (optional) at the end for history

### Review Cycle

- Review LESSONS_LEARNED.md at project checkpoints (daily, sprint end, etc.)
- Remove standards that are no longer relevant (with user approval)
- Consolidate similar standards to reduce redundancy
- Add new standards as they emerge

### Project Configuration Integration

Embed LESSONS_LEARNED.md as a config file that agents can discover:

```bash
# Example: Agent startup checks for this file
if [ -f LESSONS_LEARNED.md ]; then
  echo "Project standards found. Loading..."
  # Agent parses YAML and enforces standards
fi
```

Or in agent context:

```json
{
  "project_config": {
    "standards_file": "LESSONS_LEARNED.md",
    "auto_load": true,
    "enforce_on_startup": true
  }
}
```

---

## Tips for Effective Use

1. **Be specific** — "Always check X" is better than "Be careful"
2. **Link to context** — Include the "why" so agents understand intent
3. **Actionable steps** — List concrete steps, not vague guidelines
4. **Prioritize ruthlessly** — Mark only truly critical items as HIGH
5. **Evolve, don't accumulate** — Consolidate and remove outdated standards regularly
6. **Test your standards** — If a standard emerges mid-project, verify it actually improves outcomes before committing it permanently
