#!/usr/bin/env python3
"""verify.py — Round-trip verification of the anchor→split→compile pipeline.

Checks:
1. Tag integrity on the anchored file (matching open/close, no unsafe IDs)
2. Content-only round-trip comparison (original vs compiled, tags stripped)

Usage:  python verify.py
        [--original FPF-Spec.md]
        [--compiled FPF-Spec-Compiled.md]
        [--anchored FPF-Spec-Anchored.md]
"""

import argparse
import re
import sys


TAG_RE = re.compile(r'<H([1-6])_(.+?)>')
CLOSING_TAG_RE = re.compile(r'</H([1-6])_(.+?)>')


def strip_xml_tags(text: str) -> str:
    """Remove all <H{level}_{id}> and </H{level}_{id}> tags."""
    text = re.sub(r'<H[1-6]_[^>]+>', '', text)
    text = re.sub(r'</H[1-6]_[^>]+>', '', text)
    return text


def normalize_content(text: str) -> str:
    """Strip XML tags and normalize whitespace for comparison."""
    text = strip_xml_tags(text)
    # Normalize: strip trailing whitespace per line, collapse multiple blank lines,
    # strip leading/trailing whitespace of whole document
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]
    # Collapse 2+ consecutive blank lines into 1
    result = []
    blank_count = 0
    for line in lines:
        if line == '':
            blank_count += 1
            if blank_count <= 1:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    return '\n'.join(result).strip()


def check_tag_integrity(filepath: str) -> dict:
    """Verify tag matching and safety in the anchored file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    open_tags = TAG_RE.findall(content)
    close_tags = CLOSING_TAG_RE.findall(content)

    open_count = len(open_tags)
    close_count = len(close_tags)
    total = open_count + close_count

    # Check matching counts
    match = open_count == close_count

    # Build open/close maps for matching
    open_map: dict[str, list[int]] = {}
    close_map: dict[str, list[int]] = {}

    # Find positions of open tags
    for m in TAG_RE.finditer(content):
        level, sid = m.group(1), m.group(2)
        open_map.setdefault(f'{level}_{sid}', []).append(m.start())

    # Find positions of close tags
    for m in CLOSING_TAG_RE.finditer(content):
        level, sid = m.group(1), m.group(2)
        close_map.setdefault(f'{level}_{sid}', []).append(m.start())

    # Check duplicates
    dup_count = 0
    for tag, positions in open_map.items():
        if len(positions) > 1:
            dup_count += 1

    # Check unsafe IDs
    unsafe_ids = []
    xml_name_re = re.compile(r'^[A-Za-z_][A-Za-z0-9_.\-]*$')
    for m in TAG_RE.finditer(content):
        sid = m.group(2)
        if not xml_name_re.match(sid):
            unsafe_ids.append(sid)

    # Check nesting: open tags should be matched in LIFO order
    nesting_ok = True
    if match:
        stack: list[str] = []
        # Interleave opens and closes by position
        all_tags: list[tuple[int, str, bool]] = []  # (pos, tag, is_open)
        for m in TAG_RE.finditer(content):
            all_tags.append((m.start(), f'{m.group(1)}_{m.group(2)}', True))
        for m in CLOSING_TAG_RE.finditer(content):
            all_tags.append((m.start(), f'{m.group(1)}_{m.group(2)}', False))
        all_tags.sort(key=lambda x: x[0])

        for pos, tag, is_open in all_tags:
            if is_open:
                stack.append(tag)
            else:
                if stack and stack[-1] == tag:
                    stack.pop()
                else:
                    nesting_ok = False
                    break

    stats = {
        'total_tags': total,
        'open_count': open_count,
        'close_count': close_count,
        'match': match,
        'nesting_ok': nesting_ok,
        'dup_count': dup_count,
        'unsafe_count': len(unsafe_ids),
        'unsafe_ids': unsafe_ids[:5],  # limit output
    }
    return stats


def check_round_trip(original_path: str, compiled_path: str) -> dict:
    """Compare content-only representations of original and compiled files."""
    with open(original_path, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(compiled_path, 'r', encoding='utf-8') as f:
        compiled = f.read()

    orig_norm = normalize_content(original)
    comp_norm = normalize_content(compiled)

    match = orig_norm == comp_norm

    result = {
        'original_size': len(original),
        'compiled_size': len(compiled),
        'original_lines': original.count('\n') + (1 if original and not original.endswith('\n') else 0),
        'compiled_lines': compiled.count('\n') + (1 if compiled and not compiled.endswith('\n') else 0),
        'match': match,
    }

    if not match:
        # Find first difference
        for i, (a, b) in enumerate(zip(orig_norm, comp_norm)):
            if a != b:
                # Show context around first diff
                start = max(0, i - 100)
                end = min(len(orig_norm), i + 100)
                result['first_diff_offset'] = i
                result['orig_context'] = orig_norm[start:end].replace('\n', '\\n')
                result['comp_context'] = comp_norm[start:end].replace('\n', '\\n')
                break
        else:
            # Files differ in length
            result['length_diff'] = abs(len(orig_norm) - len(comp_norm))
            result['shorter'] = 'compiled' if len(comp_norm) < len(orig_norm) else 'original'

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description='Round-trip verification')
    parser.add_argument('--original', default='FPF-Spec.md', help='Original spec file')
    parser.add_argument('--compiled', default='FPF-Spec-Compiled.md', help='Compiled spec file')
    parser.add_argument('--anchored', default='FPF-Spec-Anchored.md', help='Anchored spec file')
    args = parser.parse_args()

    all_pass = True

    # Check 1: Tag integrity
    print('=== Check 1: Tag Integrity ===')
    stats = check_tag_integrity(args.anchored)

    print(f"  Total tags: {stats['total_tags']:,}")
    print(f"  Open: {stats['open_count']:,} / Close: {stats['close_count']:,}")
    print(f"  Matched: {'✓' if stats['match'] else '✗'}")
    print(f"  Nesting correct: {'✓' if stats['nesting_ok'] else '✗'}")
    print(f"  Duplicates: {stats['dup_count']}")
    print(f"  Unsafe IDs: {stats['unsafe_count']}")
    if stats['unsafe_ids']:
        for uid in stats['unsafe_ids']:
            print(f"    - {uid}")

    tag_pass = stats['match'] and stats['nesting_ok'] and stats['dup_count'] == 0 and stats['unsafe_count'] == 0
    if not tag_pass:
        all_pass = False
    print(f"  Result: {'✓ PASS' if tag_pass else '✗ FAIL'}")
    print()

    # Check 2: Round-trip content comparison
    print('=== Check 2: Round-Trip Content ===')
    rt = check_round_trip(args.original, args.compiled)

    print(f"  Original: {rt['original_size']:,} bytes ({rt['original_lines']:,} lines)")
    print(f"  Compiled: {rt['compiled_size']:,} bytes ({rt['compiled_lines']:,} lines)")

    if not rt['match']:
        diff_size = abs(rt['original_size'] - rt['compiled_size'])
        print(f"  Size diff: {diff_size:,} bytes")
        if 'first_diff_offset' in rt:
            print(f"  First difference at offset {rt['first_diff_offset']:,}")
            print(f"    Original:  ...{rt['orig_context']}...")
            print(f"    Compiled:  ...{rt['comp_context']}...")
        if 'length_diff' in rt:
            print(f"  Length diff: {rt['length_diff']:,} characters")

    rt_pass = rt['match']
    if not rt_pass:
        all_pass = False
    print(f"  Result: {'✓ PASS' if rt_pass else '✗ FAIL'}")
    print()

    # Final verdict
    print('=' * 40)
    if all_pass:
        print('✓ ALL CHECKS PASSED')
    else:
        print('✗ SOME CHECKS FAILED')
    sys.exit(0 if all_pass else 1)


if __name__ == '__main__':
    main()
