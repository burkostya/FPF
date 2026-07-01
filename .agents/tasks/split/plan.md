# Plan: Annotate & Split FPF-Spec.md

## Problem

`FPF-Spec.md` is 70K lines / 6.3MB — too large for LLM agents to consume as a single file. We need to split it into a hierarchical file-tree while preserving the ability to reconstruct the original document exactly.

## Solution

Four Python scripts in `scripts/`, producing an annotated intermediate form, then an extracted file-tree, then a compile-back step, then a round-trip verification.

---

## Directory layout

```
scripts/
├── anchor.py          # Original → FPF-Spec-Anchored.md  (XML-tagged intermediate)
├── split.py           # Anchored → fpf-spec/ + manifest.json
├── compile.py         # fpf-spec/ → FPF-Spec-Compiled.md  (un-annotated, round-trip)
└── verify.py          # Round-trip: original ↔ anchor→split→compile

fpf-spec/
├── manifest.json                          # Full hierarchy tree (JSON)
├── title.md                               # Document title
├── toc.md                                 # Table of Contents
├── preface.md                             # Preface header
├── keywords-discipline.md                 # Keywords & Search Queries
├── preface-subsections/                   # Preface essay headings (no pattern ID)
│   ├── preface-what-this-spec-is.md
│   ├── preface-creativity-in-open-ended-evolution.md
│   └── ...  (17 files)
├── parts/
│   ├── part-a-kernel-architecture.md       # # Part A header
│   ├── part-b.md
│   ├── part-c.md
│   ├── part-d.md
│   ├── part-e.md
│   ├── part-f.md
│   ├── part-g.md
│   ├── part-h.md
│   ├── part-i.md
│   ├── part-j.md
│   └── part-k.md
└── patterns/
    ├── a/
    │   ├── a-0-onboarding-glossary.md
    │   ├── a-1-holonic-foundation.md
    │   ├── a-1-1-u-bounded-context.md
    │   └── ...  (~29 files for Part A)
    ├── b/
    │   └── ...  (~20 files)
    ├── c/
    │   └── ...  (~30 files)
    ├── d/
    │   └── ...  (1 file)
    ├── e/
    │   └── ...  (~20 files)
    ├── f/
    │   └── ...  (~15 files)
    ├── g/
    │   └── ...  (~14 files)
    ├── h/
    │   └── ...  (1 file)
    ├── i/
    │   └── ...  (1 file)
    ├── j/
    │   └── ...  (1 file)
    └── k/
        └── ...  (3 files)
```

**Estimated: ~228 pattern/section files, ~5,457 heading anchors, ~1,000 lines of Python (4 × 250 lines).**

---

## Extraction rules

| Source heading level | What happens | Example |
|---|---|---|
| `#` (level 1) — Title, TOC, Part headers, Preface header | Standalone file at top level or `parts/` | `title.md`, `parts/part-a-kernel-architecture.md` |
| `##` with a pattern ID (e.g., `## A.1 - ...`) | Own file in `patterns/{letter}/{slug}.md` | `patterns/a/a-1-holonic-foundation.md` |
| `##` without pattern ID in Preface region | Standalone file in `preface-subsections/` | `preface-subsections/preface-what-this-spec-is.md` |
| `###` (nested, e.g., `### A.1:1 - Problem Frame`) | Stays in parent `##` file | inside `a-1-holonic-foundation.md` |
| `####`–`######` (deeper nesting) | Stays in parent file | inside `a-1-holonic-foundation.md` |

### File naming convention

Slug rules: lowercase, replace dots/hyphens with underscores, strip special chars, truncate to ~80 chars.

| Source ID | Output file |
|---|---|
| `## A.19.SURF-SPACE` | `patterns/a/a-19-surf-space.md` |
| `## E.17.0` | `patterns/e/e-17-0-u-multiviewdescribing.md` |
| `## A.6` | `patterns/a/a-6-signature-stack-and-boundary-discipline.md` |
| `## Keywords & Search Queries` | `keywords-discipline.md` |
| `## What this specification is` | `preface-subsections/preface-what-this-spec-is.md` |
| `# Part A – Kernel Architecture Cluster` | `parts/part-a-kernel-architecture.md` |

### Frontmatter in each pattern file

```markdown
---
id: A.1
title: Holonic Foundation: Entity → Holon
part: A
level: 2
parent: null
source: FPF-Spec.md
---

## A.1 - Holonic Foundation: Entity → Holon

> **Type:** Definitional (D)
> **Status:** Stable
> ...

### A.1:1 - Problem Frame
...

### A.1:2 - Problem
...
```

Non-pattern files (preface essays, parts headers, preface, toc, title, keywords) get minimal frontmatter without `id`/`parent`.

### Parent tracking

For `##` pattern files, `parent` is the nearest ancestor `# Part X` header (e.g., `"A"`). Nested `###` headings do NOT get their own files — they stay in the parent file. The `manifest.json` tracks the full tree.

---

## The round-trip invariant (verification)

```
original (FPF-Spec.md)
     │
     ▼ anchor.py
FPF-Spec-Anchored.md        # Every section wrapped in <H{level}_{id}>...</H{level}_{id}>
     │
     ▼ split.py
fpf-spec/                    # 228 extracted files + manifest.json
     │
     ▼ compile.py
FPF-Spec-Compiled.md         # Files concatenated back in order, tags stripped
     │
     ▼ verify.py
assert content_only(original) == content_only(compiled)
```

### `verify.py` does two checks:

1. **Content-only round-trip:** Strip all XML tags from both files and compare byte-for-byte. This catches missing content, wrong ordering, truncated sections, or stray whitespace changes.
2. **Tag integrity:** Verify that `FPF-Spec-Anchored.md` has:
   - Matching open/close tag counts for every tag
   - No nested tag violations (tags at same or different level must be properly nested)
   - Every tag ID is XML-safe (no `<`, `>`, `&`, spaces, etc.)

### Content stripping for comparison

Content is defined as: everything in the file with all `<H{level}_{id}>` and `</H{level}_{id}>` tags removed, plus trailing newline normalization (strip each line, then join with `\n\n` where multiple blank lines occur, then strip leading/trailing whitespace).

---

## Script signatures

```bash
# anchor.py — walk headings, emit XML-annotated file
python anchor.py [--input FPF-Spec.md] [--output FPF-Spec-Anchored.md]

# split.py — parse anchors, extract files, write manifest
python split.py [--input FPF-Spec-Anchored.md] [--output fpf-spec/]

# compile.py — read files in manifest order, write concatenated output
python compile.py [--input fpf-spec/] [--output FPF-Spec-Compiled.md]

# verify.py — round-trip comparison
python verify.py [--original FPF-Spec.md] [--compiled FPF-Spec-Compiled.md] [--anchored FPF-Spec-Anchored.md]
```

---

## anchor.py — Details

**Input:** Original `FPF-Spec.md`
**Output:** `FPF-Spec-Anchored.md`

### Heading detection regex

```python
H_RE = re.compile(
    r'^(?P<level>\#{1,6})\s+'                              # heading level
    r'(?P<bold>\*\*)?'                                      # optional **
    r'(?P<btick>`\s*)?'                                      # optional leading backtick
    r'(?P<sid>[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*)\s*'     # section ID (e.g. A.19.SURF-SPACE)
    r'(?P<sep>[-\u2013\u2014])?\s*'                          # separator (-, –, —)
    r'`?'                                                     # optional trailing backtick before title
    r'(?P<title>.+)$'                                         # rest is title
)
```

Headings **without** a pattern ID (Title, TOC, Preface sub-headings, Keywords, Part headers) are also anchored but use slugified titles as the tag identifier.

### Tag format

`<H{level}_{safe_id}>` → `</H{level}_{safe_id}>`

Examples:
```xml
<H1_S_Title>
# First Principles Framework (FPF) — Core Conceptual Specification
...
</H1_S_Title>

<H2_S_A_1>
## A.1 - Holonic Foundation: Entity → Holon
...
</H2_S_A_1>

<H3_S_A_19_SURF_SPACE_0>
### A.19.SURF-SPACE:0 - Use this when
...
</H3_S_A_19_SURF_SPACE_0>
```

### Safe ID generation

1. Take the section ID (or slugified title if no ID)
2. Replace all non-alphanumeric characters (except `_`) with `_`
3. Collapse multiple underscores
4. Strip leading/trailing underscores

### Section boundary logic

- A heading opens a tag. Its content extends from the heading line to just before the next heading line (same or any higher-level heading).
- The last section runs to end-of-file.
- Each section output: `<H{level}_{id}>\n` + all section lines + `\n</H{level}_{id}>\n`

### Validation

- Duplicate tag IDs → abort with error (print offending IDs)
- All IDs must be non-empty after sanitization
- Report stats on output (sections annotated, total lines, etc.)

---

## split.py — Details

**Input:** `FPF-Spec-Anchored.md`
**Output:** `fpf-spec/` directory tree + `fpf-spec/manifest.json`

### Parsing anchors

1. Read `FPF-Spec-Anchored.md`
2. Match `<H{level}_{id}>` open tags, `</H{level}_{id}>` close tags
3. Build stack to extract sections with: `{level, id, title, content_lines}`
4. Validate that every open tag has a matching close tag

### Section classification

Each section is classified into one of:

| Type | Criteria | Output location |
|---|---|---|
| `title` | Level 1, title contains "First Principles" or "Specification" | `fpf-spec/title.md` |
| `toc` | Level 1, title contains "Table of Content" | `fpf-spec/toc.md` |
| `preface_header` | Level 1, title contains "Preface" | `fpf-spec/preface.md` |
| `preface_essay` | Level 2, no pattern ID, falls under Preface | `fpf-spec/preface-subsections/{slug}.md` |
| `part_header` | Level 1, title starts with "Part [A-K]" | `fpf-spec/parts/part-{letter}-{slug}.md` |
| `keywords` | Title contains "Keywords" | `fpf-spec/keywords-discipline.md` |
| `pattern` | Level 2, has pattern ID matching `[A-K]\.[\d.]+` | `fpf-spec/patterns/{letter}/{slug}.md` |
| `other` | Everything else | `fpf-spec/others/` (flat, slug-named) |

### manifest.json structure

```json
{
  "version": 1,
  "source": "FPF-Spec.md",
  "sections": [
    {
      "id": "S_Title",
      "type": "title",
      "level": 1,
      "file": "title.md",
      "parent": null,
      "children": []
    },
    {
      "id": "S_A",
      "type": "part_header",
      "level": 1,
      "file": "parts/part-a-kernel-architecture.md",
      "parent": null,
      "children": [
        {
          "id": "S_A_0",
          "type": "pattern",
          "level": 2,
          "id_field": "A.0",
          "title": "Onboarding Glossary (NQD & E/E‑LOG)",
          "part": "A",
          "file": "patterns/a/a-0-onboarding-glossary.md",
          "parent": "S_A",
          "children": [
            {
              "id": "S_A_0_1",
              "type": "sub_heading",
              "level": 3,
              "id_field": "A.0:1",
              "file": null,
              "parent": "S_A_0",
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```

- `"file"` is `null` for sub-headings that stay within their parent's file.
- `"children"` is a list of child section dicts.
- Leaf sections (`pattern` type) have empty `children`.

### File content

Each extracted file contains:

```markdown
---
id: <section_id_field or null>
title: <title>
part: <letter or null>
level: <level_number>
parent: <parent_file or null>
source: FPF-Spec.md
---

<h2>A.1 - Holonic Foundation: Entity → Holon</h2>

... rest of content, preserving original markdown formatting ...
```

- The section heading line is preserved as-is (markdown heading).
- All nested content (sub-headings, paragraphs, tables, code blocks) is preserved exactly.

---

## compile.py — Details

**Input:** `fpf-spec/` directory tree
**Output:** `FPF-Spec-Compiled.md`

### Algorithm

1. Read `manifest.json`
2. Walk the section tree in document order (already in order from split)
3. For each leaf section (one with a `file`):
   - Read the file
   - Extract everything after the frontmatter block (first `---` delimiter pair)
   - Append to output
4. Join with single newline between sections
5. Strip leading/trailing whitespace

### Frontmatter handling

Frontmatter is delimited by `---` markers. Everything between the first and second `---` is stripped. The heading line and content after frontmatter are preserved verbatim.

---

## verify.py — Details

**Inputs:** `--original` (FPF-Spec.md), `--compiled` (FPF-Spec-Compiled.md), `--anchored` (FPF-Spec-Anchored.md)

### Check 1: Tag integrity (on anchored file)

- Count all `<H{level}_{id}>` and `</H{level}_{id}>` tags
- Every open must have a matching close (same id)
- No duplicate ids
- All ids are XML-safe
- Report pass/fail + stats

### Check 2: Round-trip content comparison

1. Strip all XML tags from both `--original` and `--compiled`:
   - Remove `<H{level}_{id}>` and `</H{level}_{id}>`
   - Normalize whitespace: collapse multiple blank lines to single blank line, strip per-line trailing whitespace, strip leading/trailing of whole document
2. Compare byte-for-byte
3. If mismatch: report first N differing lines with offsets

### Output

```
✓ Tag integrity: 5,457 tags (2,728 open, 2,728 close), 0 duplicates, 0 unsafe IDs
✓ Round-trip content: MATCH (6,318,099 bytes)
  - Original: 70,011 lines
  - Compiled: 70,011 lines
  - Diff size: 0 bytes
```

---

## Implementation order

1. **anchor.py** — Foundation. Without this, nothing else works.
2. **verify.py** (partial) — Write tag-integrity check first, to validate anchor.py output.
3. **split.py** — Extracts files and builds manifest.
4. **compile.py** — Reassembles files.
5. **verify.py** (complete) — Full round-trip check.

## Edge cases to handle

- Headings with backticks: `` `A.0` `` → sid = `A.0`
- Headings with quotes: `` `U.Commitment` `` → must be inside the pattern header, not a top-level heading
- Separators: `-`, `–` (en-dash), `—` (em-dash) — all three must be matched
- Level 1 headings that are not Part headers (Title, TOC, Preface)
- Preface sub-headings that are level 2 but have no pattern ID
- Sections with `### ...:End` markers (existing convention) — anchors should close at the natural boundary (before the next heading), which matches the existing behavior
- Tables, code blocks, blockquotes within sections — content is preserved verbatim
- Unicode characters in titles → slug must be safe for filenames

## Success criteria

1. `anchor.py` produces `FPF-Spec-Anchored.md` with zero duplicate/unsafe tags.
2. `split.py` produces `fpf-spec/` with all 228+ files and valid `manifest.json`.
3. `compile.py` produces `FPF-Spec-Compiled.md`.
4. `verify.py` reports full round-trip match with zero diff.
5. All scripts use only stdlib Python (no dependencies).
6. Each script runs in under 10 seconds on the 6.3MB input.
