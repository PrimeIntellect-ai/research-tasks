# test_final_state.py

import os
import json
import hashlib
import difflib
import pytest

RAW_TICKETS_PATH = "/home/user/raw_tickets.txt"
GROUPED_TICKETS_PATH = "/home/user/grouped_tickets.json"
PIPELINE_LOG_PATH = "/home/user/pipeline.log"

def compute_expected_state():
    if not os.path.exists(RAW_TICKETS_PATH):
        pytest.fail(f"Input file {RAW_TICKETS_PATH} is missing, cannot compute expected state.")

    with open(RAW_TICKETS_PATH, 'r') as f:
        content = f.read().strip()

    blocks = [b.strip() for b in content.split('===') if b.strip()]
    raw_count = len(blocks)

    tickets = []
    for b in blocks:
        lines = b.split('\n')
        tid = ""
        desc = ""
        for line in lines:
            if line.startswith("Ticket:"):
                tid = line.split("Ticket:", 1)[1].strip()
            elif line.startswith("Description:"):
                desc = line.split("Description:", 1)[1].strip()
        tickets.append({"id": tid, "desc": desc})

    seen_hashes = set()
    unique_tickets = []
    for t in tickets:
        norm_desc = t["desc"].strip().lower()
        h = hashlib.sha256(norm_desc.encode('utf-8')).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique_tickets.append(t)

    unique_count = len(unique_tickets)

    # Connected components for grouping
    parent = {t["id"]: t["id"] for t in unique_tickets}
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            # make the alphabetically smaller ID the root for consistency
            if root_i < root_j:
                parent[root_j] = root_i
            else:
                parent[root_i] = root_j

    for i in range(len(unique_tickets)):
        for j in range(i + 1, len(unique_tickets)):
            t1 = unique_tickets[i]
            t2 = unique_tickets[j]
            ratio = difflib.SequenceMatcher(None, t1["desc"], t2["desc"]).ratio()
            if ratio >= 0.85:
                union(t1["id"], t2["id"])

    groups_dict = {}
    for t in unique_tickets:
        root = find(t["id"])
        groups_dict.setdefault(root, []).append(t["id"])

    final_groups = []
    for g in groups_dict.values():
        final_groups.append(sorted(g))

    final_groups.sort(key=lambda x: x[0])
    group_count = len(final_groups)

    return raw_count, unique_count, group_count, final_groups

def test_grouped_tickets_json():
    assert os.path.exists(GROUPED_TICKETS_PATH), f"Output file {GROUPED_TICKETS_PATH} is missing."

    with open(GROUPED_TICKETS_PATH, 'r') as f:
        try:
            actual_groups = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {GROUPED_TICKETS_PATH} does not contain valid JSON.")

    assert isinstance(actual_groups, list), f"Expected JSON array in {GROUPED_TICKETS_PATH}, got {type(actual_groups).__name__}."
    for group in actual_groups:
        assert isinstance(group, list), "Expected inner elements to be arrays."

    _, _, _, expected_groups = compute_expected_state()

    # Normalize actual groups (sort inner arrays, then sort outer array)
    normalized_actual = [sorted(g) for g in actual_groups]
    normalized_actual.sort(key=lambda x: x[0] if x else "")

    assert normalized_actual == expected_groups, f"Grouped tickets do not match expected logic. Expected: {expected_groups}, Actual: {normalized_actual}"

def test_pipeline_log():
    assert os.path.exists(PIPELINE_LOG_PATH), f"Log file {PIPELINE_LOG_PATH} is missing."

    with open(PIPELINE_LOG_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    raw_count, unique_count, group_count, _ = compute_expected_state()

    expected_lines = [
        f"TOTAL_RAW: {raw_count}",
        f"TOTAL_UNIQUE_AFTER_HASH: {unique_count}",
        f"TOTAL_GROUPS: {group_count}"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {PIPELINE_LOG_PATH}, found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert actual == expected, f"Log line mismatch. Expected '{expected}', but got '{actual}'."