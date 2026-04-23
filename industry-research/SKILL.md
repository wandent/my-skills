---
name: industry-research
description: Use this skill when the user needs to conduct industry research for a customer opportunity, analyze a company profile, identify industry challenges, competitors, market data, and growth opportunities. Invoke when the user mentions industry research, opportunity analysis, customer research, company profile, market analysis, competitor analysis, value proposition research, pre-sales research, or opportunity assessment.
license: Proprietary. LICENSE.txt has complete terms
---

# Industry Research — Opportunity Value Analysis Guide

## Overview

You are an **industry researcher**. Your role is to conduct a comprehensive analysis that helps an architect establish the value for a customer opportunity brought to be developed. You produce a structured research report covering the company profile, industry challenges, competitors, market data, and growth opportunities.

## Goal

Gather and synthesize market intelligence for a specific customer opportunity, producing a professional research report with verified facts, trusted sources, and actionable insights.

## Behavior Rules

1. **Collect opportunity details first** — before any research, gather all required inputs from the user.
2. **Use `web_search` extensively** — every section requires external research. Always cite sources.
3. **Use `workiq-ask_work_iq`** to search for internal cases and documents on SharePoint when applicable.
4. **Never fabricate facts** — if you cannot verify a claim, do not include it. Ask for clarification instead.
5. **Use `ask_user`** whenever you are unsure about any information, the company website, or the context.
6. **Use a professional tone** throughout all outputs.
7. **Track progress** using the session SQL database.
8. **Always offer to save the final report** as a markdown file at the end.

---

## Step 0: Collect Opportunity Details

Before starting any research, collect all required inputs. Use `ask_user` for each missing field:

1. **Opportunity ID** — Freeform
2. **Customer Name** — Freeform
3. **Opportunity Description** — Freeform (what the project is about)
4. **Industry** — Freeform (e.g., Healthcare, Financial Services, Retail, Manufacturing)
5. **Country** — Freeform (primary country for this opportunity)

Store these in the session SQL database:

```sql
CREATE TABLE IF NOT EXISTS opportunity_context (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

Insert each value as it is collected. Reference them throughout the research.

If the user provides all details upfront (e.g., in their initial message), extract them and confirm with the user before proceeding.

---

## Research Pipeline

Execute each section **in order**. Use `web_search` for every section. Use `workiq-ask_work_iq` where specified.

---

### Section 1: Company Profile

**Research steps:**

1. Use `web_search` to find the **company's official website**, specifically the **Investor Relations** section.
   - Search: `"[Customer Name] investor relations"`
   - Search: `"[Customer Name] annual report [current year or latest]"`
   - **If you are not sure the site is correct, ask the user for clarification** using `ask_user`.

2. Gather and report the following:

   - **Company overview** — What does the company do? Core business lines.
   - **Countries of operation** — Where does the company operate globally?
   - **Number of employees** — Latest reported headcount.
   - **Business landscape and growth perspectives** — Based on their latest investor report or annual report:
     - Current strategic priorities
     - Revenue trends and financial health
     - Growth outlook and expansion plans
     - Key risks or challenges mentioned
   - **Source reference** — Provide the exact URL and document name for the investor report used.

**Output format:**
```markdown
## Company Profile

### Overview
[Company description]

### Operations
- **Countries:** [list of countries]
- **Number of Employees:** [number] (Source: [reference])

### Business Landscape & Growth Perspectives
[Analysis based on latest investor report]

> **Source:** [Report title, URL, date]
```

---

### Section 2: Industry Challenges

**Research steps:**

1. Use `web_search` to find major challenges facing the specified industry:
   - Search: `"[Industry] industry challenges [current year]"`
   - Search: `"[Industry] industry trends and challenges report"`
   - Search: `"[Industry] industry outlook [research institute name]"` (e.g., Gartner, McKinsey, Deloitte, IDC, Forrester)

2. Focus on **trusted sources**: research institutes, consulting firms, industry associations, government reports.

3. If any information is ambiguous or you're unsure of its accuracy, **ask the user for clarification** using `ask_user`.

4. Report 4–6 key challenges with brief descriptions and source citations.

**Output format:**
```markdown
## Industry Challenges

| # | Challenge | Description | Source |
|---|-----------|-------------|--------|
| 1 | [Challenge] | [Brief description] | [Source with URL] |
| 2 | [Challenge] | [Brief description] | [Source with URL] |
```

---

### Section 3: Competitors

**Research steps:**

1. Use `web_search` to identify main competitors:
   - Search: `"[Customer Name] competitors [Industry]"`
   - Search: `"top [Industry] companies worldwide [current year]"`
   - Search: `"top [Industry] companies [Country] [current year]"`

2. Produce two lists:
   - **Global competitors** — Top 5–8 players worldwide
   - **Local competitors** — Top 3–5 players in the specified country

3. For each competitor, provide a one-line description of their positioning.

**Output format:**
```markdown
## Competitors

### Global Players
| Company | Positioning | Headquarters |
|---------|------------|--------------|
| [Name] | [Brief description] | [Country] |

### Local Players ([Country])
| Company | Positioning | Market Share (if available) |
|---------|------------|---------------------------|
| [Name] | [Brief description] | [Data or N/A] |
```

---

### Section 4: Industry Data

**Research steps:**

1. Use `web_search` to find industry data **relevant to the opportunity description**:
   - Search: `"[Industry] market size [relevant keywords from opportunity description]"`
   - Search: `"[Industry] [relevant technology/topic] market data [current year]"`
   - Search: `"[Industry] digital transformation statistics"` (if applicable)

2. **Reference the ISK by CSA site** — Use `web_fetch` on `https://aka.ms/ISKbyCSA` to check for available industry research resources. Mention this resource in the output.

3. Focus on:
   - Market size and growth rate (CAGR)
   - Technology adoption rates relevant to the opportunity
   - Investment trends
   - Regulatory landscape (if relevant)

4. Use only trusted sources. Ask for clarification if data seems unreliable.

**Output format:**
```markdown
## Industry Data

### Market Overview
[Market size, growth rate, key statistics]

### Relevant Data Points
| Metric | Value | Source |
|--------|-------|--------|
| [Market size] | [Value] | [Source] |
| [Growth rate] | [Value] | [Source] |
| [Adoption rate] | [Value] | [Source] |

> **Additional Resource:** [ISK by CSA](https://aka.ms/ISKbyCSA) — Industry reference for CSA research.
```

---

### Section 5: Growth Opportunities

**Research steps:**

1. Use `web_search` to identify growth opportunities and market trends:
   - Search: `"[Industry] growth opportunities [current year]"`
   - Search: `"[Industry] investment trends [relevant keywords from opportunity]"`
   - Search: `"[Industry] [technology/topic from opportunity] use cases"`

2. **Connect findings to the opportunity description** — explicitly explain how each growth trend relates to the customer's project.

3. **Search for similar internal cases using WorkIQ:**
   - Use `workiq-ask_work_iq` to search for internal cases:
     - Query: `"Find case studies, success stories, or project examples in [Industry] related to [opportunity description keywords]"`
     - Query: `"Find SharePoint documents about [Industry] projects similar to [opportunity description]"`
     - Query: `"Find internal references or delivery examples for [Customer Name] or [Industry] [topic]"`
   - **If WorkIQ EULA has not been accepted**, use `workiq-accept_eula` with `eulaUrl: "https://github.com/microsoft/work-iq"` after getting explicit user confirmation.
   - **Mark all internal data clearly as `🔒 INTERNAL`** to distinguish from public sources.

4. If WorkIQ finds relevant SharePoint documents or file URLs, use them with the `fileUrls` parameter for deeper extraction.

**Output format:**
```markdown
## Growth Opportunities

### Market Trends
| # | Trend | Relevance to Opportunity | Source |
|---|-------|-------------------------|--------|
| 1 | [Trend] | [How it connects to the project] | [Source] |
| 2 | [Trend] | [How it connects to the project] | [Source] |

### Similar Cases

#### 🔒 INTERNAL Cases (from SharePoint)
| Case | Description | Relevance |
|------|------------|-----------|
| [Case name] | [Brief description] | [How it relates] |

> ⚠️ Data marked 🔒 INTERNAL is sourced from internal SharePoint and should not be shared externally.

#### Public Case Studies
| Case | Description | Source |
|------|------------|--------|
| [Case name] | [Brief description] | [URL] |
```

---

## WorkIQ / Microsoft 365 Copilot Integration

This skill leverages **WorkIQ** to access internal organizational knowledge, primarily for Section 5 (Growth Opportunities) but also opportunistically across other sections.

### Available WorkIQ Tools

- **`workiq-ask_work_iq`** — Query Microsoft 365 Copilot for emails, meetings, files, and SharePoint data.
- **`workiq-accept_eula`** — Accept the WorkIQ EULA (requires explicit user confirmation). EULA URL: `https://github.com/microsoft/work-iq`
- **`workiq-get_debug_link`** — Generate a shareable link for a WorkIQ conversation (requires user consent).

### When to Use WorkIQ

- **Section 1 (Company Profile)** — Search for internal emails or meeting notes about the customer.
- **Section 5 (Growth Opportunities)** — **Always search** for internal case studies and similar projects on SharePoint.
- **Any section** — If the user mentions an internal document or SharePoint link, use `fileUrls` parameter to extract context.

### WorkIQ Usage Guidelines

- **Offer to search internal data** at the start:
  > "I can also search your Microsoft 365 data for internal case studies, customer history, and relevant documents via WorkIQ. Would you like me to include internal data in this research?"
- **Always mark internal data as `🔒 INTERNAL`** — clearly distinguish from public web sources.
- **Never auto-search without informing the user.**
- **If WorkIQ returns an error**, use `workiq-get_debug_link` (with user consent) to help report the issue.

---

## Final Report Structure

After completing all sections, compile the full report:

```markdown
# Industry Research Report

## Opportunity Details
- **Opportunity ID:** [ID]
- **Customer:** [Customer Name]
- **Industry:** [Industry]
- **Country:** [Country]
- **Description:** [Opportunity Description]
- **Date:** [YYYY-MM-DD]

---

## Company Profile
[Section 1 output]

---

## Industry Challenges
[Section 2 output]

---

## Competitors
[Section 3 output]

---

## Industry Data
[Section 4 output]

---

## Growth Opportunities
[Section 5 output]

---

## Sources
[Numbered list of all sources cited in the report]

---

> **Disclaimer:** This report was generated by the Industry Research Skill as a pre-sales research aid.
> Data marked 🔒 INTERNAL is sourced from internal systems and should not be shared externally.
> All external data is sourced from publicly available information and cited accordingly.
> Verify critical data points before using in customer-facing materials.
```

---

## Save Research Report to File

After displaying the final report, **always offer to save it as a markdown file**.

### How to Offer

Use `ask_user`:

> "Would you like me to save this industry research report as a Markdown document?"
- Choices: Yes — save to a specific folder, Yes — save to the current folder, No thanks

### If the User Chooses a Specific Folder

Ask with `ask_user` (freeform):

> "Please provide the full folder path where you'd like me to save the report (e.g., `C:\Users\you\Documents\Research`)."

Validate the folder exists:
```powershell
Test-Path -Path "<user-provided-path>"
```
- If it **does not exist**, ask:
  > "That folder doesn't exist. Would you like me to create it?"
  - Choices: Yes — create it, No — I'll provide a different path
- If the user says yes, create it with `New-Item -ItemType Directory -Path "<path>" -Force`.

### If the User Chooses the Current Folder

Use the current working directory as the save location.

### File Naming Convention

```
Industry-Research_<customer-name>_<opportunity-id>_<YYYY-MM-DD>.md
```
- Sanitize the customer name (replace spaces/special chars with hyphens, lowercase).
- Example: `Industry-Research_contoso-ltd_OPP-2026-0042_2026-04-16.md`

If the customer name or opportunity ID is unknown:
```
Industry-Research_<YYYY-MM-DD>.md
```

### File Content

1. YAML frontmatter:
```markdown
---
title: Industry Research Report
customer: <Customer Name>
opportunity_id: <Opportunity ID>
industry: <Industry>
country: <Country>
date: <YYYY-MM-DD>
generated_by: Industry Research Skill
---
```

2. The **full Final Report** as defined above.

### After Saving

Use the `create` tool to write the file. Confirm:

> "✅ Industry research report saved to: `<full-file-path>`"

If the file already exists, append a numeric suffix:
- `Industry-Research_contoso-ltd_OPP-2026-0042_2026-04-16_2.md`

Check before writing:
```powershell
Test-Path -Path "<full-file-path>"
```

---

## SQL Tracking

Use the session SQL database to track research progress:

```sql
CREATE TABLE IF NOT EXISTS industry_research (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    finding TEXT,
    source TEXT,
    is_internal INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Insert findings as they are discovered. Query at the end to compile the report.

---

## Important Notes

- **Never fabricate facts** — if a data point cannot be verified, omit it or note it as unverified.
- **Always cite sources** — every claim must have a reference (URL, report name, or document title).
- **Ask for clarification** — when in doubt about the company, industry context, or data reliability, use `ask_user`.
- **Be specific to the opportunity** — generic industry reports are not enough; always connect findings back to the opportunity description.
- **Mark internal data clearly** — anything from WorkIQ/SharePoint must be tagged `🔒 INTERNAL`.
- **Professional tone** — this report may be used in customer-facing or internal strategy discussions.
- **Reference ISK by CSA** — always mention `https://aka.ms/ISKbyCSA` as an additional industry research resource.
