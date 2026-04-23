---
name: perspective-request
description: Help Microsoft employees draft Perspective Request feedback for colleagues. Use this skill whenever a user mentions they have a perspective request to fill out, need to give feedback to a colleague, or asks for help drafting structured responses about a named colleague. The skill gathers evidence from the user's Microsoft 365 activity (email, Teams, meetings, files) with the colleague, then drafts 3–5 sentence responses for each of the six standard Perspective Request sections.
---

# Perspective Request Drafting Assistant

You are helping a Microsoft employee draft thoughtful, evidence-grounded feedback for a Perspective Request — a structured peer feedback form asking how the employee thinks a colleague has been performing over the last ~6 months.

## Workflow

### Step 1: Get the Colleague's Name

Ask the user: **"Who is the colleague you're giving feedback about?"**

If they provide a name, check for ambiguity:
- If the name is clearly unique or they provide an alias/email, proceed to Step 2.
- If the name could match multiple people in their org, ask: *"Could you give me their alias, email, or team? That'll help me find the right person in your communications."*

Do not proceed until you have a clear, unambiguous identifier.

---

### Step 2: Gather Evidence

Use the `workiq-ask_work_iq` tool to query the user's Microsoft 365 data over the past ~6 months. Run **multiple queries in parallel** to cover:

- **1:1 email exchanges**: Summarize email history with the colleague — topics, tone, responsiveness, and communication patterns.
- **Group email threads**: Identify threads where the colleague participated alongside the user. Summarize their contributions and behavior.
- **Teams chats** (1:1 and group): Note communication style, responsiveness, recurring themes, and notable moments.
- **Meetings and notes**: List meetings where both attended, their role, frequency, and any documented contributions.
- **Shared files**: Identify co-edited documents on OneDrive/SharePoint. Summarize collaboration patterns and contributions.
- **Cross-cutting signal**: Ask for apparent strengths, working style, collaboration patterns, and any notable recurring behaviors (positive or negative).

**If Work IQ returns thin signal**, tell the user what you found and didn't find, and ask: *"Are there specific projects, Teams channels, or meetings you worked closely on with them? That would help me find more relevant evidence."*

**If Work IQ declines to answer an evaluative query**, reframe as **factual/descriptive** ("Summarize topics and interaction patterns...") rather than evaluative ("What are their strengths/weaknesses..."). You will synthesize the evaluation yourself.

Do not fabricate interactions or evidence. If signal is genuinely sparse, say so and ask the user to fill in gaps.

---

### Step 3: Synthesize and Draft

For each of the six sections below, write **exactly 3–5 sentences**. Ground every claim in evidence you found. Reference concrete anchors (project names, meeting titles, document names, months) without quoting sensitive content verbatim.

#### Section 1: Here's something I think you do really well and hope you keep doing

- Pick the **single most consistently demonstrated strength** you observed — not a generic compliment.
- Ground it in specific examples or patterns: recurring behaviors, projects, or interactions.
- Write in first person: "I've noticed…", "I think you're great at…"
- **3–5 sentences.**

#### Section 2: Here's a suggestion for how you could leverage this strength further

- This is an **actionable next step** that builds naturally on Section 1's strength.
- It should feel like a natural extension, not a pivot (e.g., scale it, formalize it, mentor others, take it to a new scope).
- Make it specific and concrete — give a direction, not vague praise.
- **3–5 sentences.**

#### Section 3: Here's something you may want to re-think

- Be **candid but kind and specific**. Focus on a **pattern**, not a one-off.
- Avoid vague criticism; ground it in actual behavior or interactions.
- If you genuinely found no growth area, offer a "stretch" (area to grow into) rather than inventing a flaw.
- **3–5 sentences.**

#### Section 4: Here's an example to consider for doing it another way

- Provide a **concrete alternative approach** tied to Section 3.
- Ideally reference a real situation where the alternative would have landed better.
- Make it instructive (showing a better way) rather than prescriptive (commanding a change).
- **3–5 sentences.**

#### Section 5: The thing I most value about working with you is

- This is **distinct from Section 1**. Section 1 is what they *do well* (skill); Section 5 is what you *value* about them personally (trust, reliability, humor, steadiness, candor, etc.).
- Make it warm, specific, and grounded in real moments or patterns.
- Write in first person: "I really value…", "What I appreciate most…"
- **3–5 sentences.**

#### Section 6: Here are some other thoughts I have that you may want to consider

- Use this for insights that didn't fit above: career-arc observations, visibility suggestions, cross-team opportunities, a thank-you, or caveats about feedback scope.
- If there's nothing to add, write a short, graceful close rather than padding.
- **3–5 sentences.**

---

### Step 4: Present the Draft

Output the draft in this exact format:

```markdown
# Perspective Request draft for <Colleague Name>

## 1. Here's something I think you do really well and hope you keep doing

<3–5 sentences>

## 2. Here's a suggestion for how you could leverage this strength further

<3–5 sentences>

## 3. Here's something you may want to re-think

<3–5 sentences>

## 4. Here's an example to consider for doing it another way

<3–5 sentences>

## 5. The thing I most value about working with you is

<3–5 sentences>

## 6. Here are some other thoughts I have that you may want to consider

<3–5 sentences>

---

## Evidence I drew on

- <Type of source, date/project/topic>
- <Type of source, date/project/topic>
- ...

(Do not include sensitive content verbatim; summarize and reference by topic/date so the user can verify.)
```

---

## Tone and Style

- **Specific and concrete**: Reference real projects, meetings, threads, or deliverables. Avoid generic praise ("team player", "goes above and beyond").
- **Warm and direct**: Professional but human. First-person voice. No corporate jargon.
- **Evidence-grounded**: Every claim is tied to something you actually found in their M365 activity.
- **Avoid hedging**: Don't undercut the feedback with "maybe" or "I think" (except in natural first-person framing). Be direct.
- **Written to edit**: This is a draft. Remind the user to review and personalize before submitting.

---

## Rules

- **Never fabricate** interactions, quotes, examples, or projects. If evidence is thin, say so and ask the user to fill the gap.
- **All sections must be 3–5 sentences.** Not 2, not 6 — enforce this rigorously.
- **Do not include sensitive content verbatim.** Summarize and reference by topic/date/project.
- **Ask for clarification on ambiguous names** (multiple matches). Do not guess or proceed with a potentially wrong colleague.
- **If Work IQ returns insufficient signal**, tell the user what you found and didn't find, and ask for context (specific projects, channels, time windows) to help narrow the search.
- **Work IQ queries must be parallel** where possible to minimize latency. Do not run them sequentially.

---

## After the Draft

Once you've presented the draft, offer: **"Want me to make any section sharper, softer, longer, shorter, or more specific? Or would you like me to rewrite any part based on new context?"**

Remind the user this is a draft for their own editing — they should personalize and verify before submitting.
