#!/usr/bin/env python3
"""anchor.py — Walk headings in FPF-Spec.md, emit XML-annotated intermediate file.

Input:  Original FPF-Spec.md
Output: FPF-Spec-Anchored.md (every section wrapped in <H{level}_{id}>...</H{level}_{id}>)

Usage:  python anchor.py [--input FPF-Spec.md] [--output FPF-Spec-Anchored.md]
"""

import argparse
import re
import sys


# Regex to match heading level prefix
H_LEVEL_RE = re.compile(r'^(?P<level>\#{1,6})\s+')


def _parse_heading(line: str):
    """Parse a markdown heading line.

    Returns (level, sid | None, title, is_pattern_sid) or None if not a heading.
    """
    m = H_LEVEL_RE.match(line)
    if not m:
        return None

    level = len(m.group('level'))
    rest = line[m.end():]

    # Strip leading ** markers (markdown bold)
    if rest.startswith('**'):
        rest = rest[2:]
        # Strip trailing ** (markdown bold close)
        idx = rest.find('**')
        if idx > 0:
            rest = rest[:idx] + rest[idx + 2:]

    # Strip optional leading backtick
    if rest.startswith('`'):
        rest = rest[1:]

    # Try to extract pattern section ID: [A-Z]+.[...]
    # The ID must end with alnum — prevents trailing-dot captures like "A.2.6:17."
    sid_match = re.match(r'([A-Z]+\.[\dA-Za-z:.-]*[A-Za-z0-9]+)', rest)
    if sid_match:
        sid = sid_match.group(1)
        rest = rest[sid_match.end():]
        # Strip optional trailing backtick after sid
        if rest.startswith('`'):
            rest = rest[1:]
        # Strip optional separator (-, –, —)
        sep_match = re.match(r'([-–—])\s*', rest)
        if sep_match:
            rest = rest[sep_match.end():]
        title = rest.strip()
        is_pattern = True
    else:
        sid = None
        title = rest.strip()
        is_pattern = False

    return level, sid, title, is_pattern


def make_safe_id(sid: str | None, title: str) -> str:
    """Generate an XML-safe identifier from a section ID or slugified title."""
    if sid:
        safe = sid.replace('.', '_').replace('-', '_').replace(':', '_')
    else:
        safe = title.lower()
        safe = re.sub(r'[^a-z0-9]', '_', safe)
        safe = re.sub(r'_+', '_', safe)
        safe = safe.strip('_')

    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_')
    # XML tag names must start with a letter or underscore, not a digit
    if safe and safe[0].isdigit():
        safe = 's_' + safe
    if not safe:
        safe = 'section'
    return safe


def safe_for_xml_tag(value: str) -> bool:
    """Check if a value is safe for use as an XML tag name component."""
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_.\-]*$', value))


def main() -> None:
    parser = argparse.ArgumentParser(description='Annotate headings with XML tags')
    parser.add_argument('--input', default='FPF-Spec.md', help='Input markdown file')
    parser.add_argument('--output', default='FPF-Spec-Anchored.md', help='Output annotated file')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Discover all heading positions and parse them
    headings = []
    for i, line in enumerate(lines):
        parsed = _parse_heading(line)
        if parsed:
            headings.append((i, parsed))

    if not headings:
        print('ERROR: No headings found in input file.', file=sys.stderr)
        sys.exit(1)

    # Assign content lines to each section, auto-disambiguate duplicate IDs
    sections = []
    seen_tags: dict[str, int] = {}       # tag -> count of prior uses
    tag_counts: dict[str, int] = {}      # tag -> final count for disambiguation

    for idx, (pos, (level, sid, title, is_pattern)) in enumerate(headings):
        content_start = pos  # include heading line for round-trip fidelity
        if idx + 1 < len(headings):
            content_end = headings[idx + 1][0]
        else:
            content_end = len(lines)

        content_lines = lines[content_start:content_end]
        safe_id = make_safe_id(sid, title)
        tag = f'H{level}_{safe_id}'

        # Validate XML safety
        if not safe_for_xml_tag(tag):
            print(
                f"ERROR: Unsafe tag '{tag}' for heading on line {pos + 1}: "
                f"{title[:80]}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Track tag usage for reporting
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Apply disambiguation if duplicate, including collisions with
        # naturally suffixed IDs such as E_24_UK_1.
        final_safe_id = safe_id
        if f'H{level}_{final_safe_id}' in seen_tags:
            suffix = 1
            final_safe_id = f'{safe_id}_{suffix}'
            while f'H{level}_{final_safe_id}' in seen_tags:
                suffix += 1
                final_safe_id = f'{safe_id}_{suffix}'

        seen_tags[f'H{level}_{final_safe_id}'] = idx

        sections.append((level, sid, title, is_pattern, final_safe_id, content_lines))

    # Report any disambiguated duplicates
    dup_tags = {t: c for t, c in tag_counts.items() if c > 1}
    if dup_tags:
        print(f'⚠ Disambiguated {len(dup_tags)} duplicate tag(s):', file=sys.stderr)
        for tag, count in dup_tags.items():
            print(f'  {tag} × {count}', file=sys.stderr)

    # ---- Build a parent-child tree from flat sections ----
    class _Node:
        def __init__(self, level, sid, title, is_pattern, safe_id, content_lines):
            self.level = level
            self.sid = sid
            self.title = title
            self.is_pattern = is_pattern
            self.safe_id = safe_id
            self.content_lines = content_lines
            self.children = []

    root_nodes: list[_Node] = []
    stack: list[tuple[int, _Node]] = []  # (level, node)

    for level, sid, title, is_pattern, safe_id, content in sections:
        node = _Node(level, sid, title, is_pattern, safe_id, content)
        # Pop any siblings/ancestors that are not a parent of this node
        while stack and stack[-1][0] >= node.level:
            stack.pop()
        if stack:
            stack[-1][1].children.append(node)
        else:
            root_nodes.append(node)
        stack.append((node.level, node))

    def _write(node: _Node, out) -> None:
        tag = f'{node.level}_{node.safe_id}'
        out.write(f'<H{tag}>\n')
        # Heading line
        out.write(node.content_lines[0])
        # Content between heading and first child (or all content if no children)
        if len(node.content_lines) > 1:
            out.writelines(node.content_lines[1:])
        # Nest children
        for child in node.children:
            _write(child, out)
        out.write(f'</H{tag}>\n')

    # Write output
    with open(args.output, 'w', encoding='utf-8') as out:
        for node in root_nodes:
            _write(node, out)

    # Stats
    total_lines = sum(len(c) for _, _, _, _, _, c in sections)
    level_counts: dict[int, int] = {}
    for level, _, _, _, _, _ in sections:
        level_counts[level] = level_counts.get(level, 0) + 1

    pattern_count = sum(1 for _, _, _, is_p, _, _ in sections if is_p)
    structural_count = sum(1 for _, _, _, is_p, _, _ in sections if not is_p)

    print(f'✓ Wrote {args.output}')
    print(f'  - Sections annotated: {len(sections)}')
    print(f'  - Total content lines: {total_lines}')
    for lvl in sorted(level_counts):
        print(f'  - Level {lvl}: {level_counts[lvl]}')
    print(f'  - Pattern sections: {pattern_count}')
    print(f'  - Structural sections: {structural_count}')


if __name__ == '__main__':
    main()
