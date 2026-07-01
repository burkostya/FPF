#!/usr/bin/env python3
"""compile.py — Reassemble split files back into a single markdown document.

Input:  fpf-spec/ directory tree (read manifest.json for ordering)
Output: FPF-Spec-Compiled.md (files concatenated back, frontmatter stripped)

Part/Cluster nodes without a file produce synthetic headings.
Part/Cluster nodes with a file (e.g. Part C with its table) produce
full content. Pattern nodes produce their file bodies.

Usage:  python compile.py [--input fpf-spec/] [--output FPF-Spec-Compiled.md]
"""

import argparse
import json
import os
import re
import sys


FRONTMATTER_RE = re.compile(r'^---\s*\n', re.MULTILINE)


def extract_body(file_path: str) -> str:
    """Extract content from a markdown file, stripping the frontmatter block."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find frontmatter boundaries
    first_dashes = content.find('---')
    if first_dashes < 0:
        return content  # no frontmatter, return everything

    after_first = content[first_dashes + 3:]
    second_dashes = after_first.find('\n---')
    if second_dashes < 0:
        return content  # malformed frontmatter, return everything

    # Strip the heading line and any blank lines after frontmatter
    body = after_first[second_dashes + 4:]  # skip '\n---'

    # Strip leading blank lines (frontmatter leaves a blank line before heading)
    body = body.lstrip('\n')

    # Ensure trailing newline
    if body and not body.endswith('\n'):
        body += '\n'

    return body


def collect_parts_and_files(node: dict, result: list):
    """Walk the manifest tree, collecting Part headings and files in order.

    Part/Cluster nodes without a file produce a synthetic heading.
    Part/Cluster nodes with a file produce the full file content.
    Leaf file-producing nodes produce their file content.
    Sub_heading nodes without their own file are NOT emitted - their content
    is already included in the nearest ancestor file. Large subsection nodes
    with a file are emitted like any other file-producing node.
    """
    if node.get('file'):
        # Has a file - output the file body
        result.append(('file', node['file']))
    elif node['type'] in ('part_header', 'block_header'):
        # No file but is a Part/Cluster header - synthesize the heading
        result.append(('heading', node['title']))
    # sub_heading nodes without a file are skipped because their content was
    # merged into the nearest ancestor file.
    for child in node.get('children', []):
        collect_parts_and_files(child, result)


def main() -> None:
    parser = argparse.ArgumentParser(description='Compile split files back to single doc')
    parser.add_argument('--input', default='fpf-spec/', help='Split directory')
    parser.add_argument('--output', default='FPF-Spec-Compiled.md', help='Output file')
    args = parser.parse_args()

    manifest_path = os.path.join(args.input, 'manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Collect parts+files in document order
    items = []
    for section in manifest['sections']:
        collect_parts_and_files(section, items)

    # Concatenate all items
    parts = []
    for kind, value in items:
        if kind == 'file':
            full_path = os.path.join(args.input, value)
            body = extract_body(full_path)
            parts.append(body)
        elif kind == 'heading':
            # Output the Part/Cluster heading as-is (already has # prefix)
            parts.append(value + '\n\n')

    compiled = ''.join(parts).lstrip('\n')
    # Ensure single trailing newline
    compiled = compiled.rstrip('\n') + '\n'

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(compiled)

    # Stats
    print(f'✓ Wrote {args.output}')
    print(f'  - Parts assembled: {len(items)}')
    print(f'  - Total size: {len(compiled):,} bytes')
    print(f'  - Lines: {compiled.count(chr(10)):,}')


if __name__ == '__main__':
    main()
