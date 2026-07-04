# test_final_state.py

import os
import json
import pytest

def compute_expected_state():
    file_path = '/home/user/backup_jobs.jsonl'
    assert os.path.exists(file_path), f"Input file {file_path} is missing."

    jobs = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                j = json.loads(line)
                jobs[j['job_id']] = j.get('depends_on', [])

    # Helper to get all reachable dependencies
    def get_reachable(start):
        visited = set()
        stack = [start]
        while stack:
            curr = stack.pop()
            for dep in jobs.get(curr, []):
                if dep not in visited:
                    visited.add(dep)
                    stack.append(dep)
        return visited

    # Find nodes that are part of a cycle (can reach themselves)
    in_cycle = set()
    for job in jobs:
        if job in get_reachable(job):
            in_cycle.add(job)

    # Group cycle nodes into distinct cycles
    cycle_groups = []
    unassigned = set(in_cycle)
    while unassigned:
        start = unassigned.pop()
        comp = {start}
        for other in list(unassigned):
            if start in get_reachable(other) and other in get_reachable(start):
                comp.add(other)
                unassigned.remove(other)
        cycle_groups.append(sorted(list(comp)))

    cycle_groups.sort(key=lambda x: x[0])

    # Find all stuck nodes (either in a cycle or dependent on a cycle)
    stuck = set(in_cycle)
    for job in jobs:
        if job not in stuck:
            reach = get_reachable(job)
            if reach.intersection(in_cycle):
                stuck.add(job)

    # Compute tiers for remaining valid jobs
    remaining = set(jobs.keys()) - stuck
    job_tier = {}

    def get_tier(job):
        if job in job_tier:
            return job_tier[job]
        deps = jobs.get(job, [])
        if not deps:
            job_tier[job] = 0
            return 0
        t = max(get_tier(d) for d in deps) + 1
        job_tier[job] = t
        return t

    tiers = {}
    for job in remaining:
        t = get_tier(job)
        if t not in tiers:
            tiers[t] = []
        tiers[t].append(job)

    schedule = {str(k): sorted(v) for k, v in tiers.items()}

    return cycle_groups, schedule

def test_deadlocks_json():
    expected_cycles, _ = compute_expected_state()

    file_path = '/home/user/deadlocks.json'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            actual_cycles = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    assert isinstance(actual_cycles, list), f"{file_path} should contain a list of lists."
    assert len(actual_cycles) == len(expected_cycles), f"Expected {len(expected_cycles)} deadlocks, found {len(actual_cycles)}."

    assert actual_cycles == expected_cycles, f"Deadlocks mismatch. Expected: {expected_cycles}, Actual: {actual_cycles}"

def test_valid_schedule_json():
    _, expected_schedule = compute_expected_state()

    file_path = '/home/user/valid_schedule.json'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            actual_schedule = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    assert isinstance(actual_schedule, dict), f"{file_path} should contain a JSON object (dictionary)."

    assert actual_schedule == expected_schedule, f"Valid schedule mismatch. Expected: {expected_schedule}, Actual: {actual_schedule}"