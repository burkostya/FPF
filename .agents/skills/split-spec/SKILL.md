---
name: split-spec
description: >
  Split, manage, and reassemble large monolithic markdown specification documents
  into a hierarchical file tree with manifest and full round-trip fidelity.
  Use when the user asks to split, compile, anchor, verify, re-run, or otherwise
  manipulate the FPF-Spec (or similar) pipeline: splitting a giant markdown file,
  managing the directory layout, reassembling to a single doc, or running the
  full anchor → split → compile → verify cycle.
---

# Split-Spec: Monolithic Markdown → Hierarchical File Tree

## Overview

A four-step Python pipeline that splits a single massive markdown specification
document (70 K+ lines) into a navigable file tree while preserving the exact
ability to reconstruct the original byte-for-byte.

**Scripts:** `scripts/anchor.py`, `scripts/split.py`, `scripts/compile.py`,
`scripts/verify.py`

**Input:** `FPF-Spec.md` — one flat markdown file with heading-based sections.

**Output:** `fpf-spec/` directory tree + `fpf-spec/manifest.json`.

## The Four Steps

```
FPF-Spec.md                →  FPF-Spec-Anchored.md  →  fpf-spec/
  (flat)                      (XML tags)               (tree + manifest)
    │  anchor.py                  │  split.py              │  compile.py
    ▼                             ▼                        ▼
  FPF-Spec-Anchored.md  ←  FPF-Spec-Compiled.md    verify.py
  (intermediate)            (reassembled)          (round-trip check)
```

### 1. Anchor — `anchor.py`

Walks headings in the original markdown, assigns each section a unique
XML-safe tag, and wraps content between `<H{level}_{id}>` … `</H{level}_{id}>`.

**What it does:**
- Parses heading levels (# through ######) and extracts pattern IDs
  (e.g. `A.6.RSIG`) from the heading text.
- Strips markdown bold (`**…**`) and backticks from heading titles.
- Auto-disambiguates duplicate IDs by appending `_1`, `_2` suffixes.
- Builds a parent-child tree from flat sections (stack-based depth tracking).
- Writes nested XML so children are properly enclosed in their parents.

**Usage:**
```bash
python scripts/anchor.py [--input FPF-Spec.md] [--output FPF-Spec-Anchored.md]
```

**Output:** Every heading is wrapped:
```markdown
<H1_part_a_kernel_architecture_cluster>
# **Part A – Kernel Architecture (Cluster)**

… section content …

## A.0 - System Context and Scope

**Tag.** Architectural pattern …

### A.0:1 - Problem

… sub-heading content …
</H1_part_a_kernel_architecture_cluster>
```

**Key details:**
- Content lines include the heading line itself (round-trip fidelity).
- Sub-headings (###–######) remain as siblings in the XML tree but
  their content is merged into the parent pattern file by `split.py`.
- Tag IDs are slugified: dots → `_`, spaces → `_`, lowercase.
  Example: `A.6.RSIG` → `A_6_RSIG`.

### 2. Split — `split.py`

Parses the anchored file, classifies each section, extracts files and a
manifest with a nested tree structure.

**What it does:**
- Builds an internal XML tree from the anchored tags using a stack.
- Traverses in pre-order (document order) to classify sections:
  - **Level 1** (`## H1`): `title`, `toc`, `preface_header`, `part_header`,
    `cluster_header`, `block_header`, `other`.
  - **Level 2** (`## H2`): `pattern` (e.g. `A_0`), `keywords`, `preface_essay`,
    `other`.
  - **Level 3–6** (###–######): `sub_heading` — content merged into parent.
- Writes files to the directory tree:

| Type | Location | Notes |
|------|----------|-------|
| title | `fpf-spec/title.md` | Document title |
| toc | `fpf-spec/toc.md` | Table of contents |
| keywords | `fpf-spec/keywords.md` | Keyword index |
| preface_header | `fpf-spec/preface/index.md` | Preface index |
| preface_essay | `fpf-spec/preface/<name>.md` | Each essay is separate |
| pattern | `fpf-spec/patterns/{letter}/{ID}.md` | e.g. `patterns/a/A_6_RSIG.md` |
| other | `fpf-spec/others/<name>.md` | Misc sections |
| part_header (header-only) | *(no file)* | Heading synthesized by compile.py |
| part_header/block_header (with table) | `fpf-spec/patterns/{letter}/index.md` | Summary table |

- Sub-heading content is merged into the parent pattern file.
- Part/Cluster nodes with substantive content (summary tables, etc.)
  go to `patterns/{letter}/index.md`.
- Header-only Part/Cluster nodes produce no file — their headings are
  synthesized by `compile.py` from the manifest tree.

- Builds `manifest.json` with a nested tree reflecting the document
  hierarchy. Two-phase parent matching:
  1. Exact `parent_tag` match via recursive tree search.
  2. Part-letter fallback for patterns nested under a previous pattern.

**Usage:**
```bash
python scripts/split.py [--input FPF-Spec-Anchored.md] [--output fpf-spec/]
```

**Directory structure:**
```
fpf-spec/
├── manifest.json              # Nested tree + metadata
├── title.md
├── toc.md
├── keywords.md
├── others/
│   └── *.md                   # Misc sections
├── preface/
│   ├── index.md               # Preface header + index
│   └── *.md                   # Individual essays (17 files)
├── patterns/
│   ├── a/
│   │   ├── A_0.md … A_21.md   # 72 pattern files
│   │   └── index.md           # Part C summary table (if present)
│   ├── b/
│   │   ├── B_*.md             # Pattern files
│   │   └── index.md           # Block B summary table
│   ├── c/ … g/ … h/ … i/ … j/
│   └── k/
└── parts/                     # (deprecated — no longer created)
```

**Manifest tree example:**
```json
{
  "version": 1,
  "source": "FPF-Spec.md",
  "sections": [
    {
      "id": "part_a_kernel_architecture_cluster",
      "type": "part_header",
      "level": 1,
      "file": null,
      "title": "# **Part A – Kernel Architecture (Cluster)**",
      "children": [
        {
          "id": "A_0",
          "type": "pattern",
          "level": 2,
          "file": "patterns/a/A_0.md",
          "title": "## A.0 - System Context and Scope",
          "children": [
            { "id": "s_1_problem", "type": "sub_heading", "file": null },
            …
          ]
        },
        { "id": "A_1", "type": "pattern", "file": "patterns/a/A_1.md" },
        …
      ]
    },
    …
  ]
}
```

### 3. Compile — `compile.py`

Walks the manifest tree and reassembles a single markdown document.

**What it does:**
- For nodes with a `file`: reads the file body (strips frontmatter).
- For `part_header`/`block_header` with `file: null`: emits the heading
  text directly (e.g. `# **Part G – Discipline SoTA Patterns Kit\n\n`).
- Skips `sub_heading` nodes — their content was already merged into the
  parent pattern file during splitting.
- Concatenates all parts in document order from the tree traversal.

**Usage:**
```bash
python scripts/compile.py [--input fpf-spec/] [--output FPF-Spec-Compiled.md]
```

**Compiled output characteristics:**
- Heading-only Part/Cluster nodes emit just the `#` line (no file on disk).
- Part/Block nodes with tables emit the full file content.
- Sub-heading sections produce no output (content is in the parent file).

### 4. Verify — `verify.py`

Checks tag integrity and round-trip fidelity.

**Two checks:**
1. **Tag Integrity:** Open/close tags match, nesting is LIFO-correct,
   no duplicates, no unsafe ID characters.
2. **Round-Trip Comparison:** Strips all XML tags from original and
   compiled, normalizes whitespace (collapse multiple blank lines,
   strip per-line trailing whitespace), and does a byte-level comparison.

**Usage:**
```bash
python scripts/verify.py \
  [--original FPF-Spec.md] \
  [--compiled FPF-Spec-Compiled.md] \
  [--anchored FPF-Spec-Anchored.md]
```

## Full Pipeline

```bash
# Run the complete cycle
python scripts/anchor.py
python scripts/split.py
python scripts/compile.py
python scripts/verify.py
```

**Expected output on success:**
```
✓ ALL CHECKS PASSED
```

**Typical stats for FPF-Spec.md (70,011 lines / 6.3 MB):**
- 5,457 headings annotated (17 L1, 228 L2, 5,212 L3–L6)
- 237 files written to `fpf-spec/`
- 207 pattern files across 11 part directories (a–k)
- 17 preface essays + 1 preface index
- Byte-identical round-trip (6,223,430 bytes)

## Re-running After Changes

If the original specification changes:

```bash
# 1. Clean previous outputs
rm -f FPF-Spec-Anchored.md FPF-Spec-Compiled.md
rm -rf fpf-spec/

# 2. Re-run the pipeline
python scripts/anchor.py
python scripts/split.py
python scripts/compile.py
python scripts/verify.py
```

Always verify the last step passes before proceeding.

## Modifying the Pipeline

### Adding new section types

In `split.py`, modify `classify_section()`:
1. Add a detection regex at the top (e.g. `NEW_TYPE_RE = re.compile(...)`).
2. Add a `if NEW_TYPE_RE.search(tag_id)` branch in `classify_section()`.
3. Update `make_frontmatter()` to handle the new type's frontmatter fields.

### Changing directory layout

Modify the `file` return values in `classify_section()` and the
directory creation/mapping in the file-writing loop and manifest tree builder.

### Handling new special sections

If a new section type should produce an `index.md` per-part like
summary tables: the logic in the file-writing loop already checks for
`part_header`/`block_header` with content and writes to
`patterns/{letter}/index.md`. Add new type checks in the same block.

## Common Issues

### Round-trip fails

- **Sub-heading content lost:** Ensure `split.py`'s pre-order traversal
  is correct (`_preorder_all` must process all root nodes).
- **Whitespace changes:** The `verify.py` normalizer collapses 2+ blank
  lines into 1. This is intentional. If the original uses triple blank
  lines deliberately, adjust the normalizer.
- **Missing file:** Check that `compile.py`'s `collect_parts_and_files()`
  walks the manifest tree correctly.

### Manifest tree has flat structure

- Phase 1 must use recursive `_find_node_by_id()` for exact parent matching.
- Phase 2 part-letter fallback only triggers when Phase 1 fails.
- Part/Cluster header nodes must be registered in `header_nodes` and
  `node_registry` for child lookups.

### Duplicate tag errors

`anchor.py` auto-disambiguates by appending `_1`, `_2` suffixes.
If you see disambiguation warnings, these are expected for known
duplicate section IDs (e.g. `A.2.6:17` appears twice in the original).

## Architecture Notes

### Why XML tags, not a format-specific parser?

The anchored format wraps content in `<H{level}_{id}>` … `</H{level}_{id}>`
which preserves every byte of the original while providing machine-parseable
section boundaries. This approach:
- Works with any markdown-flavored document.
- Preserves inline formatting (tables, code blocks, HTML).
- Enables LIFO-nesting verification.
- Requires zero assumptions about frontmatter or YAML semantics.

### Why manifest.json is a tree, not a flat list?

The manifest encodes the full document hierarchy so that `compile.py` can
reconstruct the correct document order without relying on filesystem
naming conventions. Part/Cluster headers with no file still appear in the
tree so their headings can be synthesized during compilation.

### Sub-heading content merging

Sub-headings (###–######) do not produce files. Their content is merged
into the parent pattern file during the split step. This means the parent
pattern file contains the full narrative — heading → content → sub-heading
→ content — exactly as it appeared in the original document.
