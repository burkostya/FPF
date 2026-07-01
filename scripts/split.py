#!/usr/bin/env python3
"""split.py — Parse anchored file, extract files + manifest.json.

Input:  FPF-Spec-Anchored.md
Output: fpf-spec/ directory tree + fpf-spec/manifest.json

Key: sub-heading content (###–######) is normally merged into the nearest
file-producing parent. Large sub-heading subtrees are split into their own
files, and their immediate sibling sub-headings are promoted to files too so
compile.py can preserve document order.

Usage:  python split.py [--input FPF-Spec-Anchored.md] [--output fpf-spec/]
"""

import argparse
import json
import os
import re
import shutil
import sys


# Tag parsing
OPEN_TAG_RE = re.compile(r'^<H([1-6])_(.+?)>$')
CLOSE_TAG_RE = re.compile(r'^</H([1-6])_(.+?)>$')

# Detection regexes (match against tag_id which uses underscores)
TITLE_RE = re.compile(r'^first_principles', re.IGNORECASE)
TOC_RE = re.compile(r'^table_of_content', re.IGNORECASE)
PREFACE_RE = re.compile(r'^preface', re.IGNORECASE)
PART_HEADER_RE = re.compile(r'^part_([a-z])', re.IGNORECASE)
CLUSTER_HEADER_RE = re.compile(r'^cluster_([a-z])', re.IGNORECASE)
KEYWORDS_RE = re.compile(r'^keywords', re.IGNORECASE)
BLOCK_HEADER_RE = re.compile(r'^block_([a-z])', re.IGNORECASE)
PART_LETTER_RE = re.compile(r'^([A-K])_')
NSTD_PATTERN_RE = re.compile(r'^(NSTD)_\d+(?:_|$)', re.IGNORECASE)
SUBSECTION_SPLIT_WORD_THRESHOLD = 5000
DPF_NSTD_SUBSECTION_SPLIT_WORD_THRESHOLD = 1500


def slug_path(tag_id: str) -> str:
    """Create a stable lowercase file slug from a tag id."""
    return tag_id.lower()


def classify_fpf_section(level, tag_id, in_preface):
    """Classify a section and determine its output file path."""
    if level == 1:
        if TITLE_RE.search(tag_id):
            return {'type': 'title', 'file': 'title.md', 'part': None}
        if TOC_RE.search(tag_id):
            return {'type': 'toc', 'file': 'toc.md', 'part': None}
        if PREFACE_RE.search(tag_id):
            return {'type': 'preface_header', 'file': 'preface/index.md', 'part': None}
        m = PART_HEADER_RE.search(tag_id)
        if m:
            letter = m.group(1).lower()
            return {'type': 'part_header', 'file': f'parts/part-{letter}.md', 'part': letter.upper()}
        m = CLUSTER_HEADER_RE.search(tag_id)
        if m:
            letter = m.group(1).lower()
            return {'type': 'part_header', 'file': f'parts/part-{letter}-cluster-{tag_id}.md', 'part': letter.upper()}
        m = BLOCK_HEADER_RE.search(tag_id)
        if m:
            letter = m.group(1).lower()
            return {'type': 'block_header', 'file': f'parts/block-{letter}.md', 'part': letter.upper()}
        return {'type': 'other', 'file': f'others/{tag_id}.md', 'part': None}

    if level == 2:
        m = PART_LETTER_RE.match(tag_id)
        if m:
            letter = m.group(1)
            return {'type': 'pattern', 'file': f'patterns/{letter.lower()}/{tag_id}.md', 'part': letter.upper()}
        if KEYWORDS_RE.search(tag_id):
            return {'type': 'keywords', 'file': 'keywords.md', 'part': None}
        if in_preface:
            return {'type': 'preface_essay', 'file': f'preface/{tag_id}.md', 'part': None}
        return {'type': 'other', 'file': f'others/{tag_id}.md', 'part': None}

    return {'type': 'sub_heading', 'file': None, 'part': None}


def classify_dpf_nstd_section(level, tag_id, in_preface):
    """Classify sections for the NSTD Domain Principle Framework document."""
    if level == 1:
        if tag_id == 'narrativization_and_narrative_studies_principles_framework':
            return {'type': 'title', 'file': 'title.md', 'part': None}
        if TOC_RE.search(tag_id):
            return {'type': 'toc', 'file': 'toc.md', 'part': None}
        if tag_id.startswith('readme'):
            return {'type': 'readme_header', 'file': 'readme/index.md', 'part': None}
        if tag_id.startswith('preface'):
            return {'type': 'preface_header', 'file': 'preface/index.md', 'part': None}
        return {'type': 'other', 'file': f'others/{slug_path(tag_id)}.md', 'part': None}

    if level == 2:
        if NSTD_PATTERN_RE.match(tag_id):
            return {
                'type': 'dpf_pattern',
                'file': f'patterns/nstd/{tag_id}.md',
                'part': 'NSTD',
            }
        if tag_id.startswith('first_practical_entry'):
            return {'type': 'readme_entry', 'file': f'readme/{slug_path(tag_id)}.md', 'part': None}
        if tag_id in (
            'package_carrier_structure_account_note',
            'package_boundary_and_owner_routing',
            'pattern_index',
        ):
            return {'type': 'framework', 'file': f'framework/{slug_path(tag_id)}.md', 'part': None}
        if tag_id == 'heterogeneous_acceptance_cases':
            return {'type': 'acceptance', 'file': 'acceptance/index.md', 'part': None}
        if (
            tag_id == 'support_maps'
            or tag_id.endswith('_bridge')
            or tag_id.endswith('_map')
            or tag_id in ('name_and_edition_route', 'dpf_relation_records', 'refresh_route')
        ):
            filename = 'index.md' if tag_id == 'support_maps' else f'{slug_path(tag_id)}.md'
            return {'type': 'support', 'file': f'support/{filename}', 'part': None}
        if in_preface:
            return {'type': 'preface_essay', 'file': f'preface/{slug_path(tag_id)}.md', 'part': None}
        return {'type': 'other', 'file': f'others/{slug_path(tag_id)}.md', 'part': None}

    return {'type': 'sub_heading', 'file': None, 'part': None}


def classify_section(level, tag_id, in_preface, profile):
    """Classify a section for a concrete split profile."""
    if profile == 'dpf-nstd':
        return classify_dpf_nstd_section(level, tag_id, in_preface)
    return classify_fpf_section(level, tag_id, in_preface)


def make_frontmatter(sec):
    """Generate YAML frontmatter for a section file."""
    lines = ['---']
    lines.append(f'source: {sec["source"]}')

    if sec['type'] in ('pattern', 'dpf_pattern'):
        lines.append(f'id: {sec["tag_id"]}')
        lines.append(f'title: {sec["title"]}')
        lines.append(f'part: {sec["part"]}')
        lines.append(f'level: {sec["level"]}')
        lines.append(f'parent: {sec["parent_part"]}')
    else:
        lines.append(f'title: {sec["title"]}')
        lines.append(f'level: {sec["level"]}')
        if sec.get('part'):
            lines.append(f'part: {sec["part"]}')

    lines.append('---')
    return '\n'.join(lines)


# ---- XML-tree node for stack-based parsing ----
class _Node:
    __slots__ = ('level', 'tag_id', 'content_lines', 'in_preface', 'children',
                 'classification', 'title', 'parent_file', 'parent_part',
                 'file_path', 'subtree_words')

    def __init__(self, level, tag_id, in_preface):
        self.level = level
        self.tag_id = tag_id
        self.content_lines = []
        self.in_preface = in_preface
        self.children = []
        self.classification = None
        self.title = ''
        self.parent_file = None
        self.parent_part = None
        self.file_path = None
        self.subtree_words = 0


def _preorder(node):
    """Yield nodes in document (pre-order) order."""
    yield node
    for child in node.children:
        yield from _preorder(child)


def clean_output_dir(output_dir):
    """Remove files and directories generated by this splitter."""
    generated_paths = [
        'manifest.json',
        'title.md',
        'toc.md',
        'keywords.md',
        'patterns',
        'preface',
        'others',
        'parts',
        'readme',
        'framework',
        'acceptance',
        'support',
    ]
    for rel_path in generated_paths:
        path = os.path.join(output_dir, rel_path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)


def count_subtree_words(node: _Node) -> int:
    """Count words in this node's direct content and all descendants."""
    node.subtree_words = len('\n'.join(node.content_lines).split())
    for child in node.children:
        node.subtree_words += count_subtree_words(child)
    return node.subtree_words


def subsection_file_path(parent_file: str, tag_id: str) -> str:
    """Create a stable child file path under the nearest file parent."""
    base, _ = os.path.splitext(parent_file)
    return f'{base}/{tag_id}.md'


def collect_file_content(node: _Node) -> list[str]:
    """Collect content owned by this file, excluding child file sections."""
    lines = list(node.content_lines)
    for child in node.children:
        if child.file_path is None:
            lines.extend(collect_file_content(child))
    return lines


def has_substantive_direct_content(node: _Node) -> bool:
    """Return true when a node has non-heading direct content."""
    return any(line.strip() for line in node.content_lines[1:])


def infer_source_path(input_path: str) -> str:
    """Infer the original source markdown path from the anchored path."""
    base = os.path.basename(input_path)
    if base == 'FPF-Spec-Anchored.md':
        return 'FPF-Spec.md'
    suffix = '-Anchored.md'
    if base.endswith(suffix):
        return base[:-len(suffix)] + '.md'
    return base


def detect_profile(profile: str, source_path: str, root_nodes: list[_Node]) -> str:
    """Resolve auto profile from source path or first title."""
    if profile != 'auto':
        return profile
    source_key = source_path.lower()
    if 'narrativization' in source_key or 'narrative-studies' in source_key:
        return 'dpf-nstd'
    first_title = root_nodes[0].content_lines[0].lower() if root_nodes and root_nodes[0].content_lines else ''
    if 'narrativization and narrative studies' in first_title:
        return 'dpf-nstd'
    return 'fpf'


def main():
    parser = argparse.ArgumentParser(description='Split anchored file into directory tree')
    parser.add_argument('--input', default='FPF-Spec-Anchored.md', help='Anchored input file')
    parser.add_argument('--output', default='fpf-spec/', help='Output directory')
    parser.add_argument(
        '--source',
        default=None,
        help='Original markdown source path stored in manifest/frontmatter',
    )
    parser.add_argument(
        '--profile',
        choices=('auto', 'fpf', 'dpf-nstd'),
        default='auto',
        help='Section classification profile',
    )
    parser.add_argument(
        '--subsection-word-threshold',
        type=int,
        default=None,
        help='Split level 3-6 sub-heading subtrees with children at or above this word count',
    )
    args = parser.parse_args()
    source_path = args.source or infer_source_path(args.input)

    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # ---- Build the XML tree using a stack ----
    root_nodes: list[_Node] = []
    stack: list[_Node] = []
    in_preface = False

    for line in lines:
        open_m = OPEN_TAG_RE.match(line.strip())
        close_m = CLOSE_TAG_RE.match(line.strip())

        if open_m:
            level = int(open_m.group(1))
            tag_id = open_m.group(2)

            if level == 1:
                if 'preface' in tag_id and 'part' not in tag_id:
                    in_preface = True
                elif 'part' in tag_id or 'cluster' in tag_id:
                    in_preface = False

            node = _Node(level, tag_id, in_preface)

            if stack:
                stack[-1].children.append(node)
            else:
                root_nodes.append(node)

            stack.append(node)

        elif close_m:
            if stack:
                stack.pop()
            else:
                print(
                    'WARNING: Closing tag with no matching open tag',
                    file=sys.stderr,
                )

        elif stack:
            stack[-1].content_lines.append(line)

    profile = detect_profile(args.profile, source_path, root_nodes)
    if args.subsection_word_threshold is None:
        subsection_word_threshold = (
            DPF_NSTD_SUBSECTION_SPLIT_WORD_THRESHOLD
            if profile == 'dpf-nstd'
            else SUBSECTION_SPLIT_WORD_THRESHOLD
        )
    else:
        subsection_word_threshold = args.subsection_word_threshold

    for root in root_nodes:
        count_subtree_words(root)

    file_sections = []       # sections that produce files
    manifest_entries = []    # all sections for manifest
    title_seen = False

    def classify_tree(
        node: _Node,
        current_part: str | None,
        nearest_file: _Node | None,
    ) -> None:
        nonlocal title_seen

        node.classification = classify_section(node.level, node.tag_id, node.in_preface, profile)
        if node.classification['type'] == 'title':
            if title_seen:
                node.classification = {
                    'type': 'other',
                    'file': f'others/{node.tag_id}.md',
                    'part': None,
                }
            else:
                title_seen = True

        if node.level == 1 and node.classification['type'] == 'part_header' and node.classification.get('part'):
            current_part = node.classification['part']

        node.title = node.content_lines[0].strip() if node.content_lines else ''
        node.parent_part = current_part
        node.parent_file = nearest_file.tag_id if nearest_file else None

        if node.classification['file'] is not None:
            node.file_path = node.classification['file']
            if node.classification['type'] in ('part_header', 'block_header'):
                if not has_substantive_direct_content(node):
                    node.file_path = None
                else:
                    letter = node.classification.get('part', '').lower()
                    if letter:
                        node.file_path = f'patterns/{letter}/index.md'
        elif (
            nearest_file is not None
            and node.level >= 3
            and node.children
            and node.subtree_words >= subsection_word_threshold
        ):
            node.classification = {
                'type': 'subsection',
                'file': subsection_file_path(nearest_file.file_path, node.tag_id),
                'part': current_part,
            }
            node.file_path = node.classification['file']

        manifest_entries.append(node)
        if node.file_path is not None:
            file_sections.append(node)
            nearest_file = node

        for child in node.children:
            classify_tree(child, current_part, nearest_file)

    for root in root_nodes:
        classify_tree(root, None, None)

    def promote_order_boundary_children(node: _Node) -> None:
        """Keep sibling ordering when one child is split into its own file."""
        if node.file_path and any(child.file_path for child in node.children):
            for child in node.children:
                if child.file_path is None and child.content_lines:
                    child.classification = {
                        'type': 'subsection',
                        'file': subsection_file_path(node.file_path, child.tag_id),
                        'part': node.parent_part,
                    }
                    child.file_path = child.classification['file']
                    file_sections.append(child)

        for child in node.children:
            promote_order_boundary_children(child)

    for root in root_nodes:
        promote_order_boundary_children(root)

    # ---- Write files ----
    # Skip Part/Cluster headers that are header-only (no direct content
    # beyond the heading line). These headings are synthesized by compile.py
    # from the manifest tree instead. Part/Block nodes with real content
    # (summary tables) are written into patterns/{letter}/index.md.
    clean_output_dir(args.output)
    os.makedirs(os.path.join(args.output, 'patterns'), exist_ok=True)
    os.makedirs(os.path.join(args.output, 'preface'), exist_ok=True)
    os.makedirs(os.path.join(args.output, 'others'), exist_ok=True)

    file_count = 0
    for sec in file_sections:
        file_path = sec.file_path
        if file_path is None:
            continue

        full_path = os.path.join(args.output, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        frontmatter = make_frontmatter({
            'type': sec.classification['type'],
            'source': source_path,
            'tag_id': sec.tag_id,
            'title': sec.title,
            'level': sec.level,
            'part': sec.classification.get('part'),
            'parent_part': sec.parent_part,
        })
        owned_lines = collect_file_content(sec)
        heading_line = owned_lines[0] if owned_lines else ''
        content_body = '\n'.join(owned_lines[1:]) if len(owned_lines) > 1 else ''
        full_content = f'{frontmatter}\n{heading_line}\n{content_body}\n'

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        file_count += 1

    # ---- Build manifest tree ----
    def manifest_node(entry: _Node) -> dict:
        node = {
            'id': entry.tag_id,
            'type': entry.classification['type'],
            'level': entry.level,
            'file': entry.file_path if entry.file_path else None,
            'title': entry.title,
            'children': [],
        }
        if entry.classification.get('part'):
            node['part'] = entry.classification['part']
        node['children'] = [manifest_node(child) for child in entry.children]
        return node

    tree = [manifest_node(root) for root in root_nodes]

    manifest = {
        'version': 1,
        'source': source_path,
        'profile': profile,
        'sections': tree,
    }

    manifest_path = os.path.join(args.output, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Stats
    type_counts: dict[str, int] = {}
    for s in manifest_entries:
        t = s.classification['type']
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f'✓ Wrote {args.output}/')
    print(f'  - Profile: {profile}')
    print(f'  - Source: {source_path}')
    print(f'  - Subsection word threshold: {subsection_word_threshold}')
    print(f'  - Files written: {file_count}')
    print(f'  - Manifest: {manifest_path}')
    for t, c in sorted(type_counts.items()):
        print(f'    - {t}: {c}')


if __name__ == '__main__':
    main()
