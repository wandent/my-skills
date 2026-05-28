---
name: document-trace-footer
description: Automatically append a concise, structured, truthful "Method Summary" footer to EVERY generated document or analysis by default. Use this skill ANY TIME the output is a report, analysis, memo, recommendation, assessment, writeup, or any generated document-like response, even if the user did not explicitly ask for a footer. Also use when users ask for transparency, traceability, explainability, auditability, assumptions used, criteria used, or "how this was produced."
---

# Document Trace Footer

Produce the requested main content first, then append a short **Method Summary** footer at the bottom of the output.

The footer gives readers a clean view of:
1. Which instructions shaped the result
2. How the reasoning was carried out (high level)
3. Which rules, constraints, and parameters were applied

## Core behavior

1. Treat this as **default-on behavior** for any generated document or analysis.
2. Deliver the main requested content completely.
3. Add the footer at the end under `## Method Summary`.
4. Keep the footer concise, structured, and factual.
5. Include only information that was actually used.
6. If information is unknown, write `Not specified` instead of inventing details.

## Opt-out rule

Only skip the footer if the user explicitly asks to omit it (for example: "no method summary", "do not include footer", or "output only main content").

## Footer template

Always use this structure (adapted to the task context):

```markdown
## Method Summary
### Instructions applied
- [Instruction or requirement]
- [Instruction or requirement]

### Reasoning approach
- [How the task was broken down]
- [How evidence/options were evaluated]

### Rules and constraints used
- [Policy, format, scope, compliance, style, or technical constraints]

### Parameters and assumptions considered
- [Input parameters, thresholds, time ranges, data sources, or assumptions]

### Exclusions or non-goals
- [What was intentionally out of scope]
```

## Reasoning summary guidance

Summarize reasoning at a high level. Focus on process quality, not hidden internal deliberation.

Good examples:
- "Compared the provided options against the stated selection criteria and ranked by fit."
- "Prioritized recommendations by impact, implementation effort, and stated timeline."

Avoid:
- Raw chain-of-thought transcripts
- Unverifiable claims like "all possibilities were evaluated"
- Vague text like "used advanced reasoning"

## Truthfulness rules

- Do not claim a rule or parameter was used if it was not.
- Do not cite tools, files, or data sources that were not actually used.
- Keep phrasing specific enough to be auditable by a reader.

## Length rules

- Target 6-14 bullet points total across all footer sections.
- Keep each bullet to one line when possible.
- Prefer concrete nouns and numbers over abstract wording.

## Output-specific adaptation

- **Formal reports/memos:** keep professional tone and preserve section headers.
- **Short analyses:** compress to fewer bullets, but keep all five sections.
- **Tabular deliverables:** include thresholds, filters, and calculation logic in "Parameters and assumptions considered."

## Examples

**Example 1**
Input: "Analyze these vendor options and recommend one."

Footer excerpt:
- Instructions applied: "Recommend one option with justification."
- Reasoning approach: "Scored each vendor against cost, fit, and migration risk."
- Rules and constraints used: "Preferred options compatible with existing stack."

**Example 2**
Input: "Generate a project status summary for leadership."

Footer excerpt:
- Instructions applied: "Use executive-level tone and concise structure."
- Parameters and assumptions considered: "Time window: current sprint; unresolved blockers flagged as open risks."
- Exclusions or non-goals: "No root-cause deep dive included."
