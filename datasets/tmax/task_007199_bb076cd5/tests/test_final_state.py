# test_final_state.py

import os
import stat
import subprocess
import pytest
from collections import defaultdict

SCRIPT_PATH = "/home/user/analyze_collaboration.sh"
AUTHORS_PATH = "/home/user/authors.csv"
COAUTHORS_PATH = "/home/user/coauthors.csv"

def compute_expected_output(target_id):
    dept_map = {}
    if os.path.isfile(AUTHORS_PATH):
        with open(AUTHORS_PATH, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    dept_map[parts[0]] = parts[2]

    adj = defaultdict(set)
    if os.path.isfile(COAUTHORS_PATH):
        with open(COAUTHORS_PATH, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    u, v = parts[0], parts[1]
                    adj[u].add(v)
                    adj[v].add(u)

    target = str(target_id)
    first_degree = adj[target]
    second_degree = set()
    for neighbor in first_degree:
        second_degree.update(adj[neighbor])

    strict_second = second_degree - first_degree - {target}

    counts = defaultdict(int)
    for node in strict_second:
        if node in dept_map:
            counts[dept_map[node]] += 1

    result = []
    for dept in sorted(counts.keys()):
        result.append(f"{dept}:{counts[dept]}")

    return "\n".join(result)

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable"

@pytest.mark.parametrize("author_id", [3, 1, 6, 2])
def test_script_logic(author_id):
    assert os.path.isfile(SCRIPT_PATH), "Script missing"

    expected = compute_expected_output(author_id)

    result = subprocess.run(
        [SCRIPT_PATH, str(author_id)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with non-zero exit code for AuthorID {author_id}. Error: {result.stderr}"

    actual_output = result.stdout.strip()
    expected_output = expected.strip()

    assert actual_output == expected_output, (
        f"Output mismatch for AuthorID {author_id}.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Got:\n{actual_output}"
    )