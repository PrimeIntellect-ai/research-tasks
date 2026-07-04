# test_final_state.py

import os
import json
import hashlib
import re
from collections import defaultdict, deque
import pytest

PIPELINE_DIR = "/home/user/legacy_pipeline"
PLAN_PATH = "/home/user/migration_plan.json"
LINUX_BIN = "/home/user/migrator/build/migrator-linux"
WINDOWS_BIN = "/home/user/migrator/build/migrator-windows.exe"

def compute_expected_plan():
    files = [f for f in os.listdir(PIPELINE_DIR) if f.endswith('.py')]

    scripts_info = {}
    graph = defaultdict(list)
    in_degree = {f: 0 for f in files}

    for f in files:
        path = os.path.join(PIPELINE_DIR, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        deps = []
        schema = ""
        weight = 0

        for line in content.splitlines():
            if line.startswith('# DEPENDS_ON:'):
                deps_str = line.split(':', 1)[1].strip()
                if deps_str:
                    deps = [d.strip() for d in deps_str.split(',')]
            elif line.startswith('# SCHEMA_VERSION:'):
                schema = line.split(':', 1)[1].strip()
            elif line.startswith('# WEIGHT_FACTOR:'):
                weight = int(line.split(':', 1)[1].strip())

        # Calculate checksum
        stripped_lines = [line for line in content.split('\n') if not line.startswith('#')]
        stripped_content = '\n'.join(stripped_lines)
        checksum = hashlib.sha256(stripped_content.encode('utf-8')).hexdigest()

        # Calculate target schema
        if schema.startswith('v'):
            major = int(schema[1:].split('.')[0])
            target_schema = f"v{major + 1}.0"
        else:
            target_schema = ""

        scripts_info[f] = {
            "weight": weight,
            "deps": deps,
            "checksum": checksum,
            "target_schema": target_schema,
            "total_weight": weight
        }

    for f, info in scripts_info.items():
        for dep in info["deps"]:
            graph[dep].append(f)
            in_degree[f] += 1

    # Topological sort with alphabetical tie-breaking
    queue = [f for f in files if in_degree[f] == 0]
    queue.sort()

    sorted_scripts = []

    while queue:
        # Sort queue to ensure alphabetical order for tie-breaking at the current level
        queue.sort()
        curr = queue.pop(0)
        sorted_scripts.append(curr)

        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Calculate total weights
    # We can calculate total weights dynamically based on dependencies
    def get_total_weight(script):
        w = scripts_info[script]["weight"]
        for dep in scripts_info[script]["deps"]:
            w += get_total_weight(dep)
        return w

    expected_plan = []
    for script in sorted_scripts:
        total_weight = get_total_weight(script)
        expected_plan.append({
            "script": script,
            "total_weight": total_weight,
            "checksum": scripts_info[script]["checksum"],
            "target_schema": scripts_info[script]["target_schema"]
        })

    return expected_plan

def test_migration_plan_exists_and_correct():
    assert os.path.exists(PLAN_PATH), f"Expected JSON report at {PLAN_PATH} is missing."

    with open(PLAN_PATH, 'r', encoding='utf-8') as f:
        try:
            actual_plan = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PLAN_PATH} is not valid JSON.")

    expected_plan = compute_expected_plan()

    assert isinstance(actual_plan, list), "JSON report must be a list of objects."
    assert len(actual_plan) == len(expected_plan), f"Expected {len(expected_plan)} scripts in the report, found {len(actual_plan)}."

    for i, (actual, expected) in enumerate(zip(actual_plan, expected_plan)):
        assert actual.get("script") == expected["script"], f"Order mismatch at index {i}: expected {expected['script']}, got {actual.get('script')}"
        assert actual.get("total_weight") == expected["total_weight"], f"Weight mismatch for {expected['script']}: expected {expected['total_weight']}, got {actual.get('total_weight')}"
        assert actual.get("checksum") == expected["checksum"], f"Checksum mismatch for {expected['script']}: expected {expected['checksum']}, got {actual.get('checksum')}"
        assert actual.get("target_schema") == expected["target_schema"], f"Schema mismatch for {expected['script']}: expected {expected['target_schema']}, got {actual.get('target_schema')}"

def test_linux_binary_exists_and_valid():
    assert os.path.exists(LINUX_BIN), f"Linux binary missing at {LINUX_BIN}"
    assert os.access(LINUX_BIN, os.X_OK), f"Linux binary at {LINUX_BIN} is not executable."

    with open(LINUX_BIN, 'rb') as f:
        header = f.read(4)
        assert header == b'\x7fELF', f"File {LINUX_BIN} is not a valid ELF binary."

def test_windows_binary_exists_and_valid():
    assert os.path.exists(WINDOWS_BIN), f"Windows binary missing at {WINDOWS_BIN}"

    with open(WINDOWS_BIN, 'rb') as f:
        header = f.read(2)
        assert header == b'MZ', f"File {WINDOWS_BIN} is not a valid Windows PE binary (missing MZ header)."