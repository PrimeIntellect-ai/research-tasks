# test_final_state.py

import os
import re
import binascii
import pytest

WORKSPACE_DIR = "/home/user/project_workspace"
SOURCE_FILES_DIR = os.path.join(WORKSPACE_DIR, "source_files")
DEPS_HEX = os.path.join(WORKSPACE_DIR, "deps.hex")
ANALYZER_C = os.path.join(WORKSPACE_DIR, "analyzer.c")
ANALYZER_BIN = os.path.join(WORKSPACE_DIR, "analyzer")
BUILD_ORDER = os.path.join(WORKSPACE_DIR, "build_order.txt")

def test_rust_extractor_output():
    assert os.path.isfile(DEPS_HEX), f"Missing {DEPS_HEX}. The Rust extractor may not have run successfully."

    with open(DEPS_HEX, "r") as f:
        hex_data = f.read().strip()

    try:
        decoded = binascii.unhexlify(hex_data).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Could not decode {DEPS_HEX} as hex-encoded UTF-8: {e}")

    expected_pairs = set()
    for fname in os.listdir(SOURCE_FILES_DIR):
        fpath = os.path.join(SOURCE_FILES_DIR, fname)
        if os.path.isfile(fpath):
            with open(fpath, "r") as f:
                for line in f:
                    m = re.match(r'#include\s+"([^"]+)"', line)
                    if m:
                        expected_pairs.add(f"{fname} {m.group(1)}")

    actual_pairs = set(line.strip() for line in decoded.splitlines() if line.strip())
    assert actual_pairs == expected_pairs, f"Extracted dependencies in {DEPS_HEX} do not match the expected source file includes."

def test_c_analyzer_exists():
    assert os.path.isfile(ANALYZER_C), f"Missing C source file: {ANALYZER_C}"
    assert os.path.isfile(ANALYZER_BIN), f"Missing compiled executable: {ANALYZER_BIN}"
    assert os.access(ANALYZER_BIN, os.X_OK), f"The file {ANALYZER_BIN} is not executable."

def test_build_order_output():
    assert os.path.isfile(BUILD_ORDER), f"Missing output file: {BUILD_ORDER}"

    nodes = set()
    deps = {}
    rev_deps = {}

    for fname in os.listdir(SOURCE_FILES_DIR):
        if os.path.isfile(os.path.join(SOURCE_FILES_DIR, fname)):
            nodes.add(fname)
            if fname not in deps:
                deps[fname] = set()
            if fname not in rev_deps:
                rev_deps[fname] = set()

            with open(os.path.join(SOURCE_FILES_DIR, fname), "r") as f:
                for line in f:
                    m = re.match(r'#include\s+"([^"]+)"', line)
                    if m:
                        dep = m.group(1)
                        nodes.add(dep)
                        deps[fname].add(dep)
                        if dep not in rev_deps:
                            rev_deps[dep] = set()
                        rev_deps[dep].add(fname)

    in_degree = {n: len(deps.get(n, [])) for n in nodes}
    queue = [n for n in nodes if in_degree[n] == 0]

    expected_order = []
    while queue:
        queue.sort()
        u = queue.pop(0)
        expected_order.append(u)
        for v in rev_deps.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    with open(BUILD_ORDER, "r") as f:
        actual_order = [line.strip() for line in f if line.strip()]

    assert actual_order == expected_order, (
        f"Build order mismatch.\n"
        f"Expected: {expected_order}\n"
        f"Got:      {actual_order}\n"
        "Ensure topological sort correctly resolves dependencies and breaks ties alphabetically."
    )