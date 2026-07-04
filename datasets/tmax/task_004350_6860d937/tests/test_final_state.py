# test_final_state.py

import os
import pytest

def parse_semver(v):
    """Parse a semver string into a tuple of integers for comparison."""
    return tuple(map(int, v.strip().split('.')))

def test_resolved_version_correctness():
    avail_path = "/home/user/semver-resolve/available.txt"
    const_path = "/home/user/semver-resolve/constraints.txt"
    out_path = "/home/user/resolved_version.txt"

    assert os.path.exists(out_path), f"Output file not found: {out_path}"
    assert os.path.exists(avail_path), f"Available versions file missing: {avail_path}"
    assert os.path.exists(const_path), f"Constraints file missing: {const_path}"

    with open(avail_path, 'r', encoding='utf-8') as f:
        available = [line.strip() for line in f if line.strip()]

    with open(const_path, 'rb') as f:
        raw_constraints = f.read()

    # The user might have transcoded the file in place or left it as UTF-16LE.
    try:
        if b'\x00' in raw_constraints:
            text_constraints = raw_constraints.decode('utf-16le')
        else:
            text_constraints = raw_constraints.decode('utf-8')
    except UnicodeDecodeError:
        text_constraints = raw_constraints.decode('utf-8', errors='ignore')

    constraints = [line.strip() for line in text_constraints.splitlines() if line.strip()]

    # Derive the expected best version
    valid_versions = []
    for v in available:
        parsed_v = parse_semver(v)
        is_valid = True
        for c in constraints:
            parts = c.split()
            if len(parts) != 2:
                continue
            op, target = parts
            parsed_t = parse_semver(target)

            if op == '>=' and not (parsed_v >= parsed_t): is_valid = False
            elif op == '<=' and not (parsed_v <= parsed_t): is_valid = False
            elif op == '>' and not (parsed_v > parsed_t): is_valid = False
            elif op == '<' and not (parsed_v < parsed_t): is_valid = False
            elif op == '==' and not (parsed_v == parsed_t): is_valid = False
            elif op == '!=' and not (parsed_v != parsed_t): is_valid = False

        if is_valid:
            valid_versions.append(v)

    if valid_versions:
        expected_version = max(valid_versions, key=parse_semver)
    else:
        expected_version = "None"

    with open(out_path, 'r', encoding='utf-8') as f:
        actual_version = f.read().strip()

    assert actual_version == expected_version, (
        f"Incorrect resolved version. "
        f"Expected '{expected_version}' based on constraints, but got '{actual_version}'."
    )