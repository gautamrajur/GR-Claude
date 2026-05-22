# Mode: resume -- ATS-Optimized Resume Generation

Triggered by `/jobs-ops resume {report_num}` (e.g. `/jobs-ops resume 007`).
If no report number given, ask which report to use.

---

## WHO THIS IS FOR

**Gautam Raju** - mid-level engineer, 3.5 years production experience.
NOT entry-level. NOT senior/principal (yet). Position: mid-level with graduate degree.
Core identity: 70% Platform Engineering / 30% SRE.

**Contact block (use verbatim):**
```
Gautam Raju
+1-857-370-2790 | raju.ga@northeastern.edu | linkedin.com/in/gautam-raju | github.com/gautamrajur
```

**Experience timeline (never alter titles or dates):**
| Period | Role | Notes |
|--------|------|-------|
| Aug 2016 - Jul 2020 | VTU - BE Computer Science | GPA 8.05/10.0 |
| Sep 2021 - Jul 2024 | Apple Inc. - Software Engineer | Backend, distributed systems, Python, CI/CD |
| Sep 2024 - Apr 2026 | Northeastern University - MS CS | GPA 3.7/4.0 |
| Jun 2025 - Dec 2025 | Ancestry - Software Engineer Cloud Platform (EKS Team) | K8s, Go/Python, platform tooling |

**Salary floor:** $135K+ base. **Visa:** H-1B sponsorship needed (OPT through ~2029). Never mention on resume.

---

## PROJECTS (selection basis, not exhaustive descriptions)

| Project | Key Tech | Best For |
|---------|----------|----------|
| Chaos Operator | Go, controller-runtime, Custom CRDs, Prometheus | SRE / K8s-heavy / Platform |
| K8s Resource Quota Enforcer | Python, FastAPI, Kyverno, Prometheus, AlertManager, PostgreSQL | Platform / Cloud / DevOps |
| Infra-Archaeology-MCP | Python, boto3, CloudTrail, Terraform, MCP, Claude AI | Any (AI tilt) / Cloud / Automation |
| EmailSender.AI | Python, OpenAI API, GitHub Actions, OAuth 2.0 | DevOps / Automation / GenAI |
| GPU Profiler | Python, CUDA, Matplotlib | Backend / Systems perf |
| AdaptEd AI | React Native, Expo, TypeScript, FastAPI, PostgreSQL | Full-stack / Mobile |
| AI Avatar System | React TypeScript, FastAPI, Groq LLM, Redux | Full-stack / GenAI |

**Default: 3 projects per resume.** Select based on JD analysis, not habit.

**Selection matrix:**
- SRE/Reliability: Chaos Operator, Quota Enforcer, Infra-Archaeology
- Platform Engineering: Quota Enforcer, Infra-Archaeology, Chaos Operator
- Cloud/DevOps: Quota Enforcer, Infra-Archaeology, EmailSender.AI
- Backend/Systems: AI Avatar, Quota Enforcer, Infra-Archaeology
- GenAI/LLM: Infra-Archaeology, AI Avatar, EmailSender.AI

---

## PIPELINE

### Step 0 - Company research (do first)

Web search: "[Company] [Role title] LinkedIn" and "site:linkedin.com [Company] SRE".
Find: common backgrounds, tech stack patterns, terminology employees use.
Share findings with user before generating resume.

### Step 1 - Load report

```bash
ls ~/projects/jobs-ops/reports/ | grep "^{report_num}-"
```

Read the full report. Extract: company, role title, JD URL, score, matched skills, gaps, archetype framing.

### Step 2 - Fetch JD + extract keywords

If JD text not inline in report, fetch the URL. Extract 15-20 keywords:
- Specific tools named in JD (exact names)
- Role verbs ("define SLOs", "own on-call")
- Scale signals ("production-scale", "100M+ requests")

### Step 3 - Score fit and set tailoring level

| Fit Score | Tailoring Level | Action |
|-----------|-----------------|--------|
| 8-10/10 | None | Submit base resume, standard project order |
| 6-7/10 | Light | Reorder bullets, mirror JD terms, pick 3 projects |
| 4-5/10 | Heavy | Rewrite summary, aggressive bullet reorder, bridge project |
| 1-3/10 | Skip | Do not apply |

### Step 4 - Detect paper format

US/Canada: `letter` (8.5in). Elsewhere: `a4` (210mm). Default: letter.

### Step 5 - Map role archetype

| Archetype | JD signals |
|-----------|------------|
| SRE/Reliability | SLOs, MTTR, postmortems, on-call, uptime |
| Cloud Platform/EKS | K8s operators, CRDs, controller-runtime, Helm, Kyverno |
| SWE Backend/Infra | microservices, APIs, CI/CD, distributed systems |
| AI/ML Platform | LLM tooling, MCP, ML serving, Claude/OpenAI |

### Step 6 - Rewrite Professional Summary

3-4 lines. Top 5 JD keywords injected. Match role framing exactly.

Template variants (pick closest, then customize):
- Platform: "Software Engineer with 3+ years building cloud platforms and automation tools on Kubernetes/EKS..."
- SRE: "Site Reliability Engineer with 3+ years managing production EKS platform, specializing in observability and toil reduction..."
- Cloud: "Cloud Platform Engineer with 3+ years building AWS infrastructure, Kubernetes platforms, and automation systems..."
- Backend: "Backend Software Engineer with 3+ years building scalable APIs, automation tools, and distributed systems..."

Keyword injection rules:
- NEVER add skills Gautam does not have
- Only reword real experience using exact JD vocabulary
- JD says "chaos engineering" + CV says "load testing, fault injection" -> "chaos engineering and fault injection at scale"

### Step 7 - Reorder experience bullets (do not delete)

**Ancestry (EKS Team):**
- Platform roles: lead with automation APIs, developer productivity, infrastructure provisioning
- SRE roles: lead with on-call, observability (Prometheus/Grafana/DataDog), MTTR, reliability
- Cloud roles: lead with EKS, AWS services, Terraform/Ansible
- Backend roles: lead with API development, Python/Go, system design

**Apple:**
- Platform/SRE: lead with distributed scale (100M+ txns), on-call, monitoring, automation
- Backend: lead with APIs, data pipelines (5TB daily), microservices
- Cloud/DevOps: lead with CI/CD (65% deployment time reduction), infrastructure, monitoring

**Max 4-5 bullets per job.**

### Step 8 - Select 3 projects

Use selection matrix above. Lead with most relevant. Projects support - don't replace - industry experience.

For Google/Meta/AWS: lead Chaos Operator, then Quota Enforcer, then Infra-Archaeology.

### Step 9 - Reorder Technical Skills

Most JD-relevant category first. Trim low-priority keywords not in JD.
Always include "AI-Assisted Development: GitHub Copilot, Claude AI" unless space critical.

Skill category templates:
- Platform/SRE first: Languages -> SRE & Operations -> Monitoring & Observability -> Kubernetes & Containers -> Cloud & Infrastructure -> Automation & CI/CD -> AI-Assisted
- Backend first: Languages -> Backend & APIs -> Cloud & Infrastructure -> Databases -> Automation & CI/CD -> Monitoring -> AI-Assisted
- Cloud/DevOps first: Cloud & Infrastructure -> Kubernetes -> Automation & CI/CD -> Monitoring -> Languages -> Databases -> AI-Assisted

### Step 10 - Run ATS keyword audit (Rule 1 - mandatory)

Extract every distinct keyword/phrase from JD. Check exact match in resume.
Build coverage table: JD Keyword | Present? | Where?
Target: 90%+ exact coverage. Fix gaps by rewriting bullets to embed exact JD phrases.
Present audit table before finalizing.

### Step 11 - Verify all 8 rules (checklist)

See Rules section below. Fix any failure before presenting output.

### Step 12 - Generate markdown artifact

Clean text/markdown with `•` bullets. ALL CAPS section headers. ATS-friendly (no special chars, no tables).

### Step 13 - Generate PDF (single bash call - see PDF Spec)

Write a JSON file `/tmp/cv-gautam-raju-{company}.json` with the resume content schema:

```json
{
  "name": "GAUTAM RAJU",
  "contact": "+1-857-370-2790 | raju.ga@northeastern.edu | linkedin.com/in/gautam-raju | github.com/gautamrajur",
  "summary": "...",
  "education": [
    {"school": "Northeastern University", "degree": "MS, Computer Science", "dates": "Sep 2024 - Apr 2026", "gpa": "3.7/4.0", "coursework": "Distributed Systems, MLOps, Cloud Computing"},
    {"school": "Visvesvaraya Technological University", "degree": "BE, Computer Science", "dates": "Aug 2016 - Jul 2020", "gpa": "8.05/10.0"}
  ],
  "experience": [
    {"company": "Ancestry", "title": "Software Engineer Cloud Platform (EKS Team)", "dates": "Jun 2025 - Dec 2025", "bullets": ["..."]},
    {"company": "Apple Inc.", "title": "Software Engineer", "dates": "Sep 2021 - Jul 2024", "bullets": ["..."]}
  ],
  "projects": [
    {"name": "Project Name", "tech": "Go, Kubernetes, ...", "bullets": ["..."]}
  ],
  "skills": [
    {"category": "Languages", "items": "Python, Go, Bash, ..."}
  ]
}
```

Then run:
```bash
cd ~/projects/jobs-ops && python3 scripts/generate_resume.py \
  /tmp/cv-gautam-raju-{company}.json \
  output/cv-gautam-raju-{company}-{YYYY-MM-DD}.pdf \
  --format={letter|a4}
```

The script auto-installs `reportlab` and `pypdf` into the project `.venv` on first run. No npm required.

### Step 14 - Update tracker + report to user

In `data/tracker.md`, row for `{report_num}`: change PDF column `❌` -> `✅`.

Print:
```
Resume: output/cv-gautam-raju-{company}-{YYYY-MM-DD}.pdf
Keywords: {N}/{total} exact matches from JD
Archetype: {archetype}
Tracker: #{report_num} PDF -> ✅
```

---

## MANDATORY RULES

### Rule 1: ATS Keyword Coverage - 90%+

Exact JD phrases must appear in resume - paraphrasing alone does not pass ATS.
Present full coverage table to user before finalizing.

### Rule 2: 12-15 Words Per Bullet (STRICT)

ALL bullets in Work Experience AND Projects: 12-15 words.
- Under 12: lacks detail. Over 15: wraps lines, breaks formatting.
- Techniques: compound terms (Python/Go, Prometheus/Grafana), remove filler, one idea per bullet, lead with metric.
- Count every bullet. Include word count verification in output.

### Rule 3: Action Verb Hierarchy

**Work Experience:** Tier 1 (60%): Architected, Led, Engineered, Designed, Drove, Spearheaded. Tier 2 (30%): Optimized, Developed, Implemented, Established, Pioneered. Tier 3 (<=10%): Built. NEVER: Participated, Helped, Assisted, Worked on.

**Projects:** Built, Developed, Implemented, Created, Designed. NEVER: Architected, Led, Engineered (implies enterprise context projects don't have).

### Rule 4: Show Don't Tell

Every bullet must be interview-ready: specific tech names (controller-runtime not "K8s framework"), specific patterns (exponential backoff not "retry logic"), specific tools (testify table-driven tests not "comprehensive testing"), measurable outcomes.

Ask: "Can I discuss this bullet for 5 minutes with technical depth?" If no, rewrite.

### Rule 5: Conciseness

Replace: "through the use of" -> "using", "in order to" -> "to", "by means of" -> "via".
Remove: very, highly, various, multiple, comprehensive, robust, innovative, cutting-edge.
Active voice always. One idea per bullet.

### Rule 6: Pre-Submission Checklist

Before presenting any resume, verify:
1. All bullets 12-15 words (counted)
2. Senior verbs in Work Experience, appropriate verbs in Projects
3. ATS audit complete, 90%+ coverage
4. No verbose phrases or filler words
5. Compound terms used (Python/Go, Prometheus/Grafana)
6. Metrics lead bullets where possible
7. Active voice throughout, one idea per bullet
8. Skills section reordered and trimmed for JD

### Rule 7: Dual Format Output

Always produce:
1. TEXT/MARKDOWN artifact - editable, ATS-friendly
2. PDF artifact - via single bash call (see PDF Spec below)

---

## PDF GENERATION SPEC

PDF generation uses `scripts/generate_resume.py` (ReportLab, Python only - no npm/Node).
Auto-installs `reportlab` + `pypdf` into `.venv` on first run.

### Single-shot rule

Generate PDF EXACTLY ONCE in a SINGLE bash call. Never iterate to fix page count.

### Two-pass algorithm (already implemented in the script)

```
Pass 1: Build all flowables at standard font sizes, sum .wrap() heights
Pass 2: total > available  -> scale all font sizes proportionally (* 0.97)
        total < 88% of available -> distribute slack into section spaceBefore
        good fit -> build as-is
Output: write PDF once, log warning if !=1 page, never regenerate
```

### Page setup

Letter: 8.5" x 11". Margins: side 0.5in (36pt), top/bottom 0.4in (28.8pt). Available: ~734pt height, 540pt width.

### Header construction (exact - prevents overlap)

```python
story.append(Paragraph("GAUTAM RAJU", name_style))          # 18pt Helvetica-Bold, centered
story.append(Spacer(1, 8))                                   # MANDATORY 8pt gap
story.append(Paragraph("contact info", contact_style))       # 9pt Helvetica, centered
story.append(Spacer(1, 4))                                   # MANDATORY 4pt gap
story.append(HRFlowable(width="100%", thickness=0.8, color=accent_color))
story.append(Spacer(1, 6))                                   # MANDATORY 6pt before first section
```

### Font sizes

| Element | Size | Font |
|---------|------|------|
| Name | 18pt (min 16pt) | Helvetica-Bold |
| Contact | 9pt (min 8.5pt) | Helvetica |
| Section headers | 10.5pt (min 10pt) | Helvetica-Bold, ALL CAPS |
| Body/bullets | 9.2pt (min 8.8pt) | Helvetica |
| Tech stacks | 8.5pt (min 8pt) | **Helvetica-Bold** (not italic) |
| Leading | 11.5pt | - |

### Spacing

| Element | spaceBefore | spaceAfter |
|---------|-------------|------------|
| Section headers | 8pt | 1pt then HR then 3pt spacer |
| Job/project headers | 5pt | - |
| Bullets | - | 1.5pt |
| Skills lines | - | 1.5pt |

If overflow: reduce bullet spaceAfter to 1.0, section spaceBefore to 6, body font to 9.0pt minimum 8.8pt.

### Date alignment

ReportLab Table: colWidths=[78%, 22%]. Right column dates RIGHT-ALIGNED. Never use &nbsp; padding.

### Keyword bolding

Bold in bullets: technology names, tool names, metrics/percentages, key concepts.
Skills section: category labels bold, items regular weight.

### Section dividers

0.5pt light gray HRFlowable under each section header. 0.8pt accent-colored line under contact info.

### Verification (informational only, no regeneration)

```python
from pypdf import PdfReader
page_count = len(PdfReader(output_path).pages)
# log warning if !=1, do NOT regenerate
```
