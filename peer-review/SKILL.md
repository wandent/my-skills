---
# Peer Review skill
name: peer-review
description: "Use this skill whenever the user asks for peer review of a scientific study, manuscript, preprint, or research report. It performs a full specialist review workflow: deep reading, AI-authorship likelihood detection, summary of objectives/methods/results, methodological validity checks, originality and relevance checks against literature, table/figure consistency checks, specific revision comments, and a final recommendation. Trigger even when the user says 'analyze this study', 'review this paper', 'evaluate this manuscript', 'is this robust', or 'compare with literature'."


---

## Purpose

Run a rigorous, structured peer review of scientific manuscripts, technical text or essays and produce a report that is both critical and constructive.

This skill is based on a repeatable 5-step workflow:

1. Deep manuscript reading and evidence extraction
2. Specialist summary of objectives, methods, and key results
3. General comments (originality, validity, relevance, strengths/weaknesses)
4. Specific comments (formal issues, tables/figures, methods, references)
5. Literature comparison and positioning in current knowledge

It also includes explicit AI-authorship likelihood analysis.

---

## Inputs

- Manuscript file (PDF, DOCX, TXT, MD, or pasted text)
- Optional field context (e.g., oncology, economics, ML)
- Optional focus area (methodology, statistics, references, novelty, etc.)

If the manuscript is not available, ask for the file or text before proceeding.

---

## Required Outputs

Always produce these outputs:

1. AI-authorship likelihood assessment with evidence
2. Study summary (objectives, methods, most relevant results)
3. General comments
4. Specific comments
5. Literature comparison with references
6. Final recommendation: Accept / Minor Revisions / Major Revisions / Reject

---

## Workflow

Follow steps in order. Do not skip steps.

### Step 1: Read Manuscript Carefully

Perform a detailed read and extract evidence for later sections.

#### 1.0 Content Extraction (PDF and HTML)

Because most scientific manuscripts are PDFs, always start with robust extraction.
If the manuscript is HTML, extract readable body text and tables before analysis.

Install dependencies when needed:

```bash
pip install pypdf pdfplumber beautifulsoup4 lxml trafilatura
```

Use this Python code for extraction:

```python
from pathlib import Path
from typing import Dict, List


def extract_pdf_content(file_path: str) -> Dict:
    """Extract text and tables from PDF using layered fallbacks."""
    result = {
        "source": file_path,
        "format": "pdf",
        "full_text": "",
        "pages": [],
        "tables": [],
    }

    # First pass: pypdf for quick page text extraction
    from pypdf import PdfReader

    reader = PdfReader(file_path)
    pypdf_text_pages: List[str] = []
    for i, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        pypdf_text_pages.append(page_text)
        result["pages"].append({"page": i, "text": page_text})

    combined_text = "\n\n".join([t for t in pypdf_text_pages if t])

    # Fallback: pdfplumber often gives better layout/table extraction
    # Use it when pypdf output is sparse.
    if len(combined_text) < 200:
        import pdfplumber

        result["pages"] = []
        pdfplumber_pages: List[str] = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_text = (page.extract_text() or "").strip()
                pdfplumber_pages.append(page_text)
                result["pages"].append({"page": i, "text": page_text})

                for table in page.extract_tables() or []:
                    if table:
                        result["tables"].append({"page": i, "rows": table})

        combined_text = "\n\n".join([t for t in pdfplumber_pages if t])

    result["full_text"] = combined_text
    return result


def extract_html_content(file_path: str) -> Dict:
    """Extract clean text and tables from HTML manuscript files."""
    result = {
        "source": file_path,
        "format": "html",
        "title": "",
        "full_text": "",
        "tables": [],
    }

    html = Path(file_path).read_text(encoding="utf-8", errors="ignore")

    # Prefer readability-style extraction from noisy HTML pages
    import trafilatura

    main_text = trafilatura.extract(html, include_tables=False)

    # Parse structural data and tables
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        result["title"] = soup.title.string.strip()

    for t_idx, table in enumerate(soup.find_all("table"), start=1):
        rows = []
        for tr in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        if rows:
            result["tables"].append({"table": t_idx, "rows": rows})

    # Fallback if trafilatura cannot extract
    if not main_text:
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        main_text = soup.get_text("\n", strip=True)

    result["full_text"] = main_text or ""
    return result


def extract_manuscript(file_path: str) -> Dict:
    """Route extraction by file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_pdf_content(file_path)
    if ext in {".html", ".htm"}:
        return extract_html_content(file_path)
    raise ValueError(f"Unsupported format for this extractor: {ext}")
```

Extraction quality checks before proceeding:

- Confirm `full_text` is non-empty and includes Methods/Results-like sections.
- Confirm tables were captured when the manuscript contains tabular data.
- If extraction quality is poor, request OCR or a better source file.

Capture:

- Research objective/hypothesis
- Study design and methodology
- Sample and participant selection details
- Statistical methods and reported significance
- Main findings and effect directions
- Tables and figure claims in text
- Reference list quality and consistency
- Claim-to-citation links (which manuscript claims are supported by which references)

#### 1A) AI-Authorship Likelihood Detection

Assess whether the manuscript appears human-authored, AI-assisted, or likely AI-generated.

Check for:

- Repetitive generic phrasing
- Formulaic paragraph cadence across sections
- Low domain-specific depth where high expertise is expected
- Citation anomalies (fabricated, mismatched, or unverifiable references)
- Overly smooth transitions with little argumentative nuance

Output one label:

- Low likelihood
- Moderate likelihood
- High likelihood

Always justify the label with concrete examples from the manuscript.

#### 1B) Table/Figure Coherence Check

For each major table/figure:

- Verify it is clearly labeled and interpretable
- Verify it supports the exact claims made in text
- Flag mismatches (text says A, figure/table shows B)

---

### Step 2: Write a Specialist Summary

Write in your own words:

- Main objectives
- Methodology used
- Most relevant results

Keep concise but substantive. Prefer exact values (effect sizes, p-values, confidence intervals) when available.

---

### Step 3: General Comments

#### 3.1 Originality

Run a quick literature search for similar studies.

Evaluate:

- Whether the hypothesis is novel
- Whether similar hypotheses have already been tested
- Whether this manuscript adds meaningful new knowledge

List similar studies with short relevance notes.

#### 3.2 Validity

Evaluate:

- Sample adequacy for claims made
- Data collection quality and reproducibility
- Statistical method appropriateness
- Statistical significance reporting adequacy
- Confounders/bias handling

State if conclusions are supported by the presented evidence.

#### 3.3 Relevance

Evaluate:

- Internal coherence between findings and claims
- Importance to the field
- Alignment or conflict with existing literature

Produce a comparison table:

```markdown
| Finding | This Study | Similar Study 1 | Similar Study 2 | Similar Study 3 |
|---|---|---|---|---|
| [Finding A] | [Result] | [Similarity/Difference] | [Similarity/Difference] | [Similarity/Difference] |
| [Finding B] | [Result] | [Similarity/Difference] | [Similarity/Difference] | [Similarity/Difference] |
```

#### 3.4 Strengths and Weaknesses

List both:

- Strengths (clarity, robust design, good analysis, etc.)
- Weaknesses (method flaws, inconsistent interpretation, weak controls, etc.)

---

### Step 4: Specific Comments

Provide targeted revision notes.

#### 4.1 Formal and Language Issues

- Grammar/phrasing errors
- Nonsensical or ambiguous sentences
- Terminology inconsistencies

#### 4.2 Tables and Figures

- Labeling clarity
- Visual readability
- Consistency with narrative claims
- Suggested corrections

#### 4.3 Methodological Questions

Raise concrete questions on:

- Participant selection
- Missing methodological details
- Statistical assumptions/tests

#### 4.4 Reference Integrity

- Verify citation order and in-text correspondence
- Spot-check references for existence and correct attribution
- Flag suspicious or fabricated references

#### 4.5 Claim-to-Citation Cross-Check (Required)

Do a best-effort verification that claims in the manuscript are consistent with the content of cited references.

Minimum procedure:

1. Extract at least 5 high-impact claims from the manuscript (or all claims if fewer than 5).
2. Map each claim to the cited reference(s) in the manuscript.
3. Retrieve the referenced source content when possible (publisher page, abstract page, PDF, HTML full text).
4. Extract text from each retrieved source and compare with the manuscript claim.
5. Label each claim-reference pair as:
   - **Supported**
   - **Partially Supported**
   - **Not Supported**
   - **Not Verifiable** (paywall, inaccessible source, broken link, etc.)

Use this implementation pattern:

```python
import re
import requests
from pathlib import Path
from typing import Dict, List


def extract_claim_citation_pairs(manuscript_text: str) -> List[Dict]:
    """Extract simple claim/citation pairs using numeric or author-year citation patterns."""
    pairs = []
    sentences = re.split(r"(?<=[.!?])\s+", manuscript_text)
    for s in sentences:
        s = s.strip()
        if not s:
            continue

        numeric = re.findall(r"\[(\d+(?:\s*[,;-]\s*\d+)*)\]", s)
        author_year = re.findall(r"\(([A-Z][A-Za-z\-]+(?:\s+et al\.)?,\s*\d{4}[a-z]?)\)", s)

        cites = []
        for block in numeric:
            cites.extend([x.strip() for x in re.split(r"[,;-]", block) if x.strip()])
        cites.extend(author_year)

        if cites:
            pairs.append({"claim": s, "citations": cites})
    return pairs


def fetch_url_text(url: str) -> str:
    """Best-effort text retrieval for citation pages."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PeerReviewBot/1.0)"
    }
    r = requests.get(url, headers=headers, timeout=25)
    r.raise_for_status()
    content_type = r.headers.get("content-type", "").lower()

    # PDF citation source
    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        temp_pdf = Path("_citation_temp.pdf")
        temp_pdf.write_bytes(r.content)
        from pypdf import PdfReader
        reader = PdfReader(str(temp_pdf))
        text = "\n\n".join([(p.extract_text() or "") for p in reader.pages])
        temp_pdf.unlink(missing_ok=True)
        return text

    # HTML citation source
    html = r.text
    import trafilatura
    txt = trafilatura.extract(html)
    if txt:
        return txt
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text("\n", strip=True)


def assess_claim_support(claim: str, source_text: str) -> str:
    """Heuristic support label; reviewer must validate manually before final report."""
    if not source_text or len(source_text.strip()) < 100:
        return "Not Verifiable"

    claim_tokens = set(re.findall(r"[A-Za-z]{4,}", claim.lower()))
    source_tokens = set(re.findall(r"[A-Za-z]{4,}", source_text.lower()))
    if not claim_tokens:
        return "Not Verifiable"

    overlap = len(claim_tokens & source_tokens) / max(1, len(claim_tokens))
    if overlap >= 0.6:
        return "Supported"
    if overlap >= 0.35:
        return "Partially Supported"
    return "Not Supported"
```

Always include a reviewer note: automated matching is heuristic and must be interpreted with human judgment.

---

### Step 5: Compare with Literature

Provide references that support your judgments on:

- Originality and relevance
- Methodological appropriateness and potential flaws

Then write a short positioning statement:

- Does the study fill a gap, replicate known findings, challenge the field, or overclaim?

Also report citation-concordance findings from Step 4.5 and highlight any major contradictions.

---

## Decision Points and Branching Logic

Use these branches during review:

1. Manuscript quality branch:
- If PDF/HTML text extraction is poor or unreadable, request a better source file (or OCR for scanned PDFs) before continuing.
2. Evidence completeness branch:
- If critical methods/statistics are missing, mark validity as limited and escalate in specific comments.
3. Literature branch:
- If few similar studies are found, report search limitations and broaden keyword strategy once.

3b. Citation retrieval branch:

- If citations are behind paywalls or inaccessible, try alternate sources (DOI landing page, PubMed abstract, preprint versions, institutional repository).
- If still inaccessible, mark as Not Verifiable and explicitly list unresolved references.
4. AI-authorship branch:
- If AI-likelihood is moderate/high, include a caution note, but continue technical evaluation on its own merits.
5. Recommendation branch:
- If major validity flaws undermine conclusions, recommendation cannot exceed Major Revisions.

---

## Quality Criteria and Completion Checks

Before finalizing, verify all checks are satisfied:

- AI-authorship likelihood assessed with evidence
- Objectives/methods/results summary completed
- Originality check includes comparable literature
- Validity analysis addresses sample, methods, and statistics
- Relevance analysis includes similarity/difference table
- Strengths and weaknesses both included
- Specific comments include methods, stats, references, tables/figures
- Claim-to-citation cross-check completed for required claims (or explicitly marked Not Verifiable with reasons)
- Final recommendation justified by evidence

If any check fails, continue reviewing until complete.

---

## Final Report Template

Use this structure:

```markdown
# Peer Review Report

## Manuscript Information
- Title:
- Authors:
- Venue/Journal (if available):
- Date Reviewed:

## AI-Authorship Likelihood
- Assessment: [Low / Moderate / High]
- Evidence:

## Summary of the Article
- Main objectives:
- Methodology:
- Most relevant results:

## General Comments

### Originality
[Assessment + similar studies]

### Validity
[Assessment + statistical/methodological reasoning]

### Relevance
[Assessment + literature alignment]

### Similar Findings Comparison
| Finding | This Study | Similar Study 1 | Similar Study 2 | Similar Study 3 |
|---|---|---|---|---|
| | | | | |

### Strengths
-

### Weaknesses
-

## Specific Comments

### Formal Issues
-

### Tables and Figures
-

### Methodological Questions
-

### Reference Check
-

### Claim-to-Citation Concordance
| Manuscript Claim | Cited Ref(s) | Verification Source | Status | Notes |
|---|---|---|---|---|
| | | | Supported / Partially Supported / Not Supported / Not Verifiable | |

## Literature Positioning
[How the manuscript sits relative to current knowledge]

## Overall Recommendation
[Accept / Minor Revisions / Major Revisions / Reject]

## Justification
[Short evidence-based rationale]

## References Used in This Review
-
```

---

## Reviewer Conduct Rules

- Be evidence-based and specific
- Separate major issues from minor edits
- Do not fabricate citations
- Be constructive and actionable
- If uncertain, explicitly state uncertainty
