# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = '/home/user/backups.db'
DEADLOCKS_PATH = '/home/user/deadlocks.txt'
DURATIONS_PATH = '/home/user/durations.txt'

def get_expected_data():
    if not os.path.exists(DB_PATH):
        return [], []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, duration FROM jobs")
    jobs = dict(cursor.fetchall())

    cursor.execute("SELECT job_id, depends_on_id FROM dependencies")
    deps = cursor.fetchall()
    conn.close()

    graph = {job: [] for job in jobs}
    for job_id, depends_on in deps:
        if job_id in graph:
            graph[job_id].append(depends_on)

    # Cycle detection
    def find_cycles():
        visited = set()
        path = []
        in_cycle = set()

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                for n in path[cycle_start:]:
                    in_cycle.add(n)
                return
            if node in visited:
                return

            visited.add(node)
            path.append(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            path.pop()

        for node in graph:
            dfs(node)

        return in_cycle

    cycles = find_cycles()

    # Transitive dependencies
    def get_all_deps(node):
        deps_set = set()
        stack = [node]
        while stack:
            curr = stack.pop()
            for n in graph.get(curr, []):
                if n not in deps_set:
                    deps_set.add(n)
                    stack.append(n)
        return deps_set

    durations = {}
    for job in jobs:
        all_deps = get_all_deps(job)
        # Check if job or any of its dependencies are in a cycle
        if job in cycles or any(dep in cycles for dep in all_deps):
            continue

        total_duration = jobs[job] + sum(jobs[dep] for dep in all_deps if dep in jobs)
        durations[job] = total_duration

    expected_deadlocks = sorted(list(cycles))
    expected_durations = [f"{job}: {durations[job]}" for job in sorted(durations.keys())]

    return expected_deadlocks, expected_durations

def test_deadlocks_file_exists():
    assert os.path.isfile(DEADLOCKS_PATH), f"File {DEADLOCKS_PATH} was not created."

def test_durations_file_exists():
    assert os.path.isfile(DURATIONS_PATH), f"File {DURATIONS_PATH} was not created."

def test_deadlocks_content():
    expected_deadlocks, _ = get_expected_data()

    with open(DEADLOCKS_PATH, 'r') as f:
        actual_deadlocks = [line.strip() for line in f if line.strip()]

    assert actual_deadlocks == expected_deadlocks, (
        f"Contents of {DEADLOCKS_PATH} do not match expected deadlocks.\n"
        f"Expected: {expected_deadlocks}\n"
        f"Got: {actual_deadlocks}"
    )

def test_durations_content():
    _, expected_durations = get_expected_data()

    with open(DURATIONS_PATH, 'r') as f:
        actual_durations = [line.strip() for line in f if line.strip()]

    assert actual_durations == expected_durations, (
        f"Contents of {DURATIONS_PATH} do not match expected durations.\n"
        f"Expected: {expected_durations}\n"
        f"Got: {actual_durations}"
    )