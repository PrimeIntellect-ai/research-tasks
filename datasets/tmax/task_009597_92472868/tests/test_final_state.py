# test_final_state.py
import os
import json
import sqlite3
import pytest

OUTPUT_PATH = '/home/user/output/top_modules_graph.json'
DB_PATH = '/home/user/data/legacy_system.db'

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_json_structure_and_metadata():
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert "page" in data, "Missing 'page' in JSON."
    assert "limit" in data, "Missing 'limit' in JSON."
    assert "total_active_modules" in data, "Missing 'total_active_modules' in JSON."
    assert "results" in data, "Missing 'results' in JSON."

    assert data["page"] == 1, f"Expected page 1, got {data['page']}"
    assert data["limit"] == 3, f"Expected limit 3, got {data['limit']}"
    assert isinstance(data["results"], list), "'results' should be a list."

def test_json_computed_values():
    # Recompute truth from the database to align with principles
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get active modules
    cursor.execute("SELECT mod_id, mod_name FROM registry_modules WHERE current_status != 'deprecated'")
    active_modules = {row[0]: row[1] for row in cursor.fetchall()}

    # Get valid links
    cursor.execute("SELECT source_mod_id, target_mod_id FROM module_dependencies")
    links = cursor.fetchall()

    incoming = {mod_id: [] for mod_id in active_modules}
    outgoing = {mod_id: [] for mod_id in active_modules}

    for src, tgt in links:
        if src in active_modules and tgt in active_modules:
            incoming[tgt].append(active_modules[src])
            outgoing[src].append(active_modules[tgt])

    # Sort lists alphabetically
    for mod_id in active_modules:
        incoming[mod_id].sort()
        outgoing[mod_id].sort()

    # Calculate in_degree and prepare results
    results = []
    for mod_id, mod_name in active_modules.items():
        results.append({
            "module_name": mod_name,
            "in_degree": len(incoming[mod_id]),
            "incoming": incoming[mod_id],
            "outgoing": outgoing[mod_id]
        })

    # Sort results: in_degree descending, then module_name ascending
    results.sort(key=lambda x: (-x["in_degree"], x["module_name"]))

    # Paginate (limit 3)
    expected_results = results[:3]
    expected_total_active = len(active_modules)

    conn.close()

    # Validate against actual output
    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    assert data["total_active_modules"] == expected_total_active, \
        f"Expected total_active_modules to be {expected_total_active}, got {data['total_active_modules']}"

    assert len(data["results"]) == 3, \
        f"Expected exactly 3 results, got {len(data['results'])}"

    for i in range(3):
        actual = data["results"][i]
        expected = expected_results[i]

        assert actual["module_name"] == expected["module_name"], \
            f"Result {i} module_name mismatch: expected {expected['module_name']}, got {actual.get('module_name')}"
        assert actual["in_degree"] == expected["in_degree"], \
            f"Result {i} in_degree mismatch: expected {expected['in_degree']}, got {actual.get('in_degree')}"
        assert actual["incoming"] == expected["incoming"], \
            f"Result {i} incoming mismatch: expected {expected['incoming']}, got {actual.get('incoming')}"
        assert actual["outgoing"] == expected["outgoing"], \
            f"Result {i} outgoing mismatch: expected {expected['outgoing']}, got {actual.get('outgoing')}"