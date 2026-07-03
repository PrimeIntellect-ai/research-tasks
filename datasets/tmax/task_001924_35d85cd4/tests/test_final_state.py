# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/query_engine.sh"
DATA_PATH = "/home/user/data/employees.jsonl"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable"

def run_script(args):
    cmd = [SCRIPT_PATH] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    lines = result.stdout.strip().split('\n')
    if lines == ['']:
        return []

    parsed = []
    for i, line in enumerate(lines):
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Output line {i+1} is not valid JSON: {line}")
    return parsed

def test_specific_test_case():
    """
    Test the exact combination specified in the instructions:
    --status active --min-salary 100000 --sort-by salary --sort-order desc --skip 1 --limit 2
    """
    args = [
        "--status", "active",
        "--min-salary", "100000",
        "--sort-by", "salary",
        "--sort-order", "desc",
        "--skip", "1",
        "--limit", "2"
    ]

    output = run_script(args)

    assert len(output) == 2, f"Expected 2 results, got {len(output)}"

    expected = [
        {"id": "e04", "name": "Diana", "department": "Engineering", "salary": 130000},
        {"id": "e01", "name": "Alice", "department": "Engineering", "salary": 120000}
    ]

    assert output == expected, f"Expected {expected}, but got {output}"

def test_default_parameters():
    """
    Test script with no arguments. Should return first 10 records by default sorted by id asc.
    """
    output = run_script([])

    assert len(output) == 10, f"Expected 10 results (default limit), got {len(output)}"

    # Check projection
    for record in output:
        assert set(record.keys()) == {"id", "name", "department", "salary"}, "Projection must only include id, name, department, salary"

    # Check default sort (id asc)
    ids = [record["id"] for record in output]
    assert ids == sorted(ids), "Default sorting should be by id ascending"

def test_filter_and_pagination():
    """
    Test filtering by department (not explicitly in params, but min-salary is), skip and limit.
    """
    args = [
        "--min-salary", "80000",
        "--skip", "2",
        "--limit", "3"
    ]

    output = run_script(args)

    # Expected salaries >= 80000, sorted by id asc (default)
    # e01 (120k), e02 (85k), e03 (95k), e04 (130k), e06 (115k), e07 (90k), e08 (140k), e10 (105k)
    # Skip 2 -> start at e03
    # Limit 3 -> e03, e04, e06

    assert len(output) == 3, f"Expected 3 results, got {len(output)}"
    expected_ids = ["e03", "e04", "e06"]
    actual_ids = [record["id"] for record in output]

    assert actual_ids == expected_ids, f"Expected IDs {expected_ids}, got {actual_ids}"