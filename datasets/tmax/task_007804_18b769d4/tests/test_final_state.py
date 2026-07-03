# test_final_state.py

import os
import json
import sqlite3
import heapq
import pytest

DEPS_JSON_PATH = "/home/user/deps.json"
DB_PATH = "/home/user/artifacts.db"
ARTIFACTS_DIR = "/home/user/artifacts"

def get_expected_build_order():
    """
    Derives the expected build order by performing a topological sort
    on the dependencies defined in deps.json, using alphabetical tie-breaking.
    """
    assert os.path.exists(DEPS_JSON_PATH), f"Missing {DEPS_JSON_PATH}"
    with open(DEPS_JSON_PATH, "r") as f:
        deps = json.load(f)

    in_degree = {pkg: 0 for pkg in deps}
    graph = {pkg: [] for pkg in deps}

    for pkg, pkg_deps in deps.items():
        in_degree[pkg] = len(pkg_deps)
        for dep in pkg_deps:
            if dep not in graph:
                graph[dep] = []
                in_degree[dep] = 0
            graph[dep].append(pkg)

    ready = [pkg for pkg, deg in in_degree.items() if deg == 0]
    heapq.heapify(ready)

    build_order = []
    while ready:
        curr = heapq.heappop(ready)
        build_order.append(curr)
        for neighbor in graph.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(ready, neighbor)

    return build_order

def test_database_schema_updated():
    """
    Verifies that the 'build_order' column of type INTEGER was added to the 'packages' table.
    """
    assert os.path.exists(DB_PATH), f"{DB_PATH} does not exist"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(packages);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    conn.close()

    assert "build_order" in columns, "Column 'build_order' is missing from 'packages' table"
    assert columns["build_order"].upper() == "INTEGER", "Column 'build_order' should be of type INTEGER"

def test_database_build_order_values():
    """
    Verifies that the 'build_order' column is correctly populated with a 1-based index
    corresponding to the topological sort order.
    """
    expected_order = get_expected_build_order()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, build_order FROM packages;")
    rows = cursor.fetchall()
    conn.close()

    db_build_order = {row[0]: row[1] for row in rows}

    for i, pkg in enumerate(expected_order, start=1):
        assert pkg in db_build_order, f"Package '{pkg}' missing from database"
        assert db_build_order[pkg] == i, f"Expected build_order for '{pkg}' to be {i}, got {db_build_order[pkg]}"

def test_mock_artifact_files():
    """
    Verifies that the mock artifact files are created in the artifacts directory
    with the correct naming and content.
    """
    expected_order = get_expected_build_order()

    assert os.path.isdir(ARTIFACTS_DIR), f"Directory {ARTIFACTS_DIR} does not exist"

    for pkg in expected_order:
        mock_file = os.path.join(ARTIFACTS_DIR, f"{pkg}.mock")
        assert os.path.isfile(mock_file), f"Mock artifact file {mock_file} is missing"

        with open(mock_file, "r") as f:
            content = f.read().strip()

        expected_content = f"MOCK_BUILD_{pkg}"
        assert content == expected_content, f"Content of {mock_file} is incorrect. Expected '{expected_content}', got '{content}'"